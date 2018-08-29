import warnings

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

import numpy as np
import os
from tqdm import tqdm

from contrast import CrossCorrelationHY

MAX_LEAD_LAG = 60


def run_inference(data_file_1, data_file_2, output_filename='out.csv', verbose_mode=True, multi_threading=False):
    from scripts.read_bitcoin_data import bitcoin_data
    x, y, t_x, t_y = bitcoin_data(data_file_1, data_file_2)
    max_lead_lag = MAX_LEAD_LAG  # in seconds.
    lag_range = np.arange(-max_lead_lag, max_lead_lag + 1, 1)
    cc = CrossCorrelationHY(x, y, t_x, t_y, lag_range, normalize=True, verbose_mode=verbose_mode)
    if multi_threading:
        contrasts = cc.fast_inference()
    else:
        contrasts = cc.slow_inference()
    cc.write_results_to_file(output_filename, contrasts)
    est_lead_lag_index = np.argmax(contrasts)
    print('Est. lead lag =', lag_range[est_lead_lag_index])


def run_inference_for_all_files(processed_data_dir='/tmp/bitcoin/', output_dir='out', multi_threading=False):
    from glob import glob
    all_files = glob(f'{processed_data_dir}/**_small.csv', recursive=True)
    file_listing_dict = {}
    exchanges = set()
    for filename in all_files:
        exchange, date, _ = os.path.splitext(os.path.basename(filename))[0].split('_')

        if date not in file_listing_dict:
            file_listing_dict[date] = {}

        if exchange not in file_listing_dict[date]:
            file_listing_dict[date][exchange] = filename

        exchanges.add(exchange)

    exchanges = sorted(exchanges)
    assert len(exchanges) == 2, 'We need exactly two exchanges.'

    # dates intersection between those two datasets.
    file_listing_dict = {k: v for k, v in file_listing_dict.items() if len(v) == 2}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    verbose_mode = False
    sorted_dates = sorted(file_listing_dict)

    # sorted_dates = sorted_dates[0:50]

    with tqdm(sorted_dates) as bar:
        for date in bar:
            data = file_listing_dict[date]
            ex1 = exchanges[0]
            ex2 = exchanges[1]
            data_filename_1 = data[ex1]
            data_filename_2 = data[ex2]
            output_filename = os.path.join(output_dir, f'contrasts_{ex1}_related_to_{ex2}_{date}.csv')
            bar.set_description(f'Working on {output_filename}')
            from time import time
            start_time = time()
            run_inference(data_filename_1, data_filename_2, output_filename, verbose_mode, multi_threading)
            print(f'Inference took {time()-start_time:.3f} seconds.')


def main():
    import sys

    if len(sys.argv) != 4:
        print('Specify a processed data directory containing CSV files '
              'of bitcoin exchanges, an output directory and whether you want to run on multi threads.')
        exit(1)
    processed_data_dir = sys.argv[1]
    output_dir = sys.argv[2]
    multi_threading = bool(int(sys.argv[3]))
    run_inference_for_all_files(processed_data_dir, output_dir, multi_threading)


if __name__ == '__main__':
    main()
