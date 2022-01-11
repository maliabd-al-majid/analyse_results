import pandas as pd

import matplotlib
import matplotlib.patches as mpatches

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'serif'

import constants as ct
import utils as ut


def is_nan(num):
    return num != num


def __is_solved(row):
    return not is_nan(row['#extensions']) and row['verdict'] != 'TLE'


def plot_instances_solved_scatter(df, subtitle='', show_title=False):
    """
    Plot showing what we can solve w.r.t. tree decomposition
    """

    df = df.sort_values(by=['tw'])
    df['int_index'] = range(len(df))

    df['color'] = [ct.SOLVED_COLOR_SCATTER if __is_solved(row) else ct.UNSOLVED_COLOR_SCATTER for _, row in df.iterrows()]
    # df['marker'] = ['o' if __is_solved(row) else 'x' for _, row in df.iterrows()]

    fig, ax = plt.subplots()

    ax = df.plot(kind='scatter', x='int_index', y='tw', s=5, c=df['color'], ax=ax)

    ax.set_yticks([0, 200, 400, 600, 800, 1000])
    ax.set_yticklabels(['0', '200', '400', '600', '800', '1000+'])

    PLOT_TITLE = 'Instances and treewidth'

    if show_title:
        ax.set_title(ut.get_plot_title(PLOT_TITLE, subtitle))

    ax.set_xlabel('Index')
    ax.set_ylabel('Primal treewidth')

    patch_solved = mpatches.Patch(edgecolor='black', facecolor=ct.SOLVED_COLOR_SCATTER, label='Solved')
    patch_unsolved = mpatches.Patch(edgecolor='black', facecolor=ct.UNSOLVED_COLOR_SCATTER, label='Unolved')

    plt.legend(handles=[patch_solved, patch_unsolved], prop={'size': 12})
    plt.tight_layout()

    plt.tight_layout()

    plt.savefig(f'1a_instances_solved_scatter_{subtitle}.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    dpdb_df = ut.get_solver_instances(df, ct.DPDB)
    aspartix_df = ut.get_solver_instances(df, ct.ASPARTIX)
    mu_toksia_df = ut.get_solver_instances(df, ct.MU_TOKSIA)
    d4_df = ut.get_solver_instances(df, ct.D4)

    aspartix_portfolio_name, aspartix_portfolio_df = ut.create_portfolio_df(dpdb_df, aspartix_df, ct.ASPARTIX, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    mu_toksia_portfolio_name, mu_toksia_portfolio_df = ut.create_portfolio_df(dpdb_df, mu_toksia_df, ct.MU_TOKSIA, ct.PORTFOLIO_TREEWIDTH_LIMIT)

    # plot_1a(aspartix_portfolio_df)
    df_with_portfolios = pd.concat([df, aspartix_portfolio_df, mu_toksia_portfolio_df])

    setup_dfs = ut.get_setup_dfs(df_with_portfolios)

    combined_setup = setup_dfs[ct.S_COMBINED]

    combined_dpdb = ut.get_solver_instances(combined_setup, ct.DPDB)
    combined_aspartix = ut.get_solver_instances(combined_setup, ct.ASPARTIX)
    combined_portfolio = ut.get_solver_instances(combined_setup, aspartix_portfolio_name)

    plot_instances_solved_scatter(combined_dpdb, subtitle=f'{ct.S_COMBINED}, {ct.DPDB}', show_title=True)
    plot_instances_solved_scatter(combined_aspartix, subtitle=f'{ct.S_COMBINED}, {ct.ASPARTIX}', show_title=True)
    plot_instances_solved_scatter(combined_portfolio, subtitle=f'{ct.S_COMBINED}, {aspartix_portfolio_name}', show_title=True)
