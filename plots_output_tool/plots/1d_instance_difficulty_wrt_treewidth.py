"""Treewidth / Instance difficulty"""

import pandas as pd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from cycler import cycler

matplotlib.rcParams['font.family'] = 'serif'

import utils as ut
import constants as ct

# TODO: set nicer colour cycles
plt.rc('axes', prop_cycle=(cycler('color', ct.DIFFICULTY_COLORS)))


def plot_instance_difficulty_wrt_treewidth(df, show_title=False):

    grouped = {
        val: [ut.get_rows_count_within_range(df[(df['run_id'].str.contains(f'A.tar/A/{key}'))], range_) for range_ in ct.RANGES] for key, val in ct.FOLDER_NAMES.items()
    }

    index = [ut.range_to_string(range_) for range_ in ct.RANGES]

    df = pd.DataFrame(grouped, index=index)
    ax = df.plot.bar(stacked=True, rot=45, edgecolor='black')

    PLOT_TITLE = 'Instance difficulty'

    if show_title:
        ax.set_title(PLOT_TITLE)

    ax.set_xlabel('Treewidth range')
    ax.set_ylabel('# instances')

    plt.tight_layout()
    plt.savefig('1d_instance_difficulty_wrt_treewidth.png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv(ct.CSV_NAME)
    df = ut.preprocess_treewidth(df)

    dpdb_df = ut.get_solver_instances(df, ct.DPDB)

    plot_instance_difficulty_wrt_treewidth(dpdb_df, show_title=True)
