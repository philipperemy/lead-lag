import os
from glob import glob

from tqdm import tqdm

import lead_lag

MAX_LEAD_LAG = 180
VERBOSE = False


def run_inference(data_file_1, data_file_2, output_filename, verbose=True, multi_threading=False):
    from lead_lag.scripts.read_bitcoin_data import bitcoin_data
    arr_1, arr_2 = bitcoin_data(data_file_1, data_file_2)
    ll = lead_lag.LeadLag(arr_1, arr_2, MAX_LEAD_LAG, verbose)
    ll.run_inference(multi_threading)
    ll.write_results_to_file(output_filename)
    print(f'Inference took {ll.inference_time:.3f} seconds.')


def run_inference_for_all_files(processed_data_dir='/tmp/bitcoin/', output_dir='out', multi_threading=False):
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

    sorted_dates = sorted(file_listing_dict)  # [0:80]
    with tqdm(sorted_dates) as bar:
        for date in bar:
            data = file_listing_dict[date]
            ex1 = exchanges[0]
            ex2 = exchanges[1]
            data_filename_1 = data[ex1]
            data_filename_2 = data[ex2]
            output_filename = os.path.join(output_dir, f'contrasts_{ex1}_related_to_{ex2}_{date}.csv')
            bar.set_description(f'Working on {output_filename}')
            run_inference(data_filename_1, data_filename_2, output_filename, VERBOSE, multi_threading)


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
