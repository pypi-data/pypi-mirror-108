# -*- coding: utf-8 -*-

import numpy as np

from sktime.transformations.base import _PanelToTabularTransformer
from sktime.utils.validation.panel import check_X

from numba import njit, prange, vectorize

from itertools import combinations


class MiniRocket(_PanelToTabularTransformer):
    """
    MINImally RandOm Convolutional KErnel Transform (MINI ROCKET).
    Univariate Only. For details and explanation on the algorithm, users are referred to [1]_.
    
    Parameters
    ----------
    num_features : int, optional
        Number of features. The default is 10_000.
    max_dilations_per_kernel : TYPE, optional
        Maximum number of dilations per kernel. The default is 32.
    random_state : int, optional
        Random seed. The default is None.
    
    
    Notes
    -----
    .. [1] "Dempster, Angus and Schmidt, Daniel F and Webb, Geoffrey I, MINIROCKET: A Very Fast (Almost) Deterministic Transform for Time Series Classification" (2020). arXiv:2012.08791
    
    """

    def __init__(self, num_features=10_000, 
                 max_dilations_per_kernel=32, random_state=None):
        self.num_features = num_features
        self.max_dilations_per_kernel = max_dilations_per_kernel
        self.random_state = (
            np.int32(random_state) if isinstance(random_state, int) else None
        )
        super(MiniRocket, self).__init__()
        self.indices = np.array(
            [_ for _ in combinations(np.arange(9), 3)], dtype=np.int32)

    def fit(self, X, y=None):
        """
        Fits dilations and biases to input time series.
        
        Parameters
        ----------
        X : DataFrame or array, shape=(n_samples, n_features, n_timestamps) 
            Input time series (sktime format).
        y : array, shape=(n_samples) 
            Target values (optional, ignored as irrelevant).
        
        Returns
        -------
        self
        
        """
        X = check_X(X, enforce_univariate=True, coerce_to_numpy=True)
        X = X[:, 0, :].astype(np.float32)
        _, n_timepoints = X.shape
        if n_timepoints < 9:
            raise ValueError(
                (
                    f"n_timepoints must be >= 9, but found {n_timepoints};"
                    " zero pad shorter series so that n_timepoints == 9"
                )
            )
        self.parameters = _fit(
            X, self.indices, self.num_features, self.max_dilations_per_kernel, self.random_state
        )
        self._is_fitted = True
        return self

    def transform(self, X, y=None, return_locs=False):
        """
        Transforms input time series.
        
        Parameters
        ----------
        
        X : DataFrame or array, shape=(n_samples, n_features, n_timestamps) 
            Input time series (sktime format).
        y : array, shape=(n_samples) 
            Target values (optional, ignored as irrelevant).
        
        Returns
        -------
        array, shape=(n_samples, n_kernels)
        
        """
        self.check_is_fitted()
        X = check_X(X, enforce_univariate=True, coerce_to_numpy=True)
        X = X[:, 0, :].astype(np.float32)
        features, locations = _transform(X, self.indices, self.parameters)
        if return_locs:
            return features, locations
        else:
            return features


