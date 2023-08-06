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
from typing import Tuple

import numpy as np
from torch.utils.data.dataloader import default_collate

from disent.data.groundtruth.base import GroundTruthData
from disent.dataset import DisentDataset


log = logging.getLogger(__name__)


# ========================================================================= #
# Convert ground truth data to a dataset                                    #
# ========================================================================= #


class GroundTruthDataset(DisentDataset, GroundTruthData):

    # TODO: these transformations should be a wrapper around any dataset.
    #       for example: dataset = AugmentedDataset(GroundTruthDataset(XYGridData()))

    def __init__(self, ground_truth_data: GroundTruthData, transform=None, augment=None):
        assert isinstance(ground_truth_data, GroundTruthData), f'{ground_truth_data=} must be an instance of GroundTruthData!'
        self.data = ground_truth_data
        super().__init__()
        self._transform = transform
        self._augment = augment

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Augmentable Dataset Overrides                                         #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    @property
    def transform(self):
        return self._transform

    @property
    def augment(self):
        return self._augment

    def _get_augmentable_observation(self, idx):
        return self.data[idx]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # State Space Overrides                                                 #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    @property
    def factor_names(self) -> Tuple[str, ...]:
        return self.data.factor_names

    @property
    def factor_sizes(self) -> Tuple[int, ...]:
        return self.data.factor_sizes

    @property
    def observation_shape(self) -> Tuple[int, ...]:
        return self.data.observation_shape

    def __getitem__(self, idx):
        # wrapped in tuple to match pair and triplet
        return self.dataset_get_observation(idx)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Single Datapoints                                                     #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    def dataset_batch_from_factors(self, factors: np.ndarray, mode: str):
        """Get a batch of observations X from a batch of factors Y."""
        return self.dataset_batch_from_indices(self.pos_to_idx(factors), mode=mode)

    def dataset_sample_batch_with_factors(self, num_samples: int, mode: str):
        """Sample a batch of observations X and factors Y."""
        factors = self.sample_factors(num_samples)
        batch = self.dataset_batch_from_factors(factors, mode=mode)
        return batch, default_collate(factors)

    def dataset_sample_batch(self, num_samples: int, mode: str):
        """Sample a batch of observations X."""
        factors = self.sample_factors(num_samples)
        batch = self.dataset_batch_from_factors(factors, mode=mode)
        return batch

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # End Class                                                             #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# ========================================================================= #
# EXTRA                                                                     #
# ========================================================================= #


class GroundTruthDatasetAndFactors(GroundTruthDataset):
    def dataset_get_observation(self, *idxs):
        return {
            **super().dataset_get_observation(*idxs),
            'factors': tuple(self.idx_to_pos(idxs))
        }


# ========================================================================= #
# END                                                                       #
# ========================================================================= #
