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

from abc import abstractmethod
from typing import List
from typing import Optional

import numpy as np
from torch.utils.data import Dataset
from torch.utils.data.dataloader import default_collate

from disent.util.iters import LengthIter


# ========================================================================= #
# util                                                                      #
# ========================================================================= #


class DisentDataset(Dataset, LengthIter):

    @property
    @abstractmethod
    def transform(self) -> Optional[callable]:
        raise NotImplementedError

    @property
    @abstractmethod
    def augment(self) -> Optional[callable]:
        raise NotImplementedError

    def _get_augmentable_observation(self, idx):
        raise NotImplementedError

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Single Datapoints                                                     #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    def _datapoint_raw_to_target(self, dat):
        x_targ = dat
        if self.transform is not None:
            x_targ = self.transform(x_targ)
        return x_targ

    def _datapoint_target_to_input(self, x_targ):
        x = x_targ
        if self.augment is not None:
            x = self.augment(x)
            x = _batch_to_observation(batch=x, obs_shape=x_targ.shape)
        return x

    def dataset_get(self, idx, mode: str):
        """
        Gets the specified datapoint, using the specified mode.
        - raw: direct untransformed/unaugmented observations
        - target: transformed observations
        - input: transformed then augmented observations
        - pair: (input, target) tuple of observations

        Pipeline:
            1. raw    = dataset[idx]
            2. target = transform(raw)
            3. input  = augment(target) = augment(transform(raw))

        :param idx: The index of the datapoint in the dataset
        :param mode: {'raw', 'target', 'input', 'pair'}
        :return: observation depending on mode
        """
        try:
            idx = int(idx)
        except:
            raise TypeError(f'Indices must be integer-like ({type(idx)}): {idx}')
        # we do not support indexing by lists
        x_raw = self._get_augmentable_observation(idx)
        # return correct data
        if mode == 'pair':
            x_targ = self._datapoint_raw_to_target(x_raw)  # applies self.transform
            x = self._datapoint_target_to_input(x_targ)    # applies self.augment
            return x, x_targ
        elif mode == 'input':
            x_targ = self._datapoint_raw_to_target(x_raw)  # applies self.transform
            x = self._datapoint_target_to_input(x_targ)    # applies self.augment
            return x
        elif mode == 'target':
            x_targ = self._datapoint_raw_to_target(x_raw)  # applies self.transform
            return x_targ
        elif mode == 'raw':
            return x_raw
        else:
            raise ValueError(f'Invalid {mode=}')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Multiple Datapoints                                                   #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    def dataset_get_observation(self, *idxs):
        xs, xs_targ = zip(*(self.dataset_get(idx, mode='pair') for idx in idxs))
        # handle cases
        if self.augment is None:
            # makes 5-10% faster
            return {
                'x_targ': xs_targ,
            }
        else:
            return {
                'x': xs,
                'x_targ': xs_targ,
            }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Batches                                                               #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    def dataset_batch_from_indices(self, indices: List[int], mode: str):
        """Get a batch of observations X from a batch of factors Y."""
        return default_collate([self.dataset_get(idx, mode=mode) for idx in indices])

    def dataset_sample_batch(self, num_samples: int, mode: str):
        """Sample a batch of observations X."""
        # sample indices
        indices = set()
        while len(indices) < num_samples:
            indices.add(np.random.randint(0, len(self)))
        # done
        return self.dataset_batch_from_indices(sorted(indices), mode=mode)


# ========================================================================= #
# util                                                                      #
# ========================================================================= #


def _batch_to_observation(batch, obs_shape):
    """
    Convert a batch of size 1, to a single observation.
    """
    if batch.shape != obs_shape:
        assert batch.shape == (1, *obs_shape), f'batch.shape={repr(batch.shape)} does not correspond to obs_shape={repr(obs_shape)} with batch dimension added'
        return batch.reshape(obs_shape)
    return batch


# ========================================================================= #
# END                                                                       #
# ========================================================================= #
