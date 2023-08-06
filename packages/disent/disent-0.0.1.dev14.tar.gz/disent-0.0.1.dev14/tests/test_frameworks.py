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

from dataclasses import asdict
from functools import partial

import pytest
import pytorch_lightning as pl
from torch.optim import Adam
from torch.utils.data import DataLoader

from disent.data.groundtruth import XYObjectData
from disent.dataset.groundtruth import GroundTruthDataset
from disent.dataset.groundtruth import GroundTruthDatasetPairs
from disent.dataset.groundtruth import GroundTruthDatasetTriples
from disent.frameworks.ae import *
from disent.frameworks.ae.experimental import *
from disent.frameworks.vae import *
from disent.frameworks.vae.experimental import *
from disent.model import AutoEncoder
from disent.model.ae import DecoderConv64
from disent.model.ae import EncoderConv64
from disent.nn.transform import ToStandardisedTensor


# ========================================================================= #
# TEST FRAMEWORKS                                                           #
# ========================================================================= #


@pytest.mark.parametrize(['Framework', 'cfg_kwargs', 'Data'], [
    # AE - unsupervised
    (Ae,                   dict(), XYObjectData),
    (TripletAe,            dict(), XYObjectData),
    # AE - weakly supervised
    (AdaAe,                dict(), XYObjectData),
    # AE - supervised
    (AdaNegTripletAe,      dict(), XYObjectData),
    # VAE - unsupervised
    (Vae,                  dict(),                                                                      XYObjectData),
    (BetaVae,              dict(),                                                                      XYObjectData),
    (DipVae,               dict(),                                                                      XYObjectData),
    (DipVae,               dict(dip_mode='i'),                                                          XYObjectData),
    (InfoVae,              dict(),                                                                      XYObjectData),
    (DfcVae,               dict(),                                                                      XYObjectData),
    (DfcVae,               dict(),                                                                      partial(XYObjectData, rgb=False)),
    (BetaTcVae,            dict(),                                                                      XYObjectData),
    (DataOverlapTripletVae,dict(overlap_mine_triplet_mode='none'),                                      XYObjectData),
    (DataOverlapTripletVae,dict(overlap_mine_triplet_mode='semi_hard_neg'),                             XYObjectData),
    (DataOverlapTripletVae,dict(overlap_mine_triplet_mode='hard_neg'),                                  XYObjectData),
    (DataOverlapTripletVae,dict(overlap_mine_triplet_mode='hard_pos'),                                  XYObjectData),
    (DataOverlapTripletVae,dict(overlap_mine_triplet_mode='easy_pos'),                                  XYObjectData),
    (DataOverlapRankVae,   dict(),                                                                      XYObjectData),
    # VAE - weakly supervised
    (AdaVae,               dict(),                                                                      XYObjectData),
    (AdaVae,               dict(ada_average_mode='ml-vae'),                                             XYObjectData),
    (SwappedTargetAdaVae,  dict(swap_chance=1.0),                                                       XYObjectData),
    (SwappedTargetBetaVae, dict(swap_chance=1.0),                                                       XYObjectData),
    (AugPosTripletVae,     dict(),                                                                      XYObjectData),
    # VAE - supervised
    (TripletVae,           dict(),                                                                      XYObjectData),
    (TripletVae,           dict(disable_decoder=True, disable_reg_loss=True, disable_posterior_scale=0.5), XYObjectData),
    (BoundedAdaVae,        dict(),                                                                      XYObjectData),
    (GuidedAdaVae,         dict(),                                                                      XYObjectData),
    (GuidedAdaVae,         dict(gada_anchor_ave_mode='thresh'),                                         XYObjectData),
    (TripletBoundedAdaVae, dict(),                                                                      XYObjectData),
    (TripletGuidedAdaVae,  dict(),                                                                      XYObjectData),
    (AdaTripletVae,        dict(),                                                                      XYObjectData),
    (AdaAveTripletVae,     dict(adat_share_mask_mode='posterior'),                                      XYObjectData),
    (AdaAveTripletVae,     dict(adat_share_mask_mode='sample'),                                         XYObjectData),
    (AdaAveTripletVae,     dict(adat_share_mask_mode='sample_each'),                                    XYObjectData),
])
def test_frameworks(Framework, cfg_kwargs, Data):
    DataWrapper = {
        1: GroundTruthDataset,
        2: GroundTruthDatasetPairs,
        3: GroundTruthDatasetTriples,
    }[Framework.REQUIRED_OBS]

    data = XYObjectData() if (Data is None) else Data()
    dataset = DataWrapper(data, transform=ToStandardisedTensor())
    dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True)

    framework = Framework(
        make_optimizer_fn=lambda params: Adam(params, lr=1e-3),
        make_model_fn=lambda: AutoEncoder(
            encoder=EncoderConv64(x_shape=data.x_shape, z_size=6, z_multiplier=2 if issubclass(Framework, Vae) else 1),
            decoder=DecoderConv64(x_shape=data.x_shape, z_size=6),
        ),
        cfg=Framework.cfg(**cfg_kwargs)
    )

    trainer = pl.Trainer(logger=False, checkpoint_callback=False, max_steps=256, fast_dev_run=True)
    trainer.fit(framework, dataloader)


def test_framework_config_defaults():
    # we test that defaults are working recursively
    assert asdict(BetaVae.cfg()) == dict(
        recon_loss='mse',
        disable_aug_loss=False,
        disable_decoder=False,
        disable_posterior_scale=None,
        disable_rec_loss=False,
        disable_reg_loss=False,
        loss_reduction='mean',
        latent_distribution='normal',
        kl_loss_mode='direct',
        beta=0.003,
    )
    assert asdict(BetaVae.cfg(recon_loss='bce', kl_loss_mode='approx')) == dict(
        recon_loss='bce',
        disable_aug_loss=False,
        disable_decoder=False,
        disable_posterior_scale=None,
        disable_rec_loss=False,
        disable_reg_loss=False,
        loss_reduction='mean',
        latent_distribution='normal',
        kl_loss_mode='approx',
        beta=0.003,
    )


# ========================================================================= #
# END                                                                       #
# ========================================================================= #
