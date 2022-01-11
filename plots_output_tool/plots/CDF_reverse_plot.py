import pandas as pd
import numpy as np
import matplotlib
import operator

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from cycler import cycler

# plt.style.use('seaborn')
matplotlib.rcParams['font.family'] = 'serif'

import constants as ct
import utils as ut


def plot_cactus_plot(df, column_name='wall_time', max_value=ct.Timeout_limit, show_title=False, subtitle=''):
    new_column_name = f'{column_name}2'
    df[new_column_name] = pd.to_numeric(df[column_name], downcast='integer')
    # set those that have more than 1000
    df.loc[df[new_column_name] >= max_value, new_column_name] = max_value

    # set those that are unsolved to max
    # df.loc[df['#models'].isnull(), new_column_name] = max_value
    df.loc[df['#models'].isnull(), new_column_name] = max_value

    grouped_by_solvers = ut.group_by_solvers(df)

    ax = None
    x = None

    for solver, group_df in grouped_by_solvers.items():
        # sort by solving time and add id
        group_df = group_df.sort_values(by=[new_column_name])
        group_df['int_index'] = range(len(group_df))

        count, bins_count = np.histogram( range(len(group_df)), bins=group_df[new_column_name])

        cdf = np.cumsum(count)



        plt.plot(bins_count[1:],cdf, label=solver, color=ct.SCATTER_COLORS_DICT[solver], marker=ct.MARKERS_DICT[solver])

    # Put more than one on single plotCDF_plot.py
     #   ax = group_df.plot(kind='scatter', x='int_index', s=20.0, y=new_column_name, color=ct.SCATTER_COLORS_DICT[solver], marker=ct.MARKERS_DICT[solver], label=solver)

    # add some text for labels, title and axes ticks
    PLOT_TITLE = 'Time needed for solving'
    plt.ylabel('# instances')
    plt.xlabel('Time [s]')
    if show_title:
        plt.title(ut.get_plot_title(PLOT_TITLE, 'by solver'))


    plt.legend()
    plt.tight_layout()
    plt.savefig(f'CDF_reversed_plot_{subtitle}.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    # dpdb_df = ut.get_solver_instances(df, ct.DPDB)
    # c2d_df = ut.get_solver_instances(df, ct.C2D)

    # add portfolio
    # c2d_30_portfolio_name, c2d_30_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df, "dpdb (width <= 30)", ct.C2D, 30)
    # c2d_35_portfolio_name, c2d_35_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df, "dpdb (width <= 35)", ct.C2D, 35)
    # c2d_40_portfolio_name, c2d_40_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df, "dpdb (width <= 40)", ct.C2D, 40)

    df_with_portfolios = pd.concat([df])

    setup_dfs = ut.get_setup_dfs(df_with_portfolios)

    for setup_name, setup_df in setup_dfs.items():
        plot_cactus_plot(setup_df, subtitle=setup_name, show_title=True)
