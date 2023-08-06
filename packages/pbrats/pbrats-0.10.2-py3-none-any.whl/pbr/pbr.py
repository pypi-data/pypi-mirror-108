#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import sys
import shutil
import tempfile
import xlsxwriter
# https://xlsxwriter.readthedocs.io/working_with_cell_notation.html
from xlsxwriter.utility import xl_rowcol_to_cell
import pkg_resources  # part of setuptools
version = pkg_resources.require("pbrats")[0].version

from string import Template

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3/28154841
import repackage
repackage.up()

# https://stackoverflow.com/questions/25127673/how-to-print-utf-8-to-console-with-python-3-4-windows-8
sys.stdout.reconfigure(encoding='utf-8')

from pbr.bridge_score import Contract, matchpoints, imps, vul_table, board_vul, vp_scale_8boards, vul_maptable
from pbr.pbr_template import *
from pbr.pbr_excel import *

from bridge_utils.pbn2html.pbn2html import get_from_pbn_file, pbn_html_deal
from bridge_utils.xin2pbn.xin2pbn import xin2pbn

def get_dealside(board_no):
    # return EW/NS for scoring
    if (board_no%2) == 0:
        dealside="NS"
    else:
        dealside="EW"
    return dealside

# fill one id for each board
def process_oneid(board, vuls, dealside, template=id_template):
    src = Template(template)
    contract = board["contract"]
    declarer = board["declarer"]
    vul_str = vul_table[vuls]

    if declarer in vul_maptable[vuls]:
        vul=True
    else:
        vul=False
    if contract == BOARD_ABORT:
        score=SCORE_ABORT
    elif contract == BOARD_ALLPASS:
        score=0
        declarer=""
    else:
        score = Contract.from_str(contract, vul).score(board["tricks"])
    if declarer in "EW":
        score = -score
    # need vul 
    # print(score)
    if score > 0:
        scorecolor="red"
    else:
        scorecolor="green"
    if score==abs(SCORE_ABORT):
        show_score = ""
    else:
        show_score = score
    all = { "contract": html_suit(contract), "result": board["result"],
            "declarer" : declarer, "score": show_score, "scorecolor": scorecolor, "vul" : vul_str}
    return src.safe_substitute(all), score

# fill one id for each board
def process_onedeal(deal,vuls, dealside, ):
    html, score = process_oneid(deal,vuls, dealside, board_id_template)
    return html

def get_teammatch_onerow(idx, board, team):
    # for one row for each board with host/guest id
    src = Template(onerow_template)
    host_id, guest_id = team
    # TODO
    host = [d for d in board if d['id'] == host_id][0]
    guest = [d for d in board if d['id'] == guest_id][0]
    # need IMP, VP
    vul = vul_table[board_vul[idx]]
    dealside = get_dealside(idx)
    host_html, host_score = process_oneid(host, board_vul[idx], dealside)
    guest_html, guest_score = process_oneid(guest, board_vul[idx], dealside)
    score_diff = host_score - guest_score
    imp = imps(host_score,guest_score)

    host_imp=guest_imp=""
    host_abort=guest_abort=False
    if abs(score_diff) > abs(SCORE_ABORT) - 10000: # abort
        score_diff = ""
        if abs(guest_score) == abs(SCORE_ABORT):
            guest_abort = True
            host_imp, guest_imp = (3,0)
        else:
            host_abort = True
            host_imp, guest_imp = (0,3)
        #print(host_imp, guest_imp)
    else:
        if imp > 0:
            host_imp=str(imp)
        elif imp <0:
            guest_imp=str(-imp)
    all = { "boardno": idx+1, "vul": vul, "host": host_html, "guest" : guest_html, "diff" : score_diff, "hostimp": host_imp, "guestimp": guest_imp }
    return src.safe_substitute(all), host_imp, guest_imp, host_abort, guest_abort

def get_board_onerow(idx, deal):
    # for one row for each board with host/guest id
    src = Template(oneboardrow_template)
    # need IMP, VP
    dealside = get_dealside(idx)
    vul = board_vul[idx]
    host_html = process_onedeal(deal, vul, dealside)
    all = { "boardno": idx+1, "vul": vul, "host": host_html, "id": deal["id"] }
    return src.safe_substitute(all)

def get_pbn_html(url):
    temp = tempfile.NamedTemporaryFile().name
    xin2pbn(url,temp)
    pbn = get_from_pbn_file(temp + ".pbn")
    pbn_table = pbn_html_deal(pbn, ul="  ",dds=True)
    pbn_html = "<table align='center' cellspacing='0px' cellpadding='6px'>%s</table><p />" % pbn_table
    return pbn_html

