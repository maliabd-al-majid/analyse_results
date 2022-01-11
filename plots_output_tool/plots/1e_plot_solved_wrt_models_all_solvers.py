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

    RANGES_NO = len(ct.RANGES_MODEL)
    SOLVERS_NO = len(grouped_by_solvers)

    ind = np.arange(RANGES_NO) * (SOLVERS_NO * (width + extra_space) + space_between_ranges)

    fig, ax = plt.subplots()

    for i, (solver, group_df) in enumerate(grouped_by_solvers.items()):

        solved = ut.get_solved_rows(group_df)
        unsolved = ut.get_unsolved_rows(group_df)
        solved_within_groups = tuple(ut.get_rows_count_within_range_models(solved, range_) for range_ in ct.RANGES_MODEL)
        unsolved_within_groups = tuple(ut.get_rows_count_within_range_models(unsolved, range_) for range_ in ct.RANGES_MODEL)
        print(solver)
        print(solved_within_groups)
        # dirty trick: to have unsolved appear on top, sum unsolved with solved (because the last
        # graph overlaps the previous ones)
        unsolved_within_groups = tuple(map(operator.add, unsolved_within_groups, solved_within_groups))

        _ = ax.bar(ind + i * (width + extra_space), unsolved_within_groups, width, color=ct.UNSOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')
        _ = ax.bar(ind + i * (width + extra_space), solved_within_groups, width, color=ct.SOLVED_COLOR_BAR, hatch=ct.HATCHES_DICT[solver], edgecolor='black')


    # add some text for labels, title and axes ticks
    PLOT_TITLE = 'Solving wrt #models'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, 'by all solvers'))

    ax.set_xlabel('models range')
    ax.set_ylabel('# instances')

    ax.set_xticks(ind + ((SOLVERS_NO -1) * width)/2 + extra_space )
    ax.set_xticklabels(tuple(ut.range_to_string(range(range_.start,(range_.stop))) for range_ in ct.RANGES_MODEL), rotation=45)

    handles = [mpatches.Patch(facecolor='white', edgecolor='black', hatch=ct.HATCHES_DICT[solver], label=solver) for solver, _ in grouped_by_solvers.items()]

    plt.legend(handles=handles, prop={'size': 14})

    plt.tight_layout()
    plt.savefig(f'1e_plot_solved_wrt_models_all_solvers_{subtitle}.png')
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
    df = ut.preprocess_models(df)



    #aspartix_portfolio_name, aspartix_portfolio_df = ut.create_portfolio_df(dpdb_df, aspartix_df, ct.ASPARTIX, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    #mu_toksia_portfolio_name, mu_toksia_portfolio_df = ut.create_portfolio_df(dpdb_df, mu_toksia_df, ct.MU_TOKSIA, ct.PORTFOLIO_TREEWIDTH_LIMIT)

    df_with_portfolios = pd.concat([df])



    setup_dfs = ut.get_setup_dfs(df_with_portfolios)
    #print(setup_dfs)
    for setup_name, setup_df in setup_dfs.items():
      #  print(setup_dfs)
       # print(setup_df)
        plot_solved_wrt_treewidth_all_solvers(setup_df,subtitle=setup_name, show_title=True)
