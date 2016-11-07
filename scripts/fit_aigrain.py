#!/usr/bin/env python

import sys
sys.path.append('..')
from gprotation.aigrain import AigrainLightCurve
from gprotation.model import GPRotModel
from gprotation.config import POLYCHORD

def fit_polychord(i, test=False):
    sys.path.append(POLYCHORD)
    import PyPolyChord.PyPolyChord as PolyChord

    lc = AigrainLightCurve(i)
    mod = GPRotModel(lc)
    basename = str(i)
    if test:
        print('Will run polychord on star {}...')
    else:
        _ = PolyChord.run_nested_sampling(mod.polychord_lnpost, 5, 0,
                        prior=mod.polychord_prior,
                        file_root=basename)    

def fit_mnest(i, test=False, **kwargs):
    import pymultinest

    lc = AigrainLightCurve(i)
    mod = GPRotModel(lc)
    basename = str(i)
    if test:
        print('Will run multinest on star {}...')
    else:
        _ = pymultinest.run(mod.mnest_loglike, mod.mnest_prior, 5, **kwargs)

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('stars', nargs='*', type=int)
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--polychord', action='store_true')

    args = parser.parse_args()

    for i in args.stars:
        if args.polychord:
            fit_polychord(i, test=args.test)
        else:
            fit_mnest(i, test=args.test)