def get_match(boards, teamno, team):
    """
    calculate one match
    """
    rows = ""
    total_hostimp = total_guestimp = 0
    total_hostabort = total_guestabort = True
    for idx, board in enumerate(boards):
        row,host_imp,guest_imp, host_abort, guest_abort = get_teammatch_onerow(idx, board["all"], team)
        rows += row
        total_hostimp += int(host_imp) if host_imp else 0
        total_guestimp+= int(guest_imp) if guest_imp else 0
        if host_abort == False:
            total_hostabort = False
        if guest_abort == False:
            total_guestabort = False
    # calculate VP from IMPs, it depends on board number
    diff_imp = total_hostimp - total_guestimp
    if abs(diff_imp) > len(vp_scale_8boards)-1:
        vp = vp_scale_8boards[-1] # 20.00
    else:
        vp = vp_scale_8boards[abs(diff_imp)]

    # handle abort
    if total_hostabort:
        host_vp = 0
        guest_vp = 12
    elif total_guestabort:
        host_vp = 12
        guest_vp = 0
    else:
        if diff_imp > 0:
            host_vp=vp
            guest_vp=20-vp
        else:
            guest_vp=vp
            host_vp=20-vp

    result = {
        "rows" : rows,
        "teamno": teamno,
        "teamhost" : team[0],
        "teamguest" : team[1],
        "hostimp" : total_hostimp,
        "guestimp": total_guestimp,
        "hostvp": format(host_vp,".2f"),
        "guestvp": format(guest_vp,".2f")
    }
    src = read_template("match-temp.html")
    contents = src.safe_substitute(result)
    return contents,(total_hostimp,total_guestimp), (host_vp,guest_vp)

def get_team_summary(summary):
    teams_html = ""
    print("\n>> Summary of team score:")
    print("==============")
    for idx, scores in enumerate(summary):
        teams, imp, vp = scores
        print("> %d: %2d : %-2d, %.2f : %.2f / %s" % \
            (idx+1,imp[0],imp[1],vp[0],vp[1],"%s vs %s" % (teams[0], teams[1]) ))
        html =  "<tr><td  class='td_top'><a href='#match-%d'>%s<a></td><td class='td_top'>vs</td><td class='td_top'><a href='#match-%d'>%s</a></td>" % (idx+1, teams[0], idx+1, teams[1])
        html += "<td align='right' class='d_lt'>%2d</td><td class='d_top''>:</td><td align='left' class='td_top'>%2d</td>" %  (imp[0],imp[1])
        html += "<td align='right' class='d_lt'>%.2f</td><td class='d_top' padding='1px'>:</td><td align='left' class='td_top'>%.2f</td></tr>" %  (vp[0],vp[1])

        teams_html += html

    src = Template(summary_template)
    result={ "teamsummary" :teams_html } 
    contents = src.safe_substitute(result)
    return contents

def get_boards_summary(boards):
    """
    calculate one match
    """
    boards_html = ""
    for idx, board in enumerate(boards):
        # for each board
        src = Template(board_template)
        board_html = pbn_html = ""
        for result in board["all"]:
            row = get_board_onerow(idx, result)
            board_html += row
        # if has xinurl, pbn2html
        if board["url"].startswith("http"):
            # print("found url", board["url"])
            pbn_html = get_pbn_html(board["url"])
        result={ "board" : board_html, "boardno": idx+1, "pbn": pbn_html} 
        contents = src.safe_substitute(result)
        boards_html += contents
    #src = Template(boards_template)
    #result={ "boards" :teams_html } 
    return boards_html

def calc_groups(record_xls, groupno, base_file):
    try:
        group = "group" + str(groupno)
        output = base_file + "-" + group + ".html"
        currentdate = os.path.basename(output)[:8]
        teams,players,boards, id_team = read_excel(record_xls, groupno)
        
        teams_html =""
        summary=[]
        for idx, team in enumerate(teams):
            html, imp, vp = get_match(boards, idx+1, team)
            teams_html += html
            summary.append([team, imp, vp])
        summary_html=get_team_summary(summary)

        boards_html=get_boards_summary(boards)

        result = {  "teams" : teams_html, 
                    "summary" : summary_html, 
                    "boards" : boards_html,
                    "version" : version,
                    "group": groupno,
                    "date": currentdate}
        src = read_template("index-temp.html")
        contents = src.safe_substitute(result)

        with io.open(output, "w", encoding="utf-8") as text_file:
            print("write to file %s" % output)
            text_file.write(contents)
        return summary, id_team

    except KeyError as e:
        print("KeyError", e)


