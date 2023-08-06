#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
#  pip install pandas openpyxl
import pandas as pd
import numpy as np
import re
import sys
import xlsxwriter

# https://stackoverflow.com/questions/25127673/how-to-print-utf-8-to-console-with-python-3-4-windows-8
sys.stdout.reconfigure(encoding='utf-8')

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3/28154841
import repackage
repackage.up()

from pbr.pbr_excel import *

def generate_excel(base_file, matchs,teams):
    # https://xlsxwriter.readthedocs.io/working_with_data.html
    team_members = {}
    for team in teams:
        team_members[team["name"]] = team["members"]
    print(team_members)
    excel = base_file + "-team.xlsx"
    color_pattens = [
        ("#FFC7CE", "#9C0006"),("#C6EFCE", "#006100"),("#FFEB9C", "#9C5700"),
        ("#FFCC99", "#3F3F76"),("#FFFFCC", "#000000"),("#A5A5A5", "#FFFFFF"),
        ("#FFC7CE", "#9C0006"),("#C6EFCE", "#006100"),("#FFEB9C", "#9C5700"),
    ]
    try:
        workbook = xlsxwriter.Workbook(excel)
        worksheet = workbook.add_worksheet("team")

        base_x = 0
        base_y = 0

        for group in range(MAX_MEMBERS):
            col_start=chr(ord('A') + base_y)
            col_end  =chr(ord('A') + base_y + 1)
            worksheet.set_column('%s:%s' % (col_start,col_end), 25)

                    
            cell_format  = workbook.add_format({
                'align':"center",
                'bg_color': color_pattens[group][0],
                'font_color' : color_pattens[group][1],
                'border': 1})

            worksheet.write(base_x, base_y,   "host", cell_format)
            worksheet.write(base_x, base_y+1, "guest", cell_format)

            print("====== Group %d =======" % group )
            for i in range(len(matchs)):
                hostteam, guestteam = matchs[i]
                host = team_members[hostteam][group][0]
                guest = team_members[guestteam][group][0]
                worksheet.write(base_x + 1 + i, base_y,    host,cell_format)
                worksheet.write(base_x + 1 + i, base_y+1,  guest,cell_format)
                print("%d 桌" % (i+1), host, guest)

            base_y += 2

        workbook.close()
    except xlsxwriter.exceptions.FileCreateError as e:
        print(e)
        print("Probably close the file ", excel)
    else:
        print(excel," is generated")

def generate(excel):
    print("parsing ...", excel)
    base_file = excel[:-len("xlsx")-1]
    teams = get_teams(excel)
    print(teams)
    matchs = get_matchtable(excel, "总成绩&下轮对阵")
    generate_excel(base_file,matchs,teams)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('excel', help='excel file contains team information, see sample')
    args = parser.parse_args()
    generate(args.excel)

if __name__ == '__main__':
    main()