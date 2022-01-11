import pandas as pd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'serif'

import utils as ut
import constants as ct


def plot_solved_wrt_treewidth(df, subtitle='', show_title=False):

    solved = ut.get_solved_rows(df)
    unsolved = ut.get_unsolved_rows(df)
   # print(solved)
    #print(unsolved['tree_width'])
    solved_list = [len(solved[(solved['tree_width'] >= range_.start) & (solved['tree_width'] <= range_.stop)].index)
                   for range_ in ct.RANGES]
    unsolved_list = [len(unsolved[(unsolved['tree_width'] >= range_.start) & (unsolved['tree_width'] <= range_.stop)].index)
                     for range_ in ct.RANGES]

    index = [ut.range_to_string(range_) for range_ in ct.RANGES]
    #print(index)
    df = pd.DataFrame({'Solved': solved_list, 'Unsolved': unsolved_list}, index=index)
    #print(df)
    ax = df.plot.bar(stacked=True, rot=45, color={'Solved': ct.SOLVED_COLOR_BAR, 'Unsolved': ct.UNSOLVED_COLOR_BAR}, edgecolor='black')

    PLOT_TITLE = 'Solving wrt treewidth range'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, subtitle))

    ax.set_xlabel('Treewidth range')
    ax.set_ylabel('# instances')

    plt.tight_layout()
    plt.savefig(f'1b_solved_wrt_treewidth_one_solver_{subtitle}.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    dpdb_df = ut.get_solver_instances(df, ct.DPDB)
    ganak_df = ut.get_solver_instances(df, ct.Ganak)
    sharpsatU_df = ut.get_solver_instances(df, ct.SharpSATU)
    d4_df = ut.get_solver_instances(df, ct.D4)
    pmcd4_df = ut.get_solver_instances(df, ut.create_portfolio_name(ct.D4,ct.PMC))
    bed4_df = ut.get_solver_instances(df, ut.create_portfolio_name(ct.D4,ct.B_E))
    c2d_df = ut.get_solver_instances(df, ct.C2D)

    c2d_30_portfolio_name, c2d_30_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df,"dpdb (width <= 30)", ct.C2D, 30)
    c2d_35_portfolio_name, c2d_35_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df,"dpdb (width <= 35)", ct.C2D, 35)
    c2d_40_portfolio_name, c2d_40_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df,"dpdb (width <= 40)", ct.C2D, 40)

    # plot_1b(dpdb_df)
    # plot_1b(aspartix_df)
    # plot_1b(mu_toksia_df)
    # plot_1b(d4_df)

    #aspartix_portfolio_name, aspartix_portfolio_df = ut.create_portfolio_df(dpdb_df, ganak_df, ct.Ganak, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    #mu_toksia_portfolio_name, mu_toksia_portfolio_df = ut.create_portfolio_df(dpdb_df, sharpsatU_df, ct.SharpSATU, ct.PORTFOLIO_TREEWIDTH_LIMIT)

    plot_solved_wrt_treewidth(dpdb_df, subtitle=ct.DPDB, show_title=True)
    plot_solved_wrt_treewidth(ganak_df, subtitle=ct.Ganak, show_title=True)
    plot_solved_wrt_treewidth(sharpsatU_df, subtitle=ct.SharpSATU, show_title=True)
    plot_solved_wrt_treewidth(d4_df, subtitle=ct.D4, show_title=True)
    plot_solved_wrt_treewidth(pmcd4_df, subtitle=ut.create_portfolio_name(ct.D4,ct.PMC), show_title=True)
    plot_solved_wrt_treewidth(bed4_df, subtitle=ut.create_portfolio_name(ct.D4,ct.B_E), show_title=True)
    plot_solved_wrt_treewidth(c2d_df, subtitle=ct.C2D, show_title=True)
    plot_solved_wrt_treewidth(c2d_30_portfolio_df, subtitle=c2d_30_portfolio_name, show_title=True)
    plot_solved_wrt_treewidth(c2d_35_portfolio_df, subtitle=c2d_35_portfolio_name, show_title=True)
    plot_solved_wrt_treewidth(c2d_40_portfolio_df, subtitle=c2d_40_portfolio_name, show_title=True)
