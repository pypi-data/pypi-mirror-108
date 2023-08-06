#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  pip install pandas openpyxl
import pandas as pd
import re

TOTAL_BOARDS=8 # later can be 12
BOARD_ABORT="ABORT"
BOARD_ALLPASS="P"
SCORE_ABORT=-50000
MAX_MEMBERS=6
MAX_ROUNDS=8

def split_contract(contract):
    """
    split the handwriting quick notes into complete info
      S5Cxx+2 => 5CXX, S, +2, 13
      1. remove space
      2. change to uppercase
      3. auto append = if no +-=
      4  return tricks as well for each score later
    """
    upper=contract.upper().replace(" ", "")
    if len(upper) == 0: # abort
        contract = BOARD_ABORT
        return "",contract,"",0
    # check whether there is +-= result
    if not re.search(re.compile(r'\+|=|-'), upper):
        upper=upper+"="
    declarer = upper[0]

    # parse to get segments
    contract, sign, result = re.split("(\+|-|=)", upper[1:])
    # AP
    if contract==BOARD_ALLPASS:
        tricks = 0
    else:
        if sign == "=":
            tricks = int(contract[0]) + 6 
        elif sign == "-":
            tricks = int(contract[0]) + 6 - int(result)
        else: # +
            tricks = int(contract[0]) + 6 + int(result)
    return declarer, contract, sign + result, tricks

# https://pbpython.com/pandas-excel-range.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html

"""
excel: E:H and J:M

参赛队伍1	中山大学队		
领队	林航宇	新睿ID	lhylllll
	姓名	新睿ID	新睿大师分
老师/嘉宾	/	沈刚	/
队员2	邵千芊	SqQ	771,53
队员3	马炜俊	超级肥马	153,2
队员4	林航宇	lhylllll	131,54
队员5	吴傲	wuao	23,12
队员6	郑永杰	桥牌哥王	9,85
"""

def get_number(str):
    return int(re.findall("\d+", str)[0])

def is_valid(team):
    members = team["members"]
    for member in members:
        # print(member)
        if str(member[0]) == "nan":
            return False
    return True

def parse_teams(df):
    members = [None] * MAX_MEMBERS
    teams=[]
    for index, row in df.iterrows():
        firstcol = row.array[0]
        if str(firstcol)=='nan': # == np.nan:
            pass
        elif "参赛队伍" in firstcol:
            team = {}
            team["index"] = get_number(firstcol)
            team["name"] = row.array[1]
            members = [None] * MAX_MEMBERS
        elif "领队" in firstcol:
            team["leader"] = (row.array[3], row.array[1], None)
        elif "老师" in firstcol:
            members = [None] * MAX_MEMBERS
            members[0] = (row.array[2], row.array[1], row.array[3])
        elif "队员" in firstcol:
            no = get_number(firstcol)
            if no in range(2,MAX_MEMBERS+1):
                members[no-1] = (row.array[2],row.array[1], row.array[3])
            if no == MAX_MEMBERS:
                team["members"] = members
                if is_valid(team):
                    print("====== %2d team: %s / leader: %s" %(team["index"],team["name"],team["leader"][0]))
                    teams.append(team)
    return teams
def get_teams(excel, all_cols=['E:H','J:M']):
    teams = []
    for cols in all_cols:
        df = pd.read_excel(excel, header=0,usecols=cols)
        teams.extend(parse_teams(df))
    return teams

"""
team	id	1	2	3	4	5	6	7	8
中山大学队	沈刚								
成中医一队	aces								
成中医二队	老爷								
龙岩学院一队	网桥								
龙岩学院二队	门道								
西交一队	nyt								
地鼠队	gopher	N2S+1	S2D=	W3NT=	E1NT=	E4D+1	S1NT-2	S2NT=	S4S-1
"""
def read_excel(xls_file, groupno):
    # read raw data from xls, see sample record.xlsx

    # https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
    pd.set_option("display.unicode.east_asian_width", True)

    sheet = "group" + str(groupno)
    # check sheet first
    xl = pd.ExcelFile(xls_file)
    print("all sheets: ", xl.sheet_names)
    teams = []
    players = []
    if "team" not in xl.sheet_names:
        print("`team` sheet is needed inside excel")
    else:
        # read coresponding team
        df = xl.parse("team")
        print("=== Read teams from team sheet:")
        for index, row in df.iterrows():
            if groupno==1:
                host, guest = "host" , "guest"
            else:
                host, guest = "host." + str(groupno-1), "guest." + str(groupno-1)
            teams.append([row[host],row[guest]])
    for team in teams:
        a,b = team
        print("> %s : %s" % (a,b))
        if a not in players:
            players.append(a)
        if b not in players:
            players.append(b)
    print("players:", players)
    
    # read current sheet for record
    df = pd.read_excel (xls_file, sheet_name=sheet).dropna(how="all").fillna("")
    all_players = {}
    # print(df)
    print("=== All boards: \n", df.head(len(players)))
    urls = [""] * TOTAL_BOARDS
    team = {}
    for index, row in df.iterrows():
        print(index, row)
        if row["id"] == "url":
            urls = row.tolist()[2:TOTAL_BOARDS+2]
            # print("url: ", urls)
        all_players[row["id"]] =  row.tolist()[2:TOTAL_BOARDS+2]
        team[row["id"]] =  row["team"]

    boards = []
    for i in range(TOTAL_BOARDS):
        all_results = []
        for player in players:
            declarer, contract, result, tricks = split_contract(all_players[player][i])
            record = {
                "id": player, 
                "declarer": declarer, 
                "contract": contract, 
                "result" : result, 
                "tricks": tricks
            }
            all_results.append(record)
        board = {
            "all": all_results,
            "url": urls[i]
        }
        boards.append(board)
    return teams, players, boards, team
