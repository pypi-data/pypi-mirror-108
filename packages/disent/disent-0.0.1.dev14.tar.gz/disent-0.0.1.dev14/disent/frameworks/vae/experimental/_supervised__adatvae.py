#  ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  MIT License
#
#  Copyright (c) 2021 Nathan Juraj Michlo
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#  ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~

import logging
from dataclasses import dataclass
from typing import Sequence
from typing import Tuple

import torch
from deprecated import deprecated
from torch.distributions import Distribution
from torch.distributions import Normal

from disent.nn.loss.triplet import configured_dist_triplet
from disent.nn.loss.triplet import configured_triplet
from disent.frameworks.vae._supervised__tvae import TripletVae
from disent.frameworks.vae._weaklysupervised__adavae import AdaVae
from disent.frameworks.vae._weaklysupervised__adavae import compute_average_distribution


log = logging.getLogger(__name__)


# ========================================================================= #
# Guided Ada Vae                                                            #
# ========================================================================= #


@deprecated(reason='Rather use the AdaNegTripletVae')
class AdaTripletVae(TripletVae):

    REQUIRED_OBS = 3

    @dataclass
    class cfg(TripletVae.cfg, AdaVae.cfg):
        # adavae
        ada_thresh_mode: str = 'dist'  # only works for: adat_share_mask_mode == "posterior"
        # ada_tvae - loss
        adat_triplet_loss: str = 'triplet_hard_neg_ave'  # should be used with a schedule!
        adat_triplet_ratio: float = 1.0
        adat_triplet_soft_scale: float = 1.0
        adat_triplet_pull_weight: float = 0.1  # only works for: adat_triplet_loss == "triplet_hard_neg_ave_pull"
        adat_triplet_share_scale: float = 0.95  # only works for: adat_triplet_loss == "triplet_hard_neg_ave_scaled"
        # ada_tvae - averaging
        adat_share_mask_mode: str = 'posterior'
        adat_share_ave_mode: str = 'all'  # only works for: adat_triplet_loss == "triplet_hard_ave_all"

    def hook_compute_ave_aug_loss(self, ds_posterior: Sequence[Normal], ds_prior: Sequence[Normal], zs_sampled: Sequence[torch.Tensor], xs_partial_recon: Sequence[torch.Tensor], xs_targ: Sequence[torch.Tensor]):
        return self.estimate_ada_triplet_loss(
            ds_posterior=ds_posterior,
            cfg=self.cfg,
        )

    @staticmethod
    def estimate_ada_triplet_loss(ds_posterior: Sequence[Normal], cfg: cfg):
        """
        zs_params and ds_posterior are convenience variables here.
        - they should contain the same values
        - in practice we only need one of them and can compute the other!
        """
        # compute shared masks, shared embeddings & averages over shared embeddings
        share_masks, share_logs = compute_triplet_shared_masks(ds_posterior, cfg=cfg)
        ds_posterior_shared, ds_posterior_shared_ave = compute_ave_shared_distributions(ds_posterior, share_masks, cfg=cfg)

        # compute loss
        ada_triplet_loss, ada_triplet_logs = AdaTripletVae.compute_ada_triplet_loss(
            share_masks=share_masks,
            zs=[d.mean for d in ds_posterior],
            zs_shared=[d.mean for d in ds_posterior_shared],
            zs_shared_ave=[d.mean for d in ds_posterior_shared_ave],
            cfg=cfg,
        )

        return ada_triplet_loss, {
            **ada_triplet_logs,
            **share_logs,
        }

    @staticmethod
    def compute_ada_triplet_loss(share_masks: Sequence[torch.Tensor], zs: Sequence[Normal], zs_shared: Sequence[Normal], zs_shared_ave: Sequence[Normal], cfg: cfg):

        # Normal Triplet Loss
        (a_z, p_z, n_z) = zs
        trip_loss = configured_triplet(a_z, p_z, n_z, cfg=cfg)

        # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ #
        # Hard Losses - zs_shared
        # TODO: implement triplet over KL divergence rather than l1/l2 distance?
        # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ #

        # Hard Averaging Before Triplet
        (ap_a_ave, ap_p_ave, an_a_ave, an_n_ave, pn_p_ave, pn_n_ave) = zs_shared
        triplet_hard_ave     = configured_dist_triplet(pos_delta=ap_a_ave - ap_p_ave, neg_delta=an_a_ave - an_n_ave, cfg=cfg)
        triplet_hard_ave_neg = configured_dist_triplet(pos_delta=a_z      - p_z,      neg_delta=an_a_ave - an_n_ave, cfg=cfg)

        # Hard Averaging Before Triplet - PULLING PUSHING
        (ap_share_mask, an_share_mask, pn_share_mask) = share_masks
        neg_delta_push = torch.where(~an_share_mask, a_z - n_z, torch.zeros_like(a_z))  # this is the same as: an_a_ave - an_n_ave
        neg_delta_pull = torch.where( an_share_mask, a_z - n_z, torch.zeros_like(a_z))
        triplet_hard_ave_neg_pull = configured_dist_push_pull_triplet(pos_delta=a_z - p_z, neg_delta=neg_delta_push, neg_delta_pull=neg_delta_pull, cfg=cfg)

        # Hard All Averaging Before Triplet
        (a_ave, p_ave, n_ave) = zs_shared_ave
        triplet_all_hard_ave = configured_dist_triplet(pos_delta=a_ave-p_ave, neg_delta=a_ave-n_ave, cfg=cfg)

        # Soft Scaled Negative Triplet
        triplet_hard_neg_ave_scaled = configured_dist_triplet(
            pos_delta=a_z - p_z,
            neg_delta=torch.where(an_share_mask, cfg.adat_triplet_share_scale * (a_z - n_z), (a_z - n_z)),
            cfg=cfg,
        )

        # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ #
        # Soft Losses
        # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ #

        # Individual Pair Averaging Losses
        _soft_ap_loss = configured_soft_ave_loss(share_mask=ap_share_mask, delta=a_z - p_z, cfg=cfg)
        _soft_an_loss = configured_soft_ave_loss(share_mask=an_share_mask, delta=a_z - n_z, cfg=cfg)
        _soft_pn_loss = configured_soft_ave_loss(share_mask=pn_share_mask, delta=p_z - n_z, cfg=cfg)

        # soft losses
        soft_loss_an       = (_soft_an_loss)
        soft_loss_an_ap    = (_soft_an_loss + _soft_ap_loss) / 2
        soft_loss_an_ap_pn = (_soft_an_loss + _soft_ap_loss + _soft_pn_loss) / 3

        # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ #
        # Return
        # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ #

        losses = {
            'triplet':                   trip_loss,
            # soft ave
            'triplet_soft_ave_neg':      trip_loss + soft_loss_an,
            'triplet_soft_ave_p_n':      trip_loss + soft_loss_an_ap,
            'triplet_soft_ave_all':      trip_loss + soft_loss_an_ap_pn,
            # hard ave
            'triplet_hard_ave':          torch.lerp(trip_loss, triplet_hard_ave,          weight=cfg.adat_triplet_ratio),
            'triplet_hard_neg_ave':      torch.lerp(trip_loss, triplet_hard_ave_neg,      weight=cfg.adat_triplet_ratio),
            'triplet_hard_neg_ave_pull': torch.lerp(trip_loss, triplet_hard_ave_neg_pull, weight=cfg.adat_triplet_ratio),
            'triplet_hard_ave_all':      torch.lerp(trip_loss, triplet_all_hard_ave,      weight=cfg.adat_triplet_ratio),
            # scaled
            'triplet_hard_neg_ave_scaled': torch.lerp(trip_loss, triplet_hard_neg_ave_scaled, weight=cfg.adat_triplet_ratio),
        }

        return losses[cfg.adat_triplet_loss], {
            'triplet': trip_loss,
            'triplet_chosen': losses[cfg.adat_triplet_loss],
        }


