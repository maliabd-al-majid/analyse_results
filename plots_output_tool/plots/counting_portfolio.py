import pandas as pd
import pprint

import constants as ct
import utils as ut


def analyse(df, tw_limit, semantics=None):
    ###
    grouped_by_solvers = ut.group_by_solvers(df, semantics=semantics)

    dpdb_df = grouped_by_solvers[ct.Nesthdb]

    SECOND_PORTFOLIO_SOLVERS = [ct.Clingo]

    portfolio_name_df_tuples = [ ut.create_portfolio_df(dpdb_df, grouped_by_solvers[solver],ct.Nesthdb, solver, tw_limit) for solver in SECOND_PORTFOLIO_SOLVERS]

    return { s: len(ut.get_solved_rows(s_df)) for s, s_df in portfolio_name_df_tuples }


if __name__ == '__main__':
    # initialize

    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    semantics = None   # change accorgingly
    initial_tw = 0
    max_tw =200
    best_for_each_solver = { k: (initial_tw, v) for k, v in analyse(df, initial_tw, semantics).items() }

    for i in range(initial_tw, max_tw):
        result_dict = analyse(df, i, semantics)  # change accordingly
        for port, number in result_dict.items():

            if best_for_each_solver[port][1] < number:
                best_for_each_solver[port] = (i, number)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(best_for_each_solver)

    # RESULTS:
    # (dpdb)+ aspartix | d4     | mu_toksia
    # ALL:
    #     16: 802=(19:802) | 0: 670 (19: 652)   | +19: 676 (dla 16: 672)      (treewidth: #solved instances)
    # ADMISSIBLE:
    #     16:230 +(19: 231) | 0: 196 (16: 190?!) | 99: 100 (16: 93)
    # COMPLETE:
    #     +16: 266 (19:265) | 0: 217 (19: 211)   | +19: 272 (16:271)
    # STABLE
    #     16: 306 +(19:307) | 0: 257             | 18: 309 +(19:309) (16:308)

    # SO:
    # dpdb+asp 16/19
    # dpdb+mu_toksia 19
