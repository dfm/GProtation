from __future__ import print_function
import numpy as np
from GProt import calc_p_init, fit
import pandas as pd
import os
import matplotlib.pyplot as plt
from multiprocessing import Pool

DATA_DIR = "../code/simulations/kepler_diffrot_full/final"
RESULTS_DIR = "results/"


def load_suzanne_lcs(id):
    id = str(int(id)).zfill(4)
    x, y = np.genfromtxt(os.path.join(DATA_DIR,
                                      "lightcurve_{0}.txt".format(id))).T
    return x - x[0], y - 1


def comparison_plot(truths):
    """
    Plot the acf, pgram and GP results.
    """
    m = truths.DELTA_OMEGA.values == 0
    pgrams, acfs = [np.zeros_like(truths.N.values[m]) for i in range(2)]
    pgram_errs, acf_errs = [np.zeros_like(truths.N.values[m]) for i in
                            range(2)]
    for i, id in enumerate(truths.N.values[m]):
        acf_fname = os.path.join(RESULTS_DIR,
                                 "{0}_acf_result.txt".format(str(int(id))
                                                             .zfill(4)))
        acfs[i], acf_errs[i] = np.genfromtxt(acf_fname).T
        p_fname = os.path.join(RESULTS_DIR,
                               "{0}_pgram_result.txt".format(str(int(id))
                                                             .zfill(4)))
        pgrams[i], pgram_errs[i] = np.genfromtxt(p_fname).T

    plt.clf()
    plt.errorbar(truths.P_MIN.values[m], acfs, yerr=acf_errs, fmt="k.",
                capsize=0)
    plt.ylim(0, 100)
    xs = np.arange(0, 100, 1)
    plt.plot(xs, xs, "k--", alpha=.5)
    plt.plot(truths.P_MIN.values[m], pgrams, "r.")
    plt.savefig("compare")


def recover(i):

    DIR = "../code/simulations/kepler_diffrot_full/par/"
    truths = pd.read_csv(os.path.join(DIR, "final_table.txt"), delimiter=" ")
    m = truths.DELTA_OMEGA.values == 0

    id = truths.N.values[m][i]
    print(id, i, "of", len(truths.N.values[m]))
    x, y = load_suzanne_lcs(str(int(id)).zfill(4))
    yerr = np.ones_like(y) * 1e-5
    acf_period, a_err, pgram_period, p_err = calc_p_init(x, y, yerr,
                                                         str(int(id))
                                                         .zfill(4))
    p_init = pgram_period
    c, sub = 100, 100  # cut off at 200 days
    mc = x < c
    xb, yb, yerrb = x[mc][::sub], y[mc][::sub], yerr[mc][::sub]
    fit(xb, yb, yerrb, acf_period, str(int(id)).zfill(4))


if __name__ == "__main__":

    DIR = "../code/simulations/kepler_diffrot_full/par/"
    truths = pd.read_csv(os.path.join(DIR, "final_table.txt"), delimiter=" ")
    m = truths.DELTA_OMEGA.values == 0

    comparison_plot(truths)

    for i in range(len(truths.N.values[m])):
        recover(i)
#     pool = Pool()
#     results = pool.map(recover, range(len(truths.N.values[m])))
#     results = pool.map(recover, range(len(truths.N.values[m])))
