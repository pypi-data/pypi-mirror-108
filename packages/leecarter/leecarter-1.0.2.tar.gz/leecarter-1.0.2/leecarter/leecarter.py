import numpy as np


def lee_carter(rate, T, N, misc=False):

    logm_xt = np.log(rate).T

    a_x = logm_xt.sum(axis=1) / T
    z_xt = logm_xt - a_x.reshape(N, 1)

    U, S, V = np.linalg.svd(z_xt, full_matrices=True)

    bxkt = S[0] * np.dot(U[:, 0].reshape(N, 1), V[0, :].reshape(T, 1).T)
    eps = z_xt - bxkt

    logm_xt_lcfitted = bxkt + a_x.reshape(N, 1)

    b_x = U[:, 0]/U[:, 0].sum()
    k_t = V[0, :]*S[0]*U[:, 0].sum()
    a_x = a_x + k_t.sum()*b_x
    k_t = k_t - k_t.sum()

    kwargs = {"U": U, "S": S, "V": V, "logm_xt": logm_xt,
              "z_xt": z_xt, "eps": eps, "logm_xt_lcfitted": logm_xt_lcfitted}

    return (a_x, b_x, k_t, kwargs) if misc else (a_x, b_x, k_t)
