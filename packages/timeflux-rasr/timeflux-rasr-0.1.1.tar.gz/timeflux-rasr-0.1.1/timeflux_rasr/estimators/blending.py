from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted
import numpy as np


class Blending(BaseEstimator, TransformerMixin):
    """Smooths features temporally to avoid discontinuities by sine-cosine blending interpolation.

    This estimator smooths features to avoid discontinuities by blending the redundant samples that has been
    transformed by different operations. Only samples with the exact same timestamp will be blended. Features with an
    unique timestamp will be left untouched. Therefore this function is useful only if the two following criteria are
    met:
    - there is an overlapping between the features of each consecutive observation
    - the features have been transformed by different operators or by an adaptive operator.

    Parameters
    ----------
    window_overlap : int (default=1)
        Number of overlapping features that will be used for blending.
    merge : bool (default=False)
        If set to True, the output will be a unique 2D matrix when all windows will be collapsed and overlapping samples
        merged. By default, each window will be blended with the previous window.
    windowing : bool | None (default=None)
        If None or False, there is no interpolation for the first trial.
        If True, the first trial will be interpolate to zeros (sinus windowing).


    Attributes
    ----------
    n_channels_ : int
        The dimension managed by the fitted Blending, e.g. number of electrodes.`
    last_window_ : ndarray, shape (Nt, Ne)
        The last window observed during the last call of transform. It will be blended with the first window.
    """

    def __init__(self, window_overlap=1, merge=False, windowing=None):
        if window_overlap is None:
            raise ValueError("window_overlap parameter is not initialized.")
        if not isinstance(window_overlap, int):
            raise TypeError("window_overlap must int")

        self.window_overlap = window_overlap

        if not isinstance(merge, bool):
            raise TypeError("merge must bool")
        self.merge = merge

        if windowing is not None:
            if not isinstance(windowing, bool):
                raise TypeError("windowing must be None, or bool")

        self.windowing = windowing
        self.last_window_ = None  # init last_window_

    def fit(self, X, y=None):
        """
        Parameters
        ----------
        X : ndarray, shape (n_trials,  n_samples, n_channels)
            Training data.
        y : ndarray, shape (n_trials,) | None, optional
            labels corresponding to each trial, not used (mentioned for sklearn comp)

        Returns
        -------
        self : Blending instance.
            the fitted Blending estimator.
        """
        if len(X.shape) == 3:
            Nt, Ns, self.n_channels_ = X.shape
        else:
            raise ValueError("X.shape should be (n_trials, n_samples, n_electrodes).")

        check_array(X, allow_nd=True)
        return self

    def transform(self, X):
        """Blend signals
        Parameters
        ----------
        X : ndarray, shape (n_trials, n_samples, n_channels)
            Data to clean, already filtered
        Returns
        -------
        Xblended : ndarray, shape (n_trials, n_samples, n_channels)
            Cleaned data
        """
        # Check is fit had been called
        check_is_fitted(self, "n_channels_")

        X = check_array(X, allow_nd=True, copy=True)
        # Check that the input is of the same shape as the one passed
        # during fit.
        if len(X.shape) == 3:
            Nt, Ns, Ne = X.shape
        else:
            raise ValueError("X.shape should be (n_trials, n_samples, n_electrodes).")

        if Ne != self.n_channels_:
            raise ValueError("Shape of input is different from what was seen in `fit`")

        if self.window_overlap > 0:  # apply blending only if samples are overlapping
            # estimate the blending coefficients
            # blending is doing an temporal sinus-cosinus interpolation between two redundant samples.
            # if self.window_overlap is 1, it is an average between the last and first sample (blend_coeff is 0.5)
            blend_coeff = (
                1
                - np.cos(
                    np.pi
                    * (
                        np.arange(1, self.window_overlap + 1)
                        / (self.window_overlap + 1)
                    )
                )
            ) / 2
            blend_coeff = blend_coeff[:, None]

            for k in range(Nt):  # for each epoch
                if (k == 0) and (self.last_window_ is None):
                    # case: first use of the class
                    if self.windowing is True:
                        # interpolate the first trial with zero (windowing)
                        self.last_window_ = np.zeros((Ns, Ne))
                        last_values = self.last_window_[
                            -self.window_overlap :, :
                        ]  # blending from zero

                    else:
                        # no interpolation
                        self.last_window_ = X[0, :, :]
                        last_values = self.last_window_[
                            : self.window_overlap, :
                        ]  # no blending
                else:
                    # case:
                    last_values = self.last_window_[
                        -self.window_overlap :, :
                    ]  # blending from previous window

                new_values = X[k, 0 : self.window_overlap, :]
                self.last_window_ = X[k, :, :]
                X[k, 0 : self.window_overlap, :] = ((1 - blend_coeff) * last_values) + (
                    blend_coeff * new_values
                )

        if self.merge:
            return _merge_overlap(X, self.window_overlap)
        else:
            return X

    def fit_transform(self, X, y=None):
        """
        Parameters
        ----------
        X : ndarray, shape (n_trials,  n_samples, n_channels)
            Training data.
        y : ndarray, shape (n_trials,) | None, optional
            labels corresponding to each trial, not used (mentioned for sklearn comp)
        Returns
        -------
        X : ndarray, shape (n_trials, n_samples, n_channels)
            blended data
        """
        self.fit(X, y)

        return self.transform(X)


def _merge_overlap(X, window_overlap):
    """Convert 3D epoched signals into continuous 2D signals for a given overlap by removing redundant samples.

    Parameters
    ----------
    X : ndarray, shape (n_trials,  n_samples, n_channels)
        The epoched data to flatten.
    window_overlap : int (default=0)
        Number of overlapping samples shared between epochs. Non-negative. If 0, just concatenate the trials.

    Returns
    -------
    Xmerged : ndarray, shape (n_samples_new, n_channels)
        the merged signals into 2D matrix without redundant samples.
    """
    if len(X.shape) == 3:
        Nt, Ns, Ne = X.shape
    else:
        raise ValueError("X.shape should be (n_trials, n_samples, n_electrodes).")

    if window_overlap < 0:
        raise ValueError("window_overlap should be non-negative.")
    if window_overlap > Ns:
        raise ValueError("window_overlap cannot be higher than n_samples.")

    if window_overlap > 0:
        interval = Ns - window_overlap
        Ns_new = (Ns) + (interval * (Nt - 1))
        Xmerged = np.zeros((Ns_new, Ne))
        for k in range(Nt):
            i = k * interval
            subrange = np.arange(i, i + Ns)
            Xmerged[subrange, :] = X[k, :, :]
    else:
        Xmerged = np.concatenate(X)

    return Xmerged
