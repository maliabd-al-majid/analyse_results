#!/usr/bin/env python3
import glob
import json
import os
import pathlib

import matplotlib
import pandas as pd
from loguru import logger
from unqlite import UnQLite
import numpy as np


df = None
# from x_ana.utils import keys
keys = [
    'solver',  'instance',
    'platform', 'hostname',
    'return_code', 'cpu_time', 'wall_time', 'max_memory', 'verdict',
    'run_id', 'cpu_sys_time'
    , '#models',
    'log10_est',
    'exit',
    'tree_width',
    'projections',
    'timeout'
]


def data2csv(source, output, unqlite):
    df = pd.DataFrame(columns=keys)

    if unqlite:
        if not pathlib.Path(source).exists():
            raise RuntimeError
        db = UnQLite(source)
        collection = db.collection('data')
        if not collection.exists():
            raise RuntimeError

        i = 0

        for d in collection.all():
            if i % 500 == 0:
                logger.info(i)
            i += 1

            for k in set(d.keys()) - set(keys):
                del d[k]

            # print(d)
            df.loc[len(df)] = d
    else:
        #print("asdasdasd")
        print(source)
        for file in glob.glob(source, recursive=True):
            # json_filename = f"{os.path.dirname(file)}/result.json"
            json_filename = f"{os.path.dirname(file)}/result_nu.json"
            print(json_filename)
            with open(json_filename, "r") as fh:
                d = json.load(fh)
                print(d)

            for k in set(d.keys()) - set(keys):     # careful   # TLE - timeout
                del d[k]

            df.loc[len(df)] = d

    # print(df[df.run_id.str.contains('SAT_dat.k85.debugged.cnf') & df.run_id.str.contains('glucose')])

    logger.info(f"Write {output}")
    df.to_csv(f'{output}')
    pass

    # df.loc[df.wall_time > 1500, 'verdict'] = "TLE"
    # my version:
    # df.loc[(df['wall_time'] > 1200) & (df['verdict'] == "TLE")]
    # df[(df['verdict'] == "TLE")]
    # df[(df['verdict'] != "TLE")]
    # df.loc[df.wall_time > 1500, 'verdict'] = "TLE"
    # df[(df['wall_time'] > 1200)]

    # d1 = df[(df['verdict'] != "TLE") & (df['solver'] == 'dpdb')][['verdict','dpdb_treewidth', '#extensions']].sort_values(by=['dpdb_treewidth'])

    # d_admissible = df[(df['semantics'] == 'admissible') & (df['solver'] == 'dpdb')][['dpdb_treewidth', 'verdict']]
 #   d_stable_tle = df[(df['semantics'] == 'stable') & (df['solver'] == 'dpdb') & ((df['verdict'] == 'TLE') | (df['#extensions'] is None))][['dpdb_treewidth', 'verdict', '#extensions']]
#    d_stable_no_tle = df[(df['semantics'] == 'stable') & (df['solver'] == 'dpdb') & (df['verdict' != 'TLE']) & (df['#extensions'] is not None)][['dpdb_treewidth', 'verdict', '#extensions']]
    # d_complete = df[(df['semantics'] == 'complete') & (df['solver'] == 'dpdb')][['dpdb_treewidth', 'verdict']]
    pass





    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)