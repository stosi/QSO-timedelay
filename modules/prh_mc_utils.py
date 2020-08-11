import numpy as np


def power_law_sf(tau, slope, intercept):
    return 10 ** intercept * tau ** slope


def exp_sf(tau, V0, dt0):
    return V0 * (1 - np.exp(-tau / dt0))


def mag_to_flux(mag):
    return 10 ** (-mag / 2.5)


def flux_to_mag(flux):
    return -2.5 * np.log10(flux)


def compute_lags_matrix(t):
    N = len(t)
    t_row_repeated = np.repeat(t[np.newaxis, :], N, axis=0)
    t_col_repeated = np.repeat(t[:, np.newaxis], N, axis=1)
    tau = np.abs(t_row_repeated - t_col_repeated)
    return tau


def generate_PRH_light_curves(support, y, sigma, slope, intercept, delay, mag_shift):
    N = len(support)
    t_doubled = np.concatenate([support, support - delay])
    err_doubled = np.concatenate([sigma, sigma])
    tau_doubled = compute_lags_matrix(t_doubled)
    s2 = (y ** 2).mean()
    C = s2 - power_law_sf(tau_doubled, slope, intercept)
    C += 1e-10 * np.eye(2 * N)
    L = np.linalg.cholesky(C)
    y = L @ np.random.normal(0, 1, 2 * N) + err_doubled @ np.random.normal(0, 1, 2 * N)

    yA = y[:N] - y[:N].mean()
    yB = y[N:] - y[N:].mean()
    yB += mag_shift

    return yA, yB
