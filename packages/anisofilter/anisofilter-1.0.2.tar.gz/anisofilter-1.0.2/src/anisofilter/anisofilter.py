"""
ANISOFILTER gets a noisy point cloud, its noise standard deviation and density value as inputs,
outputs the denoised point cloud.

The algorithm is published in:

Z. Xu and A. Foi, "Anisotropic Denoising of 3D Point Clouds by Aggregation of Multiple 
Surface-Adaptive Estimates," in IEEE Transactions on Visualization and Computer Graphics, 
vol. 27, no. 6, pp. 2851-2868, 1 June 2021, doi: 10.1109/TVCG.2019.2959761.

Copyright (c) 2019-2021 Noiseless Imaging Oy (Ltd).
All rights reserved.
This work (software, material, and documentation) shall only
be used for nonprofit noncommercial purposes.
Any unauthorized use of this work for commercial or for-profit purposes
is prohibited.
"""

import os
import platform
import numpy as np
import time
import ctypes
from sklearn.neighbors import KDTree


def _numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data], dtype=np.int32)

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]

    # Setup output array and put elements from data into masked positions
    out = -np.ones(mask.shape, dtype=np.int32)

    out[mask] = np.concatenate(data)
    return [out, lens]


def anisofilter(pcd_noi, sigma_pcd, dens_pcd):

    ##### c_fxn #####
    # A. Create library
    path = os.path.dirname(__file__) 
    if platform.system() == "Windows":
        libname = "libsquare_neigh_ici_denoi_recur_pure_c.dll"
    if platform.system() == "Linux":
        libname = "libsquare_neigh_ici_denoi_recur_pure_c.so"
    if platform.system() == "Darwin":
        libname = "libsquare_neigh_ici_denoi_recur_pure_c_mac.so"

    c_library = ctypes.CDLL(os.path.join(path,libname))

    # B. Specify function signatures
    c_fxn = c_library.square_neigh_ici_denoi_recur_pure_c
    c_fxn.argtypes = (ctypes.POINTER(ctypes.c_float),   # pcd
                      ctypes.c_int,                     # n_p
                      ctypes.POINTER(ctypes.c_float),   # sigma_map
                      ctypes.c_float,                   # dens_pcd
                      ctypes.c_float,                   # max_scale
                      ctypes.c_int,                     # start_scale
                      ctypes.c_float,                   # steps
                      ctypes.c_int,                     # dim_inc_times
                      ctypes.POINTER(ctypes.c_int),     # fix_idx_ball
                      ctypes.POINTER(ctypes.c_int),     # idx_lens
                      ctypes.c_int,                     # itr
                      ctypes.POINTER(ctypes.c_int),     # idx_knn
                      ctypes.c_int,                     # num_k
                      ctypes.POINTER(ctypes.c_float))   # closest_point_est

    # save ori dens_pcd
    dens_pcd_ori = dens_pcd

    # convert pcd to dens = 1
    pcd_noi = pcd_noi * np.sqrt(dens_pcd, dtype=np.float32)
    sigma_pcd = np.float32(sigma_pcd * np.sqrt(dens_pcd))
    dens_pcd = np.float32(1)

    # start neighborhood length(used in LPA - ICI during denosing part)
    start_scale = 3

    # the step value to increase the neighborhood size(used in LPA - ICI during denosing part)
    steps = np.sqrt(2, dtype=np.float32)

    # the maximun increase times(used in LPA - ICI during denosing part)
    dim_inc_times = 4
    max_scale = np.float32(start_scale * (steps ** dim_inc_times) / np.sqrt(dens_pcd))
    max_scale = max([max_scale, 3 * sigma_pcd])
    radius_square = np.float32(3 * max_scale ** 2)

    kdt = KDTree(pcd_noi, leaf_size=10, metric='euclidean')
    idx_ball = kdt.query_radius(pcd_noi, np.sqrt(radius_square))

    [fix_idx_ball, idx_lens] = _numpy_fillna(idx_ball)
    if not fix_idx_ball.flags['F_CONTIGUOUS']:
        fix_idx_ball = np.asfortranarray(fix_idx_ball)

    # initialize sigma map
    sigma_map = sigma_pcd * np.ones(len(pcd_noi), dtype=np.float32)

    for itr in range(0, 2):
        ######
        # compute and store knn of each point for once
        num_k = 50  # the size of knn neighbourhood

        # idx of KNN of each point
        kdt = KDTree(pcd_noi, leaf_size=10, metric='euclidean')
        dist, idx_knn = kdt.query(pcd_noi, k=num_k)
        idx_knn = np.int32(idx_knn)
        if not idx_knn.flags['F_CONTIGUOUS']:
            idx_knn = np.asfortranarray(idx_knn)
        ######

        # define pointers
        p_pcd_noi = pcd_noi.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        p_sig_m = sigma_map.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        p_fix_idx_ball = fix_idx_ball.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        p_idx_lens = idx_lens.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        p_idx_knn = idx_knn.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

        n_p = len(pcd_noi)
        closest_point_est = np.zeros((n_p, 3), dtype=np.float32)
        p_closest_point_est = closest_point_est.ctypes.data_as(ctypes.POINTER(ctypes.c_float))

        start_time = time.time()
        c_fxn(p_pcd_noi, n_p, p_sig_m, dens_pcd, max_scale, start_scale, steps, dim_inc_times,
              p_fix_idx_ball, p_idx_lens, itr, p_idx_knn, num_k, p_closest_point_est)
        pcd_noi = closest_point_est
        #print("--- main loop %s seconds ---" % (time.time() - start_time))
        print("///////////// itr = %d is finished, took %.5f seconds ///////////////" % (itr+1, time.time() - start_time))

    pcd_de_m2c = closest_point_est / np.sqrt(dens_pcd_ori)

    return pcd_de_m2c
