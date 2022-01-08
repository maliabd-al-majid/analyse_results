CSV_NAME = './PAs/PMC_ARG_100_treewidth.csv'

BINS = [0, 20, 40, 50, 100, 200, 500, 1000]
BINS_project = [0, 20, 40, 50, 100, 200, 500, 1000]
BINS_models = [0, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
Timeout_limit = 1600
PORTFOLIO_TREEWIDTH_LIMIT = 50

RANGES = [range(bin + 1, BINS[i + 1]) for i, bin in enumerate(BINS) if i < len(BINS) - 1]
RANGES_PROJECT = [range(bin + 1, BINS_project[i + 1]) for i, bin in enumerate(BINS_project) if
                  i < len(BINS_project) - 1]
RANGES_MODEL = [range((bin * 1000) + 1, (BINS_models[i + 1]) * 1000) for i, bin in enumerate(BINS_models) if
                i < len(BINS_models) - 1]
RANGES_MODEL_PlOT = [range((bin * 1000) + 1, (BINS_models[i + 1]) * 1000) for i, bin in enumerate(BINS_models) if
                     i < len(BINS_models) - 1]
# DIFFICULTY_COLORS = ['#CEDEA3', '#DDDEA3', '#DED0A3', '#DEC2A3', '#DEA5A4']
DIFFICULTY_COLORS = ['#CEDEA3', '#DDDEA3', '#DED0A3', '#DEA5A4', '#DD6961']

BAR_COLORS = ['#FFB5E8', '#B28DFF', '#DCD3FF', '#AFF8D8', '#6EB5FF', '#FFFFD1', '#FFABAB', '#2E3332', '#CCADB2',
              '#FF6961', '#EAB159']

SOLVED_COLOR_SCATTER = 'green'
UNSOLVED_COLOR_SCATTER = 'red'

SOLVED_COLOR_BAR = '#AFF8D8'  # '#BFFCC6' # '#B7BF5E'
UNSOLVED_COLOR_BAR = '#FFABAB'  # '#C36F31'

DPDB = 'dpdb'
Nesthdb = 'nesthdb'
Nesthdb_OLD = 'nesthdb_old'
SharpSATU = 'SharpSATU'
Clingo = 'clingo'
D4 = 'd4'
Ganak = 'ganak'
C2D = 'c2d'
PMC = 'pmc'
B_E = 'B+E'

# '-', '+', 'x', '\\', '*', 'o', 'O', '.'

HATCHES_DICT = {
    DPDB: '',
    Nesthdb: '',
    SharpSATU: '..',
    Clingo: '..',
    D4: '\\\\',
    Nesthdb_OLD: '\\\\',
    Ganak: 'OO',
    C2D: '++',
    'd4 with pmc': '//',
    'd4 with B+E': '+x',
    'dpdb (width <= 30) with c2d': '*/',
    'dpdb (width <= 35) with c2d': 'o-',
    'dpdb (width <= 40) with c2d': 'o+*',
    'nesthdb (treewidth <= 50) with clingo': '++',
    'nesthdb (projection <= 100) with clingo': 'OO',
    'nesthdb (treewidth >= 20 and #model > 10M) with clingo': '+x'
}

SCATTER_COLORS_DICT = {
    DPDB: '#6EB5FF',
    Nesthdb: '#6EB5FF',
    SharpSATU: '#B28DFF',
    Clingo: '#B28DFF',
    D4: '#AFF8D8',
    Nesthdb_OLD: '#AFF8D8',
    Ganak: '#612700',
    C2D: '#FF6A06',
    'd4 with pmc': '#CCADB2',
    'd4 with B+E': '#EAB159',
    'dpdb (width <= 30) with c2d': '#CDABCD',
    'dpdb (width <= 35) with c2d': '#DFBBCD',
    'dpdb (width <= 40) with c2d': '#FBBCDE',
    'nesthdb (treewidth <= 50) with clingo': '#CDABCD',
    'nesthdb (projection <= 100) with clingo': '#612700',
    'nesthdb (treewidth >= 20 and #model > 10M) with clingo': '#DFBBCD'
}

MARKERS_DICT = {
    DPDB: '1',
    Nesthdb: '1',
    SharpSATU: '*',
    Clingo: '*',
    D4: '+',
    Nesthdb_OLD: '+',
    Ganak: 'x',
    C2D: 's',
    'd4 with pmc': 'p',
    'd4 with B+E': 'd',
    'dpdb (width <= 30) with c2d': '2',
    'dpdb (width <= 35) with c2d': '3',
    'dpdb (width <= 40) with c2d': '4',
    'nesthdb (treewidth <= 50) with clingo': '2',
    'nesthdb (projection <= 100) with clingo': '3',
    'nesthdb (treewidth >= 20 and #model > 10M) with clingo': '4'
}

SCATTER_COLORS = ['#6EB5FF', '#B28DFF', '#AFF8D8', '#612700', '#FF6A06', '#EAB159']

MARKERS_CYCLE = ['1', '*', '+', 'x', '<', '>', 's', 'p', 'P', '2', '3', '4', '8', '*', 'h', 'H', 'X', 'D', 'd', '.',
                 'o', 'v', '^', '<', '>', 's', 'p', 'P']

# SETUPS
# S_ADMISSIBLE = 'S. admissible'
# S_COMPLETE = 'S. complete'
ASP = 'ASP'
# S_COMBINED = 'S. combined'
# S_COM_STAB = 'S. com+stab'


# semantics
# ADMISSIBLE = 'admissible'
# COMPLETE = 'complete'
# STABLE = 'stable'

FOLDER_NAMES = {
    1: 'very easy',
    2: 'easy',
    3: 'medium',
    4: 'hard',
    5: 'too hard'
}
#
INPUT_TYPES = {
    'aba2af': {
        'prefix': 'afinput',
        'name': 'ABA2AF'
    },
    'admbuster': {
        'prefix': 'admbuster',
        'name': 'AdmBuster'
    },
    'barabasi': {
        'prefix': 'BA',
        'name': 'Barabasi-Albert'
    },
    'erdos': {
        'prefix': 'ER',
        'name': 'Erdös-Renyi'
    },
    'grounded_gen': {
        'prefix': 'grd',
        'name': 'GroundedGenerator'
    },
    'planning_2_af': {
        'prefix': ['bw2', 'bw3', 'ferry2'],
        'name': 'Planning2AF'
    },
    'scc_gen': {
        'prefix': 'scc',
        'name': 'SccGenerator'
    },
    'sem_buster': {
        'prefix': 'sembuster',
        'name': 'SemBuster'
    },
    'stable_gen': {
        'prefix': 'stb',
        'name': 'StableGenerator'
    },
    'traffic': {
        'prefix': None,
        'name': 'Traffic'
    },
    'watts_strogatz': {
        'prefix': 'WS',
        'name': 'Watts-Strogatz'
    }
}
