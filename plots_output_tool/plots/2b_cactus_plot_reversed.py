import pandas as pd
import numpy as np
import matplotlib
import operator

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from cycler import cycler

# plt.style.use('seaborn')
matplotlib.rcParams['font.family'] = 'serif'

import constants as ct
import utils as ut


def plot_cactus_plot_inversed(df, column_name='wall_time', max_value=ct.Timeout_limit, show_timed_out=True, show_title=False,
                              subtitle=''):
    new_column_name = f'{column_name}2'
    df[new_column_name] = pd.to_numeric(df[column_name], downcast='integer')
    # set those that have more than 1000
    df.loc[df[new_column_name] >= max_value, new_column_name] = max_value

    # set those that are unsolved to max
    #df.loc[df['#models'].isnull(), new_column_name] = max_value
    df.loc[df['#models'].isnull(), new_column_name] = max_value
    grouped = df.groupby('solver')
  #  print(df)
   # print(grouped)
    if not show_timed_out:
        df = df[(df[new_column_name] < max_value)]

    grouped_by_solvers = ut.group_by_solvers(df)

    ax = None

    for solver, group_df in grouped_by_solvers.items():
        # sort by solving time and add id
        group_df = group_df.sort_values(by=[new_column_name])
        group_df['int_index'] = range(len(group_df))

        # Put more than one on single plot
        ax = group_df.plot(kind='scatter', y='int_index', x=new_column_name, s=20.0,
                           color=ct.SCATTER_COLORS_DICT[solver], marker=ct.MARKERS_DICT[solver], ax=ax, label=solver)

    PLOT_TITLE = 'Time needed for solving'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, 'by solver'))

    ax.set_ylabel('# instances')
    ax.set_xlabel('Time [s]')

    ax.legend()

    plt.tight_layout()
    plt.savefig(f'2b_cactus_plot_reversed_{subtitle}.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME_all_in)
    #df_25 = pd.read_csv(ct.CSV_NAME_100)
    #df_50 = pd.read_csv(ct.CSV_NAME_50)
    #df_75 = pd.read_csv(ct.CSV_NAME_75)
    #df_100 = pd.read_csv(ct.CSV_NAME_100)
    #df_25 = df_25[df_25['projections'] == 100]
    #df_50 =df_50[df_50['projections']==50]
    #df_75 =df_75[df_75['projections']==75]
    #df_100 =df_100[df_100['projections']==100]
    #df =pd.concat([df_50,df_75,df_100])
    #df = ut.preprocess_treewidth(df_25)

    df = ut.preprocess_treewidth(df)
    df = ut.preprocess_projection(df)




    df_with_portfolios = pd.concat([df])



    setup_dfs = ut.get_setup_dfs(df_with_portfolios)

    for setup_name, setup_df in setup_dfs.items():
        plot_cactus_plot_inversed(setup_df, subtitle=setup_name, show_title=True)
