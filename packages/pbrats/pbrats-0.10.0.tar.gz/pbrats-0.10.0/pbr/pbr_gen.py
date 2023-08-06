#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
#  pip install pandas openpyxl
import pandas as pd
import numpy as np
import re
import sys

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3/28154841
import repackage
repackage.up()

from pbr.pbr_excel import *

# https://stackoverflow.com/questions/25127673/how-to-print-utf-8-to-console-with-python-3-4-windows-8
sys.stdout.reconfigure(encoding='utf-8')


def generate_excel(teams):
    print(teams)
    #for i in range(MAX_MEMBERS):
    groups = [[]*MAX_ROUNDS]*MAX_MEMBERS
    print(groups)
    team_names = []
    for team in teams:
        print(team)
        for i in range(MAX_MEMBERS):
            #print(team["members"][i][0])
            # use copy !!
            group = groups[i].copy()
            group.append(team["members"][i][0])
            groups[i] = group
            #print(groups)
        team_names.append(team["name"])
    for idx, group in enumerate(groups):
        print("group: ", idx+1, group)
        df = pd.DataFrame([[''] * MAX_ROUNDS ] * len(teams),
                    index=[team_names,group],
                    columns=list(range(1, MAX_ROUNDS+1)))
        print(idx, type(idx))
        excel = "202106-record-group%d.xlsx" % (idx+1)
        df.to_excel( excel, sheet_name='0601',  index_label=["team","id"])

def generate(excel):
    print("parsing ...", excel)
    teams = get_teams(excel)
    # print(teams)
    generate_excel(teams)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('excel', help='excel file contains team information, see sample')
    args = parser.parse_args()
    generate(args.excel)

if __name__ == '__main__':
    main()