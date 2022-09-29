import logging
import sys
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path

import pandas as pd

from lead_lag import LeadLag


def bitmex_date_parser(x):
    return [datetime.strptime(x_, '%Y-%m-%dD%H:%M:%S.%f000') for x_ in x]


def main():
    bitmex_file = Path('../data/XBTUSD.csv.zip')
    ftx_file = Path('../data/BTC-PERP.csv.zip')
    bitmex, ftx = read_data(bitmex_file, ftx_file)

    ll = LeadLag(ts1=ftx, ts2=bitmex, max_lag=1, verbose=False, min_precision=0.001)
    print('Running inference...')
    ll.run_inference(num_threads=cpu_count() // 2)
    print(f'Estimated lag: {ll.lead_lag} seconds.')
    print(f'Positive lag means ts1 is leading. LLR: {ll.llr:.2f} (cf. paper for the definition of LLR).')
    ll.plot_results()


def read_data(bitmex, ftx):
    bitmex = pd.read_csv(bitmex, index_col=0, parse_dates=True, date_parser=bitmex_date_parser, compression='zip')
    bitmex = bitmex[bitmex['symbol'] == 'XBTUSD']
    bitmex = bitmex[bitmex['price'].diff() != 0]
    bitmex = bitmex['price']
    ftx = pd.read_csv(ftx, index_col=0, parse_dates=True, compression='zip')
    ftx = ftx[ftx['price'].diff() != 0]
    ftx = ftx['price']
    return bitmex, ftx


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
    main()
