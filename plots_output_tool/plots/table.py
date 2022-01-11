import pprint

import pandas as pd

import utils as ut
import constants as ct


def table_info(df, setup_name, column_name='wall_time'):

    grouped_by_solvers = ut.group_by_solvers(df)
    grouped_by_solvers = { s: ut.get_solved_rows(s_df) for s, s_df in grouped_by_solvers.items() }

    solved_by_dpdb = grouped_by_solvers[ct.Nesthdb]

    # solved by all solvers:
    def __solved_by_all(row):
        instance_name = row['instance']
        semantics = None
        return all(not s_df[(s_df['instance'] == instance_name) ].empty for s, s_df in grouped_by_solvers.items() if s != ct.Nesthdb)

    # this surely can be done easier
    solved_by_all_instances_names_semantics_tuples = [(row['instance']) for _, row in solved_by_dpdb.iterrows() if __solved_by_all(row)]

    baseline_size = len(solved_by_all_instances_names_semantics_tuples)

    solvers_solved_by_all = { s: pd.concat([s_df[(s_df['instance'] == instance)] for instance in solved_by_all_instances_names_semantics_tuples]) for s, s_df in grouped_by_solvers.items() }

    TOP_PERCENTAGES = [1, 0.95, 0.9, 0.5]

    big_dict = { s: { f'all {len(s_df)}': { percentage: None for percentage in TOP_PERCENTAGES },
                      f'baseline {baseline_size}': { percentage: None for percentage in TOP_PERCENTAGES }
                     } for s, s_df in grouped_by_solvers.items() }

    for percentage in TOP_PERCENTAGES:
        for (s, s_df), (s_by_all, s_by_all_df) in zip(grouped_by_solvers.items(), solvers_solved_by_all.items()):

            top_percentage_s_df = ut.get_top_percentage_rows(s_df.sort_values(by=[column_name]), percentage)
            top_percentage_s_by_all_df = ut.get_top_percentage_rows(s_by_all_df.sort_values(by=[column_name]), percentage)

            all_key, baseline_key = [*big_dict[s].keys()]

            big_dict[s][all_key][percentage] = f'{top_percentage_s_df[column_name].median()}'
            big_dict[s][baseline_key][percentage] = f'{top_percentage_s_by_all_df[column_name].median()}'


    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(big_dict)


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    nesthdb_df = ut.get_solver_instances(df, ct.Nesthdb)
    clingo_df = ut.get_solver_instances(df, ct.Clingo)

  #  sharpsat_portfolio_name, sharpsat_portfolio_df = ut.create_portfolio_df(dpdb_df, sharpsat_df,ct.DPDB, ct.SharpSATU, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    #d4_portfolio_name, d4_portfolio_df = ut.create_portfolio_df(dpdb_df, d4_df, ct.DPDB,ct.D4, ct.PORTFOLIO_TREEWIDTH_LIMIT)
    #c2d_portfolio_name, c2d_portfolio_df = ut.create_portfolio_df(dpdb_df, c2d_df,ct.DPDB, ct.C2D, ct.PORTFOLIO_TREEWIDTH_LIMIT)


    #print(sharpsat_portfolio_df)
    #print(sharpsat_portfolio_name)
    df_with_portfolios = pd.concat([df])

    setup_dfs = ut.get_setup_dfs(df_with_portfolios)
   # print(setup_dfs.items())
    for setup_name, setup_df in setup_dfs.items():
        table_info(setup_df, setup_name)
        #table_info(df_with_portfolios)
        #plot_solved_wrt_difficulty(setup_df,subtitle=setup_name, show_title=True)