# ========================================================================= #
# Ada-TVae                                                                  #
# ========================================================================= #


def dist_push_pull_triplet(pos_delta, neg_delta, neg_delta_pull, margin_max=1., p=1, pull_weight=1.):
    """
    Pushing Pulling Triplet Loss
    - should match standard triplet loss if pull_weight=0.
    """
    p_dist = torch.norm(pos_delta, p=p, dim=-1)
    n_dist = torch.norm(neg_delta, p=p, dim=-1)
    n_dist_pull = torch.norm(neg_delta_pull, p=p, dim=-1)
    loss = torch.clamp_min(p_dist - n_dist + margin_max + pull_weight * n_dist_pull, 0)
    return loss.mean()


def configured_dist_push_pull_triplet(pos_delta, neg_delta, neg_delta_pull, cfg: AdaTripletVae.cfg):
    """
    required config params:
    - cfg.triplet_margin_max:      (0, inf)
    - cfg.triplet_p:               1 or 2
    - cfg.triplet_scale:           [0, inf)
    - cfg.adat_triplet_pull_weight: [0, 1]
    """
    return dist_push_pull_triplet(
        pos_delta=pos_delta, neg_delta=neg_delta, neg_delta_pull=neg_delta_pull,
        margin_max=cfg.triplet_margin_max, p=cfg.triplet_p, pull_weight=cfg.adat_triplet_pull_weight,
    ) * cfg.triplet_scale


