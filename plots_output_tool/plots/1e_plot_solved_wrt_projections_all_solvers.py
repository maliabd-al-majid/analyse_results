import pandas as pd
import numpy as np
import matplotlib
import operator
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


matplotlib.rcParams['font.family'] = 'serif'

import utils as ut
import constants as ct


def plot_solved_wrt_treewidth_all_solvers(df, subtitle='', show_title=False):
    grouped_by_solvers = ut.group_by_solvers(df)
    #print(grouped_by_solvers['tree_width'])
    #print(df)
    # idea taken from:
    # https://stackoverflow.com/questions/28152267/how-do-i-plot-stacked-histograms-side-by-side-in-matplotlib
   # print(grouped_by_solvers)
    width = 0.6  # the width of the bars
    extra_space = 0.05
    space_between_ranges = 1

    RANGES_NO = len(ct.RANGES_PROJECT)
    SOLVERS_NO = len(grouped_by_solvers)

    ind = np.arange(RANGES_NO) * (SOLVERS_NO * (width + extra_space) + space_between_ranges)

    fig, ax = plt.subplots()

    for i, (solver, group_df) in enumerate(grouped_by_solvers.items()):

        solved = ut.get_solved_rows(group_df)
        unsolved = ut.get_unsolved_rows(group_df)
        solved_within_groups = tuple(ut.get_rows_count_within_range_projections(solved, range_) for range_ in ct.RANGES_PROJECT)
        print("Solved :", solved_within_groups)
        unsolved_within_groups = tuple(ut.get_rows_count_within_range_projections(unsolved, range_) for range_ in ct.RANGES_PROJECT)
        print("unSolved :", unsolved_within_groups)
      #  print(solver)
        # dirty trick: to have unsolved appear on top, sum unsolved with solved (because the last
        # graph overlaps the previous ones)
        unsolved_within_groups = tuple(map(operator.add, unsolved_within_groups, solved_within_groups))

        _ = ax.bar(ind + i * (width + extra_space), unsolved_within_groups, width, color=ct.UNSOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')
        _ = ax.bar(ind + i * (width + extra_space), solved_within_groups, width, color=ct.SOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')


    # add some text for labels, title and axes ticks
    PLOT_TITLE = 'Solving wrt projections'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, 'by all solvers'))

    ax.set_xlabel('projections range')
    ax.set_ylabel('# instances')

    ax.set_xticks(ind + ((SOLVERS_NO -1) * width)/2 + extra_space )
    ax.set_xticklabels(tuple(ut.range_to_string(range_) for range_ in ct.RANGES_PROJECT), rotation=45)

    handles = [mpatches.Patch(facecolor='white', edgecolor='black', hatch=ct.HATCHES_DICT[solver], label=solver) for solver, _ in grouped_by_solvers.items()]

    plt.legend(handles=handles, prop={'size': 14})

    plt.tight_layout()
    plt.savefig(f'1e_plot_solved_wrt_projections_all_solvers_{subtitle}.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_projection(df)

   # nesthdb_df = ut.get_solver_instances(df, ct.Nesthdb)
   # clingo_df = ut.get_solver_instances(df, ct.Clingo)

    # add portfolio
 #   clingo_50_portfolio_name, clingo_50_portfolio_df = ut.create_portfolio_df_projections(nesthdb_df, clingo_df,
      #                                                                        "nesthdb (projection <= 100)", ct.Clingo,
            #                                                                  100)
#
    #aspartix_portfolio_name, aspartix_portfolio_df = ut.create_portfolio_df(dpdb_df, aspartix_df, ct.ASPARTIX, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    #mu_toksia_portfolio_name, mu_toksia_portfolio_df = ut.create_portfolio_df(dpdb_df, mu_toksia_df, ct.MU_TOKSIA, ct.PORTFOLIO_TREEWIDTH_LIMIT)

    df_with_portfolios = pd.concat([df])



    setup_dfs = ut.get_setup_dfs(df_with_portfolios)
    #print(setup_dfs)
    for setup_name, setup_df in setup_dfs.items():
      #  print(setup_dfs)
       # print(setup_df)
        plot_solved_wrt_treewidth_all_solvers(setup_df,subtitle=setup_name, show_title=True)
