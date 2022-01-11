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

import utils as ut
import constants as ct


def plot_solved_wrt_instance_domain(df, subtitle='', show_title=False):
    grouped_by_solvers = ut.group_by_solvers(df)

    # idea taken from:
    # https://stackoverflow.com/questions/28152267/how-do-i-plot-stacked-histograms-side-by-side-in-matplotlib

    width = 0.6  # the width of the bars
    extra_space = 0.05
    space_between_ranges = 1

    INPUT_TYPES_NO = len(ct.INPUT_TYPES)
    SOLVERS_NO = len(grouped_by_solvers)

    ind = np.arange(INPUT_TYPES_NO) * (SOLVERS_NO * (width + extra_space) + space_between_ranges)

    fig, ax = plt.subplots()

    for i, (solver, group_df) in enumerate(grouped_by_solvers.items()):

        solved = ut.get_solved_rows(group_df)
        unsolved = ut.get_unsolved_rows(group_df)

        solved_grouped_by_input_type = ut.group_by_input(solved)
        unsolved_grouped_by_input_type = ut.group_by_input(unsolved)

        solved_grouped_by_input_type = tuple(len(df_) for df_ in solved_grouped_by_input_type.values())
        unsolved_grouped_by_input_type = tuple(len(df_) for df_ in unsolved_grouped_by_input_type.values())

        # dirty trick: to have unsolved appear on top, sum unsolved with solved (because the last
        # graph overlaps the previous ones)
        unsolved_grouped_by_input_type = tuple(map(operator.add, solved_grouped_by_input_type, unsolved_grouped_by_input_type))

        _ = ax.bar(ind + i * (width + extra_space), unsolved_grouped_by_input_type, width, color=ct.UNSOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')
        _ = ax.bar(ind + i * (width + extra_space), solved_grouped_by_input_type, width, color=ct.SOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')


    # add some text for labels, title and axes ticks
    PLOT_TITLE = 'Solving wrt instance domain'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, subtitle))

    ax.set_xlabel('Domain')
    ax.set_ylabel('# instances')

    ax.set_xticks(ind + ((SOLVERS_NO -1) * width)/2 + extra_space )
    ax.set_xticklabels(tuple(v['name'] for v in ct.INPUT_TYPES.values()), rotation=45)

    handles = [mpatches.Patch(edgecolor='black', facecolor='white', hatch=ct.HATCHES_DICT[solver], label=solver) for solver, _ in grouped_by_solvers.items()]

    plt.legend(handles=handles, prop={'size': 12})
    plt.tight_layout()
    plt.savefig(f'1g_plot_solved_wrt_instance_domain_{subtitle}.png')
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
        plot_solved_wrt_instance_domain(setup_df,subtitle=setup_name, show_title=True)