def soft_ave_loss(share_mask, delta):
    return torch.norm(torch.where(share_mask, delta, torch.zeros_like(delta)), p=2, dim=-1).mean()


def configured_soft_ave_loss(share_mask, delta, cfg: AdaTripletVae.cfg):
    """
    required config params:
    - cfg.triplet_scale:          [0, inf)
    - cfg.adat_triplet_soft_scale: [0, inf)
    """
    return soft_ave_loss(share_mask=share_mask, delta=delta) * (cfg.adat_triplet_soft_scale * cfg.triplet_scale)


# ========================================================================= #
# AveAda-TVAE                                                               #
# ========================================================================= #


def compute_triplet_shared_masks_from_zs(zs: Sequence[torch.Tensor], cfg):
    """
    required config params:
    - cfg.ada_thresh_ratio:
    """
    a_z, p_z, n_z = zs
    # shared elements that need to be averaged, computed per pair in the batch.
    ap_share_mask = AdaVae.compute_z_shared_mask(a_z, p_z, ratio=cfg.ada_thresh_ratio)
    an_share_mask = AdaVae.compute_z_shared_mask(a_z, n_z, ratio=cfg.ada_thresh_ratio)
    pn_share_mask = AdaVae.compute_z_shared_mask(p_z, n_z, ratio=cfg.ada_thresh_ratio)
    # return values
    share_masks = (ap_share_mask, an_share_mask, pn_share_mask)
    return share_masks, {
        'ap_shared': ap_share_mask.sum(dim=1).float().mean(),
        'an_shared': an_share_mask.sum(dim=1).float().mean(),
        'pn_shared': pn_share_mask.sum(dim=1).float().mean(),
    }


def compute_triplet_shared_masks(ds_posterior: Sequence[Distribution], cfg: AdaTripletVae.cfg):
    """
    required config params:
    - cfg.ada_thresh_ratio:
    - cfg.ada_thresh_mode: "kl", "symmetric_kl", "dist", "sampled_dist"
      : only applies if cfg.ada_share_mask_mode=="posterior"
    - cfg.adat_share_mask_mode: "posterior", "sample", "sample_each"
    """
    a_posterior, p_posterior, n_posterior = ds_posterior

    # shared elements that need to be averaged, computed per pair in the batch.
    if cfg.adat_share_mask_mode == 'posterior':
        ap_share_mask = AdaVae.compute_posterior_shared_mask(a_posterior, p_posterior, thresh_mode=cfg.ada_thresh_mode, ratio=cfg.ada_thresh_ratio)
        an_share_mask = AdaVae.compute_posterior_shared_mask(a_posterior, n_posterior, thresh_mode=cfg.ada_thresh_mode, ratio=cfg.ada_thresh_ratio)
        pn_share_mask = AdaVae.compute_posterior_shared_mask(p_posterior, n_posterior, thresh_mode=cfg.ada_thresh_mode, ratio=cfg.ada_thresh_ratio)
    elif cfg.adat_share_mask_mode == 'sample':
        a_z_sample, p_z_sample, n_z_sample = a_posterior.rsample(), p_posterior.rsample(), n_posterior.rsample()
        ap_share_mask = AdaVae.compute_z_shared_mask(a_z_sample, p_z_sample, ratio=cfg.ada_thresh_ratio)
        an_share_mask = AdaVae.compute_z_shared_mask(a_z_sample, n_z_sample, ratio=cfg.ada_thresh_ratio)
        pn_share_mask = AdaVae.compute_z_shared_mask(p_z_sample, n_z_sample, ratio=cfg.ada_thresh_ratio)
    elif cfg.adat_share_mask_mode == 'sample_each':
        ap_share_mask = AdaVae.compute_z_shared_mask(a_posterior.rsample(), p_posterior.rsample(), ratio=cfg.ada_thresh_ratio)
        an_share_mask = AdaVae.compute_z_shared_mask(a_posterior.rsample(), n_posterior.rsample(), ratio=cfg.ada_thresh_ratio)
        pn_share_mask = AdaVae.compute_z_shared_mask(p_posterior.rsample(), n_posterior.rsample(), ratio=cfg.ada_thresh_ratio)
    else:
        raise KeyError(f'Invalid cfg.adat_share_mask_mode={repr(cfg.adat_share_mask_mode)}')

    # return values
    share_masks = (ap_share_mask, an_share_mask, pn_share_mask)
    return share_masks, {
        'ap_shared': ap_share_mask.sum(dim=1).float().mean(),
        'an_shared': an_share_mask.sum(dim=1).float().mean(),
        'pn_shared': pn_share_mask.sum(dim=1).float().mean(),
    }


