import warnings

warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

import numpy as np
import os
from tqdm import tqdm

from contrast import CrossCorrelationHY

MAX_LEAD_LAG = 120


def run_inference(data_file_1, data_file_2, output_filename='out.csv', verbose_mode=True):
    # ===== DATA PART =====
    from scripts.read_bitcoin_data import bitcoin_data
    x, y, t_x, t_y = bitcoin_data(data_file_1, data_file_2)
    # in that case we don't know the lead lag so we can just set a big value here.
    # ===== DATA PART =====

    # import matplotlib.pyplot as plt
    # plt.title('Non-synchronous data with leader / lagger relationship')
    # plt.scatter(range(len(x)), x, s=0.5, color='lime')
    # plt.scatter(range(len(x)), y, s=0.5, color='blue')
    # plt.legend(['Bitstamp', 'WEX'])
    # plt.show()

    # ===== COMPUTATION ====
    max_lead_lag = MAX_LEAD_LAG  # in seconds.
    lag_range = np.arange(-max_lead_lag, max_lead_lag + 1, 1)
    cc = CrossCorrelationHY(x, y, t_x, t_y, lag_range, normalize=True, verbose_mode=verbose_mode)
    contrasts = cc.fast_inference()
    cc.write_results_to_file(output_filename, contrasts)

    # for lag, contrast in zip(lag_range, contrasts):
    #     print(lag, contrast)

    # import matplotlib.pyplot as plt
    # plt.title('Contrast = f(Lag)')
    # plt.ylabel('Contrast')
    # plt.xlabel('Lag')
    # plt.plot(lag_range, contrasts)
    # plt.show()

    # could have a better granularity.
    est_lead_lag_index = np.argmax(contrasts)
    print('Est. lead lag =', lag_range[est_lead_lag_index])
    # ===== COMPUTATION ====


def run_inference_for_all_files(processed_data_dir='/tmp/bitcoin/', output_dir='out'):
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

    # pprint(file_listing_dict, indent=4)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    verbose_mode = False
    with tqdm(file_listing_dict.items()) as bar:
        for date, data in bar:
            ex1 = exchanges[0]
            ex2 = exchanges[1]
            data_filename_1 = data[ex1]
            data_filename_2 = data[ex2]
            output_filename = os.path.join(output_dir, f'contrasts_{ex1}_related_to_{ex2}_{date}.csv')
            bar.set_description(f'Working on {output_filename}')
            run_inference(data_filename_1, data_filename_2, output_filename, verbose_mode)


def main():
    import sys

    if len(sys.argv) != 3:
        print('Specify a processed data directory containing CSV files of bitcoin exchanges and an output directory.')
        exit(1)
    processed_data_dir = sys.argv[1]
    output_dir = sys.argv[2]
    run_inference_for_all_files(processed_data_dir, output_dir)


if __name__ == '__main__':
    main()
