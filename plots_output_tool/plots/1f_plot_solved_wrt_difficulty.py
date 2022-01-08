import pandas as pd
import numpy as np
import matplotlib
import operator
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from cycler import cycler

matplotlib.rcParams['font.family'] = 'serif'

import constants as ct
import utils as ut


def plot_solved_wrt_difficulty(df, subtitle='', show_title=False):
    grouped_by_solvers = ut.group_by_solvers(df)

    # idea taken from:
    # https://stackoverflow.com/questions/28152267/how-do-i-plot-stacked-histograms-side-by-side-in-matplotlib

    width = 0.6  # the width of the bars
    extra_space = 0.05
    space_between_ranges = 1

    DIFFICULTY_LEVEL_NO = len(ct.FOLDER_NAMES)
    SOLVERS_NO = len(grouped_by_solvers)

    ind = np.arange(DIFFICULTY_LEVEL_NO) * (SOLVERS_NO * (width + extra_space) + space_between_ranges)

    fig, ax = plt.subplots()

    for i, (solver, group_df) in enumerate(grouped_by_solvers.items()):
        solved = ut.get_solved_rows(group_df)
        unsolved = ut.get_unsolved_rows(group_df)

        solved_within_difficulty = tuple(len(solved[(solved['run_id'].str.contains(f'A.tar/A/{key}'))]) for key in ct.FOLDER_NAMES.keys())
        unsolved_within_difficulty = tuple(len(unsolved[(unsolved['run_id'].str.contains(f'A.tar/A/{key}'))]) for key in ct.FOLDER_NAMES.keys())

        # dirty trick: to have unsolved appear on top, sum unsolved with solved (because the last
        # graph overlaps the previous ones)
        unsolved_within_difficulty = tuple(map(operator.add, unsolved_within_difficulty, solved_within_difficulty))

        _ = ax.bar(ind + i * (width + extra_space), unsolved_within_difficulty, width, color=ct.UNSOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')
        _ = ax.bar(ind + i * (width + extra_space), solved_within_difficulty, width, color=ct.SOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')


    PLOT_TITLE = 'Solving wrt difficulty'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, subtitle))

    ax.set_xlabel('Difficulty')
    ax.set_ylabel('# instances')

    ax.set_xticks(ind + ((SOLVERS_NO -1) * width)/2 + extra_space )
    ax.set_xticklabels(tuple(ct.FOLDER_NAMES.values()), rotation=45)

    handles = [mpatches.Patch(facecolor='white', edgecolor='black', hatch=ct.HATCHES_DICT[solver], label=solver) for solver, _ in grouped_by_solvers.items()]

    plt.legend(handles=handles, prop={'size': 12})

    plt.tight_layout()
    plt.savefig(f'1f_plot_solved_wrt_difficulty_{subtitle}.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)
    # add portfolio
    dpdb_df = ut.get_solver_instances(df, ct.DPDB)
    aspartix_df = ut.get_solver_instances(df, ct.ASPARTIX)
    mu_toksia_df = ut.get_solver_instances(df, ct.MU_TOKSIA)

    aspartix_portfolio_name, aspartix_portfolio_df = ut.create_portfolio_df(dpdb_df, aspartix_df, ct.ASPARTIX, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    mu_toksia_portfolio_name, mu_toksia_portfolio_df = ut.create_portfolio_df(dpdb_df, mu_toksia_df, ct.MU_TOKSIA, ct.PORTFOLIO_TREEWIDTH_LIMIT)

    df_with_portfolios = pd.concat([df, aspartix_portfolio_df, mu_toksia_portfolio_df])

    setup_dfs = ut.get_setup_dfs(df_with_portfolios)

    for setup_name, setup_df in setup_dfs.items():
        plot_solved_wrt_difficulty(setup_df,subtitle=setup_name, show_title=True)

