#!/usr/bin/env python3
from utils.unqlite2csv import data2csv
from utils.result_parser_json import fix_jsons
# UNQLITE_LOCATION = '../output/benchmark_results.unqlite'
OUTPUTS_LOCATION = './PAs/output_75/**/stdout.txt'
CSV_LOCTATION = 'treewidth_output_PMC_ARG_75.csv'

if __name__ == '__main__':
    # fix_jsons("../outputs/output/**/stdout.txt", 'output_argu.unqlite', rss_default='1G', hostname='taurus-haswell')
    data2csv(OUTPUTS_LOCATION, CSV_LOCTATION, unqlite=False)