def compute_ave_shared_distributions(ds_posterior: Sequence[Normal], share_masks: Sequence[torch.Tensor], cfg: AdaTripletVae.cfg) -> Tuple[Sequence[Normal], Sequence[Normal]]:
    """
    required config params:
    - cfg.ada_average_mode: "gvae", "ml-vae"
    - cfg.adat_share_ave_mode: "all", "pos_neg", "pos", "neg"
    """
    a_posterior, p_posterior, n_posterior = ds_posterior
    ap_share_mask, an_share_mask, pn_share_mask = share_masks

    # compute shared embeddings
    ave_ap_a_posterior, ave_ap_p_posterior = AdaVae.make_averaged_distributions(a_posterior, p_posterior, ap_share_mask, average_mode=cfg.ada_average_mode)
    ave_an_a_posterior, ave_an_n_posterior = AdaVae.make_averaged_distributions(a_posterior, n_posterior, an_share_mask, average_mode=cfg.ada_average_mode)
    ave_pn_p_posterior, ave_pn_n_posterior = AdaVae.make_averaged_distributions(p_posterior, n_posterior, pn_share_mask, average_mode=cfg.ada_average_mode)

    # compute averaged shared embeddings
    if cfg.adat_share_ave_mode == 'all':
        ave_a_posterior = compute_average_distribution(ave_ap_a_posterior, ave_an_a_posterior, average_mode=cfg.ada_average_mode)
        ave_p_posterior = compute_average_distribution(ave_ap_p_posterior, ave_pn_p_posterior, average_mode=cfg.ada_average_mode)
        ave_n_posterior = compute_average_distribution(ave_an_n_posterior, ave_pn_n_posterior, average_mode=cfg.ada_average_mode)
    elif cfg.adat_share_ave_mode == 'pos_neg':
        ave_a_posterior = compute_average_distribution(ave_ap_a_posterior, ave_an_a_posterior, average_mode=cfg.ada_average_mode)
        ave_p_posterior = ave_ap_p_posterior
        ave_n_posterior = ave_an_n_posterior
    elif cfg.adat_share_ave_mode == 'pos':
        ave_a_posterior = ave_ap_a_posterior
        ave_p_posterior = ave_ap_p_posterior
        ave_n_posterior = n_posterior
    elif cfg.adat_share_ave_mode == 'neg':
        ave_a_posterior = ave_an_a_posterior
        ave_p_posterior = p_posterior
        ave_n_posterior = ave_an_n_posterior
    else:
        raise KeyError(f'Invalid cfg.adat_share_ave_mode={repr(cfg.adat_share_ave_mode)}')

    ds_posterior_shared = (
        ave_ap_a_posterior, ave_ap_p_posterior,  # a & p
        ave_an_a_posterior, ave_an_n_posterior,  # a & n
        ave_pn_p_posterior, ave_pn_n_posterior,  # p & n
    )

    ds_posterior_shared_ave = (
        ave_a_posterior,
        ave_p_posterior,
        ave_n_posterior
    )

    # return values
    return ds_posterior_shared, ds_posterior_shared_ave


# ========================================================================= #
# END                                                                       #
# ========================================================================= #
