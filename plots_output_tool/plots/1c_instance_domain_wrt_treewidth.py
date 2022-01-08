import pandas as pd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from cycler import cycler

matplotlib.rcParams['font.family'] = 'serif'

import constants as ct
import utils as ut

plt.rc('axes', prop_cycle=(cycler('color', ct.BAR_COLORS)))


def plot_instance_domain_wrt_treewidth(df, show_title=False):

    grouped = ut.group_by_input(df)

    instances_dict = { ct.INPUT_TYPES[key]['name']: [ut.get_rows_count_within_range(group_df, range_) for range_ in ct.RANGES] for key, group_df in grouped.items() }

    index = [ut.range_to_string(range_) for range_ in ct.RANGES]

    df = pd.DataFrame(instances_dict, index=index)
    ax = df.plot.bar(stacked=True, rot=45, edgecolor='black')

    PLOT_TITLE = 'Instance domain'

    if show_title:
        ax.set_title(PLOT_TITLE)

    ax.set_xlabel('Treewidth range')
    ax.set_ylabel('# instances')

    plt.tight_layout()
    plt.savefig('1c_instance_domain_wrt_treewidth.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    dpdb_df = ut.get_solver_instances(df, ct.DPDB)

    plot_instance_domain_wrt_treewidth(dpdb_df, show_title=True)
