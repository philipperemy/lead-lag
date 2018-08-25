import numpy as np
import os
from tqdm import tqdm

from contrast import CrossCorrelationHY


def run_inference(data_file_1, data_file_2, output_filename='out.csv', verbose_mode=True):
    # ===== DATA PART =====
    print('Using bitcoin data.')
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
    max_lead_lag = 40  # in seconds.
    lag_range = np.arange(-max_lead_lag, max_lead_lag, 1)
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


def run_inference_for_all_files():
    from glob import glob
    from scripts.read_bitcoin_data import EXCHANGE_1, EXCHANGE_2, CURRENCY
    all_files = glob('data2/**_small.csv', recursive=True)
    file_listing_dict = {}
    for filename in all_files:
        exchange, date, _ = os.path.splitext(os.path.basename(filename))[0].split('_')

        if date not in file_listing_dict:
            file_listing_dict[date] = {}

        if exchange not in file_listing_dict[date]:
            file_listing_dict[date][exchange] = filename

    verbose_mode = False
    with tqdm(file_listing_dict.items()) as bar:
        for date, data in bar:
            data_filename_1 = data[EXCHANGE_1 + CURRENCY]
            data_filename_2 = data[EXCHANGE_2 + CURRENCY]
            output_filename = f'contrasts_{EXCHANGE_1}_{EXCHANGE_2}_{date}.csv'
            bar.set_description(f'Working on {output_filename}')
            run_inference(data_filename_1, data_filename_2, output_filename, verbose_mode)


if __name__ == '__main__':
    # run_inference('data/bitflyerJPY.csv.small', 'data/btcboxJPY.csv.small')
    run_inference_for_all_files()
