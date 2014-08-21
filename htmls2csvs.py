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

def position_html_local(posn):
    dflist = []
    for ii in range(1, 17):
        fname = '%s%s.html' % (posn, ii)
        with open(fname) as f:
            df = html2df(BeautifulSoup(f))
        df['wk'] = ii
        df.columns = header_clean(df.columns, posn)
        dflist.append(df)
    return pd.concat(dflist)

def position_html(posn):
    dflist = []
    for ii in range(1, 17):
        fname = make_url(posn, ii)
        df = html2df(BeautifulSoup(urlopen(fname)))
        df['wk'] = ii
        df.columns = header_clean(df.columns, posn)
        dflist.append(df)
    return pd.concat(dflist)

pos_header_suffixes = {
    'qb': ['_pass', '_rush'],
    'rb': ['_rush', '_recv'],
    'wr': ['_recv'],
    'te': ['_recv'],
}

exclude_cols = ['rk', 'player', 'team', 'pos', 'fantasy points',
'wk', 'fum', 'lost', 'qb rating']

def header_clean(header, posn):
    res = []
    if posn in pos_header_suffixes:
        suffixes = pos_header_suffixes[posn]
        seen_dict = {hh: 0 for hh in header}
        for hh in header:
            if not hh in exclude_cols:
                hres = hh + suffixes[seen_dict[hh]]
                seen_dict[hh] += 1
                res.append(hres)
            else:
                res.append(hh)
    else:
        res = header

    return res


if __name__ == '__main__':
    data_all = {}
    for pp in ['qb', 'wr', 'rb', 'te']:
        data_all[pp] = position_html_local(pp)
        data_all[pp].to_pickle('%s.pkl' % pp)