def generate_final(base_file, results, ids):

    tables = len(results[0])
    # https://xlsxwriter.readthedocs.io/working_with_data.html
    excel = base_file + "-result.xlsx"
    try:
        workbook = xlsxwriter.Workbook(excel)
        worksheet = workbook.add_worksheet("各桌成绩")
        # set big width for id
        for col in ["B","F","H","L"]:
            worksheet.set_column('%s:%s' % (col,col), 30)

        # print(ids)
        # Add a header format.
        cell_format  = workbook.add_format({
            'align':"center",
            'border': 1})
        tp_format = workbook.add_format({
            'align':"center",
            'border': 1,
            'num_format': '0.0'})
        vp_format = workbook.add_format({
            'align':"center",
            'border': 1,
            'num_format': '0.00'})
        print("\n>> All teams score")
        print("============")
        
        base_x = 1
        base_y = 1

        for table in range(tables):
            hostteamvp = guestteamvp = 0
            hosttp = guesttp = 0.0
            (host, guest),x,x = results[0][table]
            for i in range(MAX_MEMBERS):
                print(results[i][table])
                (host, guest),x,(hostvp, guestvp) = results[i][table]
                hostteamvp += hostvp
                guestteamvp += guestvp
                if hostvp > guestvp:
                    hosttp +=1
                elif hostvp == guestvp:
                    hosttp += 0.5
                    guesttp+= 0.5
                else:
                    guesttp +=1
                worksheet.write(base_x + i + 1, base_y, host,cell_format)
                worksheet.write(base_x + i + 1, base_y+1, hostvp,vp_format)
                worksheet.write(base_x + i + 1, base_y+2, str(i + 1),cell_format)
                worksheet.write(base_x + i + 1, base_y+3, guestvp,vp_format)
                worksheet.write(base_x + i + 1, base_y+4, guest,cell_format)

            print(ids[host],hosttp,"%d 桌" % (table + 1),guesttp,ids[guest])
            print(hostteamvp,guestteamvp)

            worksheet.write(base_x, base_y, ids[host],cell_format)
            worksheet.write(base_x, base_y+1, hosttp,tp_format)
            worksheet.write(base_x, base_y+2, "%d 桌" % (table + 1),cell_format)
            worksheet.write(base_x, base_y+3, guesttp, tp_format)
            worksheet.write(base_x, base_y+4, ids[guest],cell_format)

            worksheet.write(base_x + MAX_MEMBERS +1, base_y, "", cell_format)
            # 'C9', '=SUM(C3:C8)'
            vp_host_cell = xl_rowcol_to_cell(base_x + MAX_MEMBERS +1, base_y+1)
            vp_host_start_cell = xl_rowcol_to_cell(base_x + 1, base_y+1)
            vp_host_end_cell = xl_rowcol_to_cell(base_x + MAX_MEMBERS, base_y+1)
            # print(vp_host_cell,'=SUM(%s:%s)' % (vp_host_start_cell,vp_host_end_cell))
            worksheet.write_formula(vp_host_cell, '=SUM(%s:%s)' % (vp_host_start_cell,vp_host_end_cell),cell_format)
            # worksheet.write(base_x + MAX_MEMBERS +1, base_y+1, hostteamvp,cell_format)
            worksheet.write(base_x + MAX_MEMBERS +1, base_y+2, "VP",cell_format )

            vp_guest_cell = xl_rowcol_to_cell(base_x + MAX_MEMBERS +1, base_y+3)
            vp_guest_start_cell = xl_rowcol_to_cell(base_x + 1, base_y+3)
            vp_guest_end_cell = xl_rowcol_to_cell(base_x + MAX_MEMBERS, base_y+3)
            # print(vp_guest_cell, '=SUM(%s:%s)' % (vp_guest_start_cell,vp_guest_end_cell))
            worksheet.write_formula(vp_guest_cell, '=SUM(%s:%s)' % (vp_guest_start_cell,vp_guest_end_cell),cell_format)

            #worksheet.write(base_x + MAX_MEMBERS +1, base_y+3, guestteamvp,cell_format)
            worksheet.write(base_x + MAX_MEMBERS +1, base_y+4, "", cell_format)

            if (table+1) % 2 == 0:
                base_y = 1
                base_x += (MAX_MEMBERS + 3) # team, vp, space
            else:
                base_y = 7

        workbook.close()
    except xlsxwriter.exceptions.FileCreateError as e:
        print(e)
        print("Probably close the file ", excel)
    #for idx, group in enumerate(groups):
    #    print("group: ", idx+1, group)
    #    df = pd.DataFrame([[''] * MAX_ROUNDS ] * len(teams),
    #                index=[team_names,group],
    #               columns=list(range(1, MAX_ROUNDS+1)))
    #    df.to_excel( excel, sheet_name='各桌成绩',  index_label=["team","id"])
    else:
        print(excel," is generated")

def pbr(record_xls):
    """
    read xls file and generate related html
    """
    base_file = record_xls[:-len("xlsx")-1]
    
    results = []
    ids = {}
    for i in range(MAX_MEMBERS):
        result, id_team = calc_groups(record_xls, i+1, base_file)
        results.append(result)
        #print(id_team)
        ids.update(id_team)
    generate_final(base_file, results, ids)

def usage():
    usage = """
    $ pbr sample # download sample record.xlsx
    $ pbr <record.xlsx> # check result.html
    see more for README
    """
    print(usage)

def download_sample():
    if __name__ == '__main__':
        print("dear contributor, do this in package mode")
        return
    sample_files=['record.xlsx']
    for sample_file in sample_files:
        if os.path.exists(sample_file):
            print("%s already exists, ingore (or remove it first)" % sample_file)
        else:
            print("download sample file -> [%s]" % sample_file)
            shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)),sample_file),".")

def main():
    # print(sys.argv)
    if len(sys.argv) > 1:
        params = sys.argv[1:]
        if params[0] == "sample":
            download_sample()
        elif params[0] == "help":
            usage()
        else:
            record_xls=params[0]
            if record_xls.endswith(".xlsx"):
                pbr(record_xls)
            else:
                usage()
    else:
        usage()

if __name__ == '__main__':
    main()
