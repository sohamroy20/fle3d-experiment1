import numpy as np

class IsotropicBasis3D:
    """
    Stable, dependency-free replacement for FLEBasis3D
    that produces rotation-invariant (isotropic) volumes.

    - No .mat files
    - No NUFFT
    - No spherical harmonics
    - Works on Kaggle, Mac, Linux
    """

    def __init__(self, N: int, nbins: int | None = None):
        self.N = int(N)
        self.nbins = nbins if nbins is not None else N // 2 + 1

        self._rbin = self._precompute_radius_bins()

    def _precompute_radius_bins(self):
        N = self.N
        coords = np.arange(N) - (N - 1) / 2
        x, y, z = np.meshgrid(coords, coords, coords, indexing="ij")
        r = np.sqrt(x**2 + y**2 + z**2)

        rmax = r.max()
        r_scaled = (r / rmax) * (self.nbins - 1)
        rbin = np.rint(r_scaled).astype(np.int32)
        return np.clip(rbin, 0, self.nbins - 1)

    # ---------- Forward transform ----------
    def evaluate_t(self, volume: np.ndarray) -> np.ndarray:
        """
        Maps 3D volume -> radial coefficients (rotation-invariant descriptor)
        """
        assert volume.shape == (self.N, self.N, self.N)

        flat_bins = self._rbin.ravel()
        flat_vals = volume.ravel().astype(np.float64)

        sums = np.bincount(flat_bins, weights=flat_vals, minlength=self.nbins)
        counts = np.bincount(flat_bins, minlength=self.nbins)

        coeffs = np.zeros(self.nbins)
        np.divide(sums, counts, out=coeffs, where=counts > 0)
        return coeffs

    # ---------- Isotropic selector ----------
    def keep_isotropic(self, coeffs: np.ndarray) -> np.ndarray:
        """
        In FLEBasis3D this was selecting l=0,m=0.
        Here the coefficients are already isotropic.
        """
        return coeffs.copy()

    # ---------- Backward transform ----------
    def evaluate(self, coeffs: np.ndarray) -> np.ndarray:
        """
        Reconstruct isotropic 3D volume from radial coefficients
        """
        assert coeffs.shape[0] == self.nbins
        return coeffs[self._rbin].astype(np.float32)