#!/usr/bin/env python3
import codecs
import glob
import json
import os
import re
import pathlib

import numpy as np
from loguru import logger

import Constant

DPDB_SOLVER = 'nesthdb'

# from x_ana_mcc2020.util import keys
# TODO: keys
keys = [
    'solver',  'instance',
    'platform', 'hostname',
    'return_code', 'cpu_time', 'wall_time', 'max_memory', 'verdict',
    'run_id', 'cpu_sys_time'
    , '#models',
    'log10_est',
    'exit',
    'tree_width',
    'projections',
    'timeout'

]

err_patterns = {"User time (seconds):": "cpu_time",
                "System time (seconds):": "cpu_sys_time",
                "Elapsed (wall clock) time (h:mm:ss or m:ss):": "wall_time",
                "Maximum resident set size (kbytes):": "max_memory",
                "Exit status:": "runsolver_STATUS"
                }
std_patterns = {"Exit code=": "runsolver_STATUS"}
var_patterns = {"RETCODE": "return_code",
                "SIGNAL": "signal",
                "WCTIME": "wall_time",
                "CPUTIME": "cpu_time",
                "USERTIME": "cpu_user_time",
                "SYSTEMTIME": "cpu_sys_time",
                "CPUUSAGE": "cpu_usage",
                "MAXVM": "max_memory",
                "TIMEOUT": "timeout",
                "MEMOUT": "memout"
                }


def extract_data(stream, d, delimn, patterns):
    for line in stream.readlines():
        for p, k in patterns.items():
            n = line.find(p)
            if n != -1:
                m = line.rfind(delimn)
                if m == -1:
                    continue
                if delimn == ":":
                    d[k] = float(line[m + 2:])
                elif delimn == "=":
                    try:
                        d[k] = float(line[m + 1:])
                    except ValueError:
                        d[k] = line[m + 1:-1]
                else:
                    raise NotImplementedError


