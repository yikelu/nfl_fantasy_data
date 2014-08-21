# pylint: disable = C0301
from bs4 import BeautifulSoup
from urllib2 import urlopen

import pandas as pd

pos_idx_map = {
    'qb': 2,
    'rb': 3,
    'wr': 4,
    'te': 5,
}

def make_url(pos, wk):
    ii = pos_idx_map[pos]
    fstr = "http://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx?fs=1&stype=0&sn=1&w=%s&s=&t=0&p=%s&st=FantasyPointsPPR&d=1&ls=&live=false" \
            % (wk, ii)
    return fstr

def html2df(soup):
    table = soup.find('table')
    headers = [header.text.lower() for header in table.find_all('th')]
    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text.encode('utf8') for val in row.find_all('td')])
    rows = [rr for rr in rows if len(rr) > 0]

    df = pd.DataFrame.from_records(rows)
    df.columns = headers

    return df

def position_html_local(posn_name):
    dflist = []
    for ii in range(1, 17):
        fname = '%s%s.html' % (posn_name, ii)
        with open(fname) as f:
            df = html2df(BeautifulSoup(f))
        df['wk'] = ii
        dflist.append(df)
    return pd.concat(dflist)

def position_html(posn_name):
    dflist = []
    for ii in range(1, 17):
        fname = make_url(posn_name, ii)
        with urlopen(fname) as f:
            df = html2df(BeautifulSoup(f))
        df['wk'] = ii
        dflist.append(df)
    return pd.concat(dflist)

if __name__ == '__main__':
    data_all = {}
    for posn in ['qb', 'wr', 'rb', 'te']:
        data_all[posn] = position_html(posn)