@njit(
    fastmath=True,
    parallel=True,
    cache=True,
)
def _fit_biases(X, indices, dilations, num_features_per_dilation, quantiles, seed):

    if seed is not None:
        np.random.seed(seed)

    n_instances, n_timepoints = X.shape
    # >>>

    num_kernels = len(indices)
    num_dilations = len(dilations)

    num_features = num_kernels * np.sum(num_features_per_dilation)

    biases = np.zeros(num_features, dtype=np.float32)

    feature_index_start = 0

    for dilation_index in prange(num_dilations):

        dilation = dilations[dilation_index]
        padding = ((9 - 1) * dilation) // 2

        num_features_this_dilation = num_features_per_dilation[dilation_index]

        for kernel_index in prange(num_kernels):

            feature_index_end = feature_index_start + num_features_this_dilation

            _X = X[np.random.randint(n_instances)]

            A = -_X  # A = alpha * X = -X
            G = _X + _X + _X  # G = gamma * X = 3X

            C_alpha = np.zeros(n_timepoints, dtype=np.float32)
            C_alpha[:] = A

            C_gamma = np.zeros((9, n_timepoints), dtype=np.float32)
            C_gamma[9 // 2] = G

            start = dilation
            end = n_timepoints - padding

            for gamma_index in prange(9 // 2):

                C_alpha[-end:] = C_alpha[-end:] + A[:end]
                C_gamma[gamma_index, -end:] = G[:end]

                end += dilation

            for gamma_index in prange(9 // 2 + 1, 9):

                C_alpha[:-start] = C_alpha[:-start] + A[start:]
                C_gamma[gamma_index, :-start] = G[start:]

                start += dilation

            index_0, index_1, index_2 = indices[kernel_index]

            C = C_alpha + C_gamma[index_0] + \
                C_gamma[index_1] + C_gamma[index_2]

            biases[feature_index_start:feature_index_end] = np.quantile(
                C, quantiles[feature_index_start:feature_index_end]
            )

            feature_index_start = feature_index_end

    return biases


def _fit_dilations(n_timepoints, num_features, max_dilations_per_kernel):

    num_kernels = 84

    num_features_per_kernel = num_features // num_kernels
    true_max_dilations_per_kernel = min(
        num_features_per_kernel, max_dilations_per_kernel
    )
    multiplier = num_features_per_kernel / true_max_dilations_per_kernel

    max_exponent = np.log2((n_timepoints - 1) / (9 - 1))
    dilations, num_features_per_dilation = np.unique(
        np.logspace(0, max_exponent, true_max_dilations_per_kernel, base=2).astype(
            np.int32
        ),
        return_counts=True,
    )
    num_features_per_dilation = (num_features_per_dilation * multiplier).astype(
        np.int32
    )  # this is a vector

    remainder = num_features_per_kernel - np.sum(num_features_per_dilation)
    i = 0
    while remainder > 0:
        num_features_per_dilation[i] += 1
        remainder -= 1
        i = (i + 1) % len(num_features_per_dilation)

    return dilations, num_features_per_dilation


def _quantiles(n):
    return np.array(
        [(_ * ((np.sqrt(5) + 1) / 2)) % 1 for _ in range(1, n + 1)], dtype=np.float32
    )


def _fit(X, indices, num_features=10_000, max_dilations_per_kernel=32, seed=None):

    _, n_timepoints = X.shape

    num_kernels = 84

    dilations, num_features_per_dilation = _fit_dilations(
        n_timepoints, num_features, max_dilations_per_kernel
    )

    num_features_per_kernel = np.sum(num_features_per_dilation)

    quantiles = _quantiles(num_kernels * num_features_per_kernel)

    biases = _fit_biases(X, indices, dilations,
                         num_features_per_dilation, quantiles, seed)

    return dilations, num_features_per_dilation, biases


@vectorize("float32(float32,float32)", nopython=True, cache=True)
def _PPV(a, b):
    if a > b:
        return 1
    else:
        return 0


@njit(
    fastmath=True,
    parallel=False,
    cache=True,
)
def _conv_to_input_indexes(convolution_indexes, dilation, padding, length, n_timepoints):
    indexes = np.zeros((n_timepoints), dtype=np.uint8)
    for i_conv in prange(convolution_indexes.shape[0]):
        for i_x in prange(length):
            i = convolution_indexes[i_conv] + i_x*dilation - padding
            if 0 <= i < n_timepoints:
                indexes[i] += 1
    return indexes


@njit(
    fastmath=True,
    parallel=True,
    cache=True,
)
def _transform(X, indices, parameters):

    n_instances, n_timepoints = X.shape

    dilations, num_features_per_dilation, biases = parameters

    num_kernels = len(indices)
    num_dilations = len(dilations)

    num_features = num_kernels * np.sum(num_features_per_dilation)

    features = np.zeros((n_instances, num_features), dtype=np.float32)
    # Count how many time an X index is used for a ppv
    features_location = np.zeros(
        (n_instances, num_features, n_timepoints), dtype=np.uint8)

    for example_index in prange(n_instances):

        _X = X[example_index]

        A = -_X  # A = alpha * X = -X
        G = _X + _X + _X  # G = gamma * X = 3X

        feature_index_start = 0

        for dilation_index in range(num_dilations):

            _padding0 = dilation_index % 2

            dilation = dilations[dilation_index]
            padding = ((9 - 1) * dilation) // 2

            num_features_this_dilation = num_features_per_dilation[dilation_index]

            C_alpha = np.zeros(n_timepoints, dtype=np.float32)
            C_alpha[:] = A

            C_gamma = np.zeros((9, n_timepoints), dtype=np.float32)
            C_gamma[9 // 2] = G

            start = dilation
            end = n_timepoints - padding

            for gamma_index in range(9 // 2):

                C_alpha[-end:] = C_alpha[-end:] + A[:end]
                C_gamma[gamma_index, -end:] = G[:end]

                end += dilation

            for gamma_index in range(9 // 2 + 1, 9):

                C_alpha[:-start] = C_alpha[:-start] + A[start:]
                C_gamma[gamma_index, :-start] = G[start:]

                start += dilation

            for kernel_index in range(num_kernels):

                feature_index_end = feature_index_start + num_features_this_dilation

                _padding1 = (_padding0 + kernel_index) % 2

                index_0, index_1, index_2 = indices[kernel_index]

                C = C_alpha + C_gamma[index_0] + \
                    C_gamma[index_1] + C_gamma[index_2]

                if _padding1 == 0:
                    for feature_count in range(num_features_this_dilation):
                        ppv = _PPV(
                            C, biases[feature_index_start + feature_count])
                        features[example_index, feature_index_start +
                                 feature_count] = ppv.mean()

                        input_indexes = _conv_to_input_indexes(np.where(ppv > 0)[0],
                                                               dilation, padding,
                                                               9, n_timepoints)
                        features_location[
                            example_index, feature_index_start + feature_count, :
                        ] += input_indexes

                else:
                    for feature_count in range(num_features_this_dilation):
                        ppv = _PPV(C[padding:-padding],
                                   biases[feature_index_start + feature_count])
                        features[example_index, feature_index_start +
                                 feature_count] = ppv.mean()
                        input_indexes = _conv_to_input_indexes(np.where(ppv > 0)[0],
                                                               dilation, 0,
                                                               9, n_timepoints)
                        features_location[
                            example_index, feature_index_start + feature_count, :
                        ] += input_indexes

                feature_index_start = feature_index_end

    return features, features_location
