import pandas as pd

import constants as ct


def group_by_input(df):
    def get_by_prefix(df_, prefix):
        if type(prefix) is list:
            return df_[(df_['instance'].str.startswith(tuple(prefix)))]
        elif prefix is None:
            prefixes = [val['prefix'] for val in ct.INPUT_TYPES.values() if val['prefix'] is not None]
            prefixes = sum([pref if type(pref) is list else [pref] for pref in prefixes], [])
            return df_[~(df_['instance'].str.startswith(tuple(prefixes)))]
        else:
            return df_[(df_['instance'].str.startswith(prefix))]

    return {key: get_by_prefix(df, val['prefix']) for key, val in ct.INPUT_TYPES.items()}


def group_by_solvers(df, semantics=None):
    grouped = df.groupby('solver')
    # print(grouped)
    grouped_by_solvers = {s: grouped.get_group(s) for s in grouped.groups}
    if semantics is None:

        #  print(grouped_by_solvers)
        return grouped_by_solvers
    else:
        #  for solver, df_ in grouped_by_solvers.items():
        #    print(solver)
        return {solver: df_ for solver, df_ in grouped_by_solvers.items()}


def get_rows_count_within_range_projections(df, range_):
    return len(df[(df['projections'] >= range_.start) & (df['projections'] <= range_.stop)].index)


def get_rows_count_within_range_models(df, range_):
    return len(df[(df['#models'] >= range_.start) & (df['#models'] <= range_.stop) & (df['verdict'] != 'TLE') & (
            pd.to_numeric(df['wall_time'], downcast='integer') <= ct.Timeout_limit)].index)


def get_rows_count_within_range(df, range_):
    return len(df[(df['tree_width'] >= range_.start) & (df['tree_width'] <= range_.stop)].index)


def range_to_string(range_):
    if range_.start>=1000000 and range_.start< 1000000000:
        if range_.stop== 1000000000:
            return f'{int((range_.start - 1) / 1000000)}Mil. - {int(range_.stop / 1000000000)}Bil.'
        else:
            return f'{int((range_.start-1)/1000000)}Mil. - {int(range_.stop/1000000)}Mil.'
    if range_.start>=1000000000:
        return f'{int((range_.start-1)/1000000000)}Bil. - {int(range_.stop/1000000000)}Bil.'
    else:
        if range_.stop == 1000000:
            return f'{range_.start}- {int(range_.stop/1000000)}Mil.'
        else:
            return f'{range_.start}- {range_.stop}'


def get_solved_rows(df):
    return df[(df['#models'].notnull()) & (df['verdict'] != 'TLE') & (df['verdict'] != 'RTE') & (
            pd.to_numeric(df['wall_time'], downcast='integer') <= ct.Timeout_limit)]


def get_unsolved_rows(df):
    return df[(df['#models'].isnull()) | (df['verdict'] == 'TLE') | (
            pd.to_numeric(df['wall_time'], downcast='integer') > ct.Timeout_limit)]


def preprocess_projection(df):
    # remove the problematic 'onebag'
    df = df[(df['tree_width'] != 'onebag')]
    df = df[df["tree_width"].notna()]
    df['projections'] = pd.to_numeric(df['projections'], downcast='integer')
    # set those that have more than 1000
    df.loc[df['projections'] >= 1000, 'projections'] = 1000
    return df





def preprocess_treewidth(df):
    # remove the problematic 'onebag'
    df = df[(df['tree_width'] != 'onebag')]
    df = df[df["tree_width"].notna()]
    df['tree_width'] = pd.to_numeric(df['tree_width'], downcast='integer')
    # set those that have more than 1000
    df.loc[df['tree_width'] >= 1000, 'tree_width'] = 1000
    return df


def preprocess_models(df):
    # remove the problematic 'onebag'
    df = df[(df['tree_width'] != 'onebag')]
    df = df[df["tree_width"].notna()]
    # set those that have more than 1000
    df.loc[df['#models'] >= 10000000000, '#models'] = 10000000000
    return df


def create_portfolio_df(dpdb_df, other_solver_df, solver_name, other_solver_name, treewidth_limit):
    portfolio_df = pd.concat(
        [dpdb_df[(dpdb_df['tree_width'] <= treewidth_limit)],
         other_solver_df[(other_solver_df['tree_width'] > treewidth_limit)]])
    portfolio_name = create_portfolio_name(solver_name, other_solver_name)
    # print(portfolio_df['wall_time'][portfolio_df['tree_width']<= treewidth_limit])
    portfolio_df = portfolio_df.assign(solver=portfolio_name)
    return portfolio_name, portfolio_df


def create_portfolio_df_projections(dpdb_df, other_solver_df, solver_name, other_solver_name, projection_limit):
    portfolio_df = pd.concat(
        [dpdb_df[(dpdb_df['projections'] <= projection_limit)],
         other_solver_df[(other_solver_df['projections'] > projection_limit)]])
    portfolio_name = create_portfolio_name(solver_name, other_solver_name)
    portfolio_df = portfolio_df.assign(solver=portfolio_name)
    return portfolio_name, portfolio_df