solver_re = {
    "dpdb":
        {
            # get the treewidth from:
            # [INFO] dpdb: #bags: 749 tree_width: 3 #vertices: 1000 #leafs: 3 #edges: 748
            # '[INFO] asp2sat: Tree decomposition #bags: 8287 tree_width: 418 #vertices: 10337 #leafs: 583 #edges: 8286'
            # [INFO] asp2sat: Tree decomposition #bags:
            'tree_width': (int, re.compile(
                r'\[INFO]\s*asp2sat:\s*Tree\s*decomposition\s*#bags:\s*\d+\s*tree_width:\s(?P<val>\d+)\s*.*$')),
            # [INFO] dpdb.problems.ce_admissible2: Problem has 1500 admissible sets
            # [INFO] dpdb.problems.sharpsat: Problem has
            '#models': (
                int, re.compile(r'\[INFO]\s*dpdb\.problems\.sharpsat:\s*Problem\s*has\s*(?P<val>\d+)\s*.*$')),
            'exit': (int, re.compile(r".*Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },

    "nesthdb":
        {
            # get the treewidth from:
            # [INFO] dpdb: #bags: 749 tree_width: 3 #vertices: 1000 #leafs: 3 #edges: 748
            # '[INFO] asp2sat: Tree decomposition #bags: 8287 tree_width: 418 #vertices: 10337 #leafs: 583 #edges: 8286'
            # [INFO] asp2sat: Tree decomposition #bags:
            #[INFO] nestHDB: original tree_width: 5
            'tree_width': (int, re.compile(
                r'\[INFO]\s*nestHDB:\s*Original\s*tree_width:\s*(?P<val>\d+)\s*.*$')),
            #[INFO] nestHDB: projections: 6
            #[INFO] nestHDB: Original projections: 1000
            'projections': (int, re.compile(
                r'\[INFO]\s*nestHDB:\s*Original\s*projections:\s*(?P<val>\d+)\s*.*$')),
            # [INFO] nestHDB: Original #atoms: 110, #rules: 184, #projected: 32, depth: 0
            # [INFO] dpdb.problems.ce_admissible2: Problem has 1500 admissible sets
            # [INFO] dpdb.problems.sharpsat: Problem has
            # [INFO] dpdb.problems.nestpmc: Problem has
            #[INFO] nestHDB: PMC:
            '#models': (
                int, re.compile(r'\[INFO]\s*nestHDB:\s*PMC:\s*(?P<val>\d+)\s*.*$')),
            'exit': (int, re.compile(r".*Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "clingo":
        {
            # get the treewidth from:
            # [INFO] dpdb: #bags: 749 tree_width: 3 #vertices: 1000 #leafs: 3 #edges: 748
            # '[INFO] asp2sat: Tree decomposition #bags: 8287 tree_width: 418 #vertices: 10337 #leafs: 583 #edges: 8286'
            # [INFO] asp2sat: Tree decomposition #bags:
            # Models       : 32769
            # [INFO] dpdb.problems.ce_admissible2: Problem has 1500 admissible sets
            # [INFO] dpdb.problems.sharpsat: Problem has
            #
            '#models': (
                int, re.compile(r'Models\s*:\s(?P<val>\d+)\s*.*$')),
            'exit': (int, re.compile(r".*Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "dpdbSAT":
        {
            # get the treewidth from:
            # [INFO] dpdb: #bags: 749 tree_width: 3 #vertices: 1000 #leafs: 3 #edges: 748
            # '[INFO] asp2sat: Tree decomposition #bags: 8287 tree_width: 418 #vertices: 10337 #leafs: 583 #edges: 8286'
            # [INFO] dpdb: #bags: 2534 tree_width: 402 #vertices: 3947 #leafs: 1011 #edges: 2533
            'tree_width': (int, re.compile(
                r'\[INFO]\s*dpdb:\s*#bags:\s*\d+\s*tree_width:\s(?P<val>\d+)\s*.*$')),
            # [INFO] dpdb.problems.ce_admissible2: Problem has 1500 admissible sets
            # [INFO] dpdb.problems.sharpsat: Problem has
            '#models': (
                int, re.compile(r'\[INFO]\s*dpdb\.problems\.sharpsat:\s*Problem\s*has\s*(?P<val>\d+)\s*.*$')),
            'exit': (int, re.compile(r".*Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "dpdbCP":
        {
            # get the treewidth from:
            # [INFO] dpdb: #bags: 749 tree_width: 3 #vertices: 1000 #leafs: 3 #edges: 748
            # '[INFO] asp2sat: Tree decomposition #bags: 8287 tree_width: 418 #vertices: 10337 #leafs: 583 #edges: 8286'
            'tree_width': (int, re.compile(
                r'\[INFO]\s*asp2sat:\s*Tree\s*decomposition\s*#bags:\s*\d+\s*tree_width:\s(?P<val>\d+)\s*.*$')),
            # [INFO] dpdb.problems.ce_admissible2: Problem has 1500 admissible sets
            # [INFO] dpdb.problems.sharpsat: Problem has
            '#models': (
                int, re.compile(r'\[INFO]\s*dpdb\.problems\.sharpsat:\s*Problem\s*has\s*(?P<val>\d+)\s*.*$')),
            'exit': (int, re.compile(r".*Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },

    "c2d":
        {
            "#models": (int, re.compile(r"^\s*Counting\.*\s*(?P<val>\d+).*$")),
            "exit": (int, re.compile(r".*Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "bed4":
        {

            "log10_est": (
                float, re.compile(r"^c\s+s\s+log10-estimate\s+(?P<val>([-+]?([0-9]*[.])?[0-9]+([eE][-+]?\d+)?))")),
            "#models": (int, re.compile(r"^c\s+s\s+exact\s+arb\s+int\s*(?P<val>(\d*\.\d+)|(\d+)|(\d*\.\d+e[-+]\d+))\s*$")),
            "exit": (int, re.compile(r"^Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "pmcd4":
        {

            "log10_est": (
                float, re.compile(r"^c\s+s\s+log10-estimate\s+(?P<val>([-+]?([0-9]*[.])?[0-9]+([eE][-+]?\d+)?))")),
            "#models": (int, re.compile(r"^c\s+s\s+exact\s+arb\s+int\s*(?P<val>(\d*\.\d+)|(\d+)|(\d*\.\d+e[-+]\d+))\s*$")),
            "exit": (int, re.compile(r"^Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "d4":
        {

            "log10_est": (
                float, re.compile(r"^c\s+s\s+log10-estimate\s+(?P<val>([-+]?([0-9]*[.])?[0-9]+([eE][-+]?\d+)?))")),
            "#models": (int, re.compile(r"^c\s+s\s+exact\s+arb\s+int\s*(?P<val>(\d*\.\d+)|(\d+)|(\d*\.\d+e[-+]\d+))\s*$")),
            "exit": (int, re.compile(r"^Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "unweighted":
    # c s log10-estimate 0.6989700043360189
        {
            "#models": (int, re.compile(r"^c\s+s\s+(approx|exact)\s+(arb|single|double|quadruple)\s+"
                                        r"(int|log10|prec-sci|float)\s+"
                                        r"(?P<val>([-+]?([0-9]*[.])?[0-9]+([eE][-+]?\d+)?))")),
            "log10_est": (

                float, re.compile(r"^c\s+s\s+log10-estimate\s+(?P<val>([-+]?([0-9]*[.])?[0-9]+([eE][-+]?\d+)?))")),
            # "#models": (int, re.compile(r"^\s*(?P<val>\d+)\s*$")),
            "exit": (int, re.compile(r"^Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    "ganak":
        {
            "#models": (int, re.compile(r"^s\s+mc\s*(?P<val>\d+)\s*$")),
            "exit": (int, re.compile(r"^Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
        },
    # "cachet":
    #     {
    #         "#models": (int, re.compile(r"^\s*s\s*(?P<val>\d*\.\d+|\d+|\d*\.\d+e[-+]\d+)\s*$")),
    #         "#lit": (float, re.compile(r"^\s*Original Num Literals\s*(?P<val>\d*\.\d+|\d+|\d*\.\d+e[-+]\d+)\s*$")),
    #         "#clauses": (float, re.compile(r"^\s*Original Num Clauses\s*(?P<val>\d*\.\d+|\d+|\d*\.\d+e[-+]\d+)\s*$")),
    #         "#var": (float, re.compile(r"^\s*Number of Variables\s*(?P<val>\d*\.\d+|\d+|\d*\.\d+e[-+]\d+)\s*$")),
    #         "#desicions": (float, re.compile(r"^\s*Number of Decisions\s*(?P<val>\d*\.\d+|\d+|\d*\.\d+e[-+]\d+)\s*$")),
    #         "infinite": (str, re.compile(r"^\s*s\s*(?P<val>inf)\s*$")),
    #         "exit": (int, re.compile(r"^Solver\sfinished\swith\sexit\scode=(?P<val>\d+)")),
    #     },

}


def extract_solver(stream, d, solver):
    for line in stream.readlines():
        for val, reg in solver_re[solver].items():

            m = reg[1].match(line)
            if m:
                # Here specify solver specific
                # in the tuple are general
                key = f'{solver}_{val}' if val not in ('exit', 'tree_width', '#models','projections') else f"{val}"
                d[key] = reg[0](m.group("val"))


# folder = f'../output_mcc2020_classification_all/number_sat/*/track1_mc/**/stdout.txt'
# folder = f'../output_mcc2020_classification_all/number_sat/**/stdout.txt'
folder_stdout = f'{Constant.output_path}/**/stdout.txt'
folder_stderr = f'{Constant.output_path}/**/stdout.txt'
# solver_name_re = re.compile(r"default\[s=(?P<solver>([\w.-]+))(,[\w]*)*\]")
SOLVER_SEMANTICS_RE = re.compile(r'default\[a=(?P<semantics>([\w.-]+)),s=(?P<solver>[\w]+).*\]')

for file in glob.glob(folder_stdout, recursive=True):
    print(f'file: {file}')
    logger.trace(f"file: {file}")
    # solver = re.findall(solver_name_re, file)[0][0]
    semantics, solver = list(dict.fromkeys(re.findall(SOLVER_SEMANTICS_RE, file)[0]))
    if solver == DPDB_SOLVER:
        continue
    dirname = os.path.dirname(file)
    d = {key: np.nan for key in keys}
    d.update({"run_id": dirname[3:], "wall_time": "nan", "cpu_sys_time": "nan", "cpu_time": "nan",
              "verdict": "RTE", "return_code": 9,
              'platform': 'Linux-3.10.0-1062.12.1.el7.x86_64-x86_64-with-redhat-7.7-Maipo',
              'hostname': 'missing',
              "runsolver_STATUS": 9, "runsolver_TIMEOUT": 0, "runsolver_MEMOUT": 0, "max_memory": "nan"})

    # setting solver & semantics manually
    d['solver'] = solver
    if semantics == 1:
        d['semantics'] = "ASP"
    d['instance'] = pathlib.Path(file).parent.parent.stem

    with open(file, 'r') as stdout_p:

        extract_solver(stream=stdout_p, d=d, solver=solver)
    with codecs.open(f"{file[:-7]}err.txt", mode='r', errors='ignore', encoding='utf-8') as stderr_p:
        # with open(f"{file[:-7]}err.txt", 'r') as stderr_p:
        extract_data(stream=stderr_p, d=d, delimn=":", patterns=err_patterns)
    try:
        with open(f"{file[:-10]}varfile.txt", 'r') as var_p:
            extract_data(stream=var_p, d=d, delimn="=", patterns=var_patterns)
        logger.trace(d)
        try:
            if d['signal'] in (0,):
                d["verdict"] = "OK"
            if d['signal'] in (9, 15) or d['exit'] == 143:
                d["verdict"] = "RTE"
            if d['exit'] == 139:
                d["verdict"] = "MEM"
            if d['timeout'] == 'true':
                d["verdict"] = "TLE"
            elif d['memout'] == 'true':
                d["verdict"] = "MEM"

            # else:
            #     logger.error(d)
            #     raise NotImplementedError
        except KeyError as e:
            logger.error(f"{file}")
            #raise RuntimeError
    except FileNotFoundError as e:
        logger.info(f"Missing varfile for file {file}")
        # TODO:
        # MEMOUT = "MEM"
        # RUNTIME_ERR = "RTE"
        # OUTPUT_LIMIT = "OLE"

    try:
        with open(f"{dirname}/result.json", "r", encoding="utf-8") as fh_read:
            d2 = json.load(fh_read)
    except json.decoder.JSONDecodeError:
        d2 = {}

    d2.update(d)
    with open(f"{dirname}/result_nu.json", "w", encoding="utf-8") as fh:
        json.dump(d2, fh, ensure_ascii=False, indent=4)

# FOR DPDB ONLY

for file in glob.glob(folder_stderr, recursive=True):
    logger.trace(f"file: {file}")
    semantics, solver = list(dict.fromkeys(re.findall(SOLVER_SEMANTICS_RE, file)[0]))
    # solver = re.findall(solver_name_re, file)[0][0]
    if solver != DPDB_SOLVER:
        continue
    dirname = os.path.dirname(file)
    d = {key: np.nan for key in keys}
    d.update({"run_id": dirname[3:], "wall_time": "nan", "cpu_sys_time": "nan", "cpu_time": "nan",
              "verdict": "RTE", "return_code": 9,
              'platform': 'Linux-3.10.0-1062.12.1.el7.x86_64-x86_64-with-redhat-7.7-Maipo',
              'hostname': 'missing',
              "runsolver_STATUS": 9, "runsolver_TIMEOUT": 0, "runsolver_MEMOUT": 0, "max_memory": "nan"})

    # setting solver & semantics manually
    d['solver'] = solver
    if semantics == 1:
        d['semantics'] = "ASP"

    d['instance'] = pathlib.Path(file).parent.parent.stem

    with open(file, 'r') as stdout_p:
        extract_solver(stream=stdout_p, d=d, solver=solver)
    with codecs.open(f"{file[:-7]}err.txt", mode='r', errors='ignore', encoding='utf-8') as stderr_p:
        # with open(f"{file[:-7]}err.txt", 'r') as stderr_p:
        extract_solver(stream=stderr_p, d=d, solver=solver)
        extract_data(stream=stderr_p, d=d, delimn=":", patterns=err_patterns)
    try:
        with open(f"{file[:-10]}varfile.txt", 'r') as var_p:
            extract_data(stream=var_p, d=d, delimn="=", patterns=var_patterns)
        logger.trace(d)
        try:
            if d['signal'] in (0,):
                d["verdict"] = "OK"
            if d['signal'] in (9, 15) or d['exit'] == 143:
                d["verdict"] = "RTE"
            elif d['exit'] == 139:
                d["verdict"] = "MEM"
            if d['timeout'] == 'true':
                d["verdict"] = "TLE"
            elif d['memout'] == 'true':
                d["verdict"] = "MEM"

            # else:
            #     logger.error(d)
            #     raise NotImplementedError
        except KeyError as e:
            logger.error(f"{file}")
    #     raise RuntimeError
    except FileNotFoundError as e:
        logger.info(f"Missing varfile for file {file}")
        # TODO:
        # MEMOUT = "MEM"
        # RUNTIME_ERR = "RTE"
        # OUTPUT_LIMIT = "OLE"

    try:
        with open(f"{dirname}/result.json", "r", encoding="utf-8") as fh_read:
            d2 = json.load(fh_read)
    except json.decoder.JSONDecodeError:
        d2 = {}

    d2.update(d)
    with open(f"{dirname}/result_nu.json", "w", encoding="utf-8") as fh:
        json.dump(d2, fh, ensure_ascii=False, indent=4)