def create_portfolio_df_projections_models(dpdb_df, other_solver_df, solver_name, other_solver_name, projection_limit,
                                           model_limit):
    #
    portfolio_df = pd.concat(
        [dpdb_df[(dpdb_df['projections'] >= projection_limit) | dpdb_df['#models'] >= (model_limit * 1000000)],
         other_solver_df[
             (other_solver_df['projections'] <= projection_limit) | dpdb_df['#models'] < (model_limit * 1000000)]])
    portfolio_name = create_portfolio_name(solver_name, other_solver_name)
    portfolio_df = portfolio_df.assign(solver=portfolio_name)
    return portfolio_name, portfolio_df


def create_portfolio_df_treewidth_models(dpdb_df, other_solver_df, solver_name, other_solver_name, treewidth_limit,
                                         model_limit):
    portfolio_df = pd.concat(
        [dpdb_df[(dpdb_df['tree_width'] >= treewidth_limit) & (pd.to_numeric(dpdb_df['#models']) >= model_limit)],
         other_solver_df[
             (other_solver_df['tree_width'] < treewidth_limit) | ((other_solver_df['tree_width'] >= treewidth_limit) & (
                     pd.to_numeric(other_solver_df['#models']) < model_limit))]])
    portfolio_name = create_portfolio_name(solver_name, other_solver_name)
    portfolio_df = portfolio_df.assign(solver=portfolio_name)
    return portfolio_name, portfolio_df


def create_portfolio_name(solver_name, other_solver_name):
    return f'{solver_name} with {other_solver_name}'


def get_semantics_instances(df_, semantics):
    if type(semantics) is not list:
        semantics = [semantics]
    return df_[(df_['semantics'].isin(semantics))]


def get_solver_instances(df_, solver, solved_only=False, semantics=None):
    if type(solver) is not list:
        solver = [solver]
    solver_instances = df_[df_['solver'].isin(solver)]

    if semantics is not None:
        solver_instances = get_semantics_instances(solver_instances, semantics)

    if solved_only:
        return get_solved_rows(solver_instances)
    #   print(solver_instances)
    # print(solver_instances)
    return solver_instances


def get_top_percentage_rows(df_, n_):
    return df_.head(int(len(df_) * n_))


def get_plot_title(title, subtitle):
    if subtitle is not None:
        return f'{title}: {subtitle}'


def get_setup_dfs(df_with_portfolio):
    PMC_df_portfolio_name = create_portfolio_name("d4", ct.PMC)

    BE_df_portfolio_name = create_portfolio_name("d4", ct.B_E)
    dpdb_c2d_30_df_portfolio_name = create_portfolio_name("dpdb (width <= 30)", ct.C2D)
    dpdb_c2d_35_df_portfolio_name = create_portfolio_name("dpdb (width <= 35)", ct.C2D)
    dpdb_c2d_40_df_portfolio_name = create_portfolio_name("dpdb (width <= 40)", ct.C2D)
    nesthdb_clingo_tw50_df_portfolio_name = create_portfolio_name("nesthdb (treewidth <= 50)", ct.Clingo)
    nesthdb_clingo_pr50_df_portfolio_name = create_portfolio_name("nesthdb (projection <= 100)", ct.Clingo)
    nesthdb_clingo_tw20_10M_df_portfolio_name = create_portfolio_name("nesthdb (treewidth >= 20 and #model > 10M)",
                                                                      ct.Clingo)

    return {
        ct.ASP: get_solver_instances(df_with_portfolio,
                                     [ct.D4, ct.DPDB, ct.Ganak, ct.SharpSATU, ct.C2D, PMC_df_portfolio_name,
                                      BE_df_portfolio_name, dpdb_c2d_30_df_portfolio_name,
                                      dpdb_c2d_35_df_portfolio_name, dpdb_c2d_40_df_portfolio_name,
                                      ct.Nesthdb_OLD,
                                      ct.Nesthdb,
                                      ct.Clingo, nesthdb_clingo_tw50_df_portfolio_name,

                                      nesthdb_clingo_pr50_df_portfolio_name, nesthdb_clingo_tw20_10M_df_portfolio_name])
        #   ct.PMC: get_solver_instances(df_with_portfolio, PMC_df_portfolio_name),
        #   ct.B_E:get_solver_instances(df_with_portfolio, BE_df_portfolio_name),
        #  ct.SharpSATU: get_solver_instances(df_with_portfolio, ct.SharpSATU),
        #  ct.Ganak: get_solver_instances(df_with_portfolio, ct.Ganak),
        #  ct.DPDB: get_solver_instances(df_with_portfolio, ct.DPDB),
        #  ct.C2D: get_solver_instances(df_with_portfolio, ct.C2D)
    }
#  ct.S_ADMISSIBLE: get_solver_instances(df_with_portfolio, [ct.Ganak, ct.D4, ct.DPDB, PMC_df_portfolio_name]),
# ct.S_COMPLETE: get_solver_instances(df_with_portfolio, [ct.Ganak, ct.D4, ct.DPDB, ct.MU_TOKSIA, PMC_df_portfolio_name, BE_df_portfolio_name]),
# ct.S_STABLE: get_solver_instances(df_with_portfolio, [ct.Ganak, ct.D4, ct.DPDB, ct.MU_TOKSIA, PMC_df_portfolio_name, BE_df_portfolio_name]),
# ct.S_COMBINED: get_solver_instances(df_with_portfolio, [ct.Ganak, ct.D4, ct.DPDB, PMC_df_portfolio_name]),
# ct.S_COM_STAB: get_solver_instances(df_with_portfolio, [ct.Ganak, ct.D4, ct.DPDB, ct.MU_TOKSIA, PMC_df_portfolio_name, BE_df_portfolio_name])
