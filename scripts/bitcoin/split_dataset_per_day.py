def split_dataset_per_day(input_filename, output_dir):
    import warnings

    warnings.filterwarnings('ignore', message='numpy.dtype size changed')
    warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

    import os
    import pandas as pd
    import shutil

    try:
        shutil.rmtree(output_dir)
    except:
        pass
    os.makedirs(output_dir)

    def to_days(df):
        return [g[1] for g in df.groupby([df.index.year, df.index.month, df.index.day])]  # DataFrame to List<Day>

    if not os.path.isfile(os.path.expanduser(input_filename)):
        print('Could not find the CSV file with raw data. '
              'Browse http://api.bitcoincharts.com/v1/csv/ and '
              'download one (unzip it first).')
        exit(1)
    else:
        print(f'Processing {input_filename}.')

    d = pd.read_csv(input_filename, index_col=0, parse_dates=True)
    d_days = to_days(d)
    for d_day in d_days:
        date = str(d_day.index[0]).split(' ')[0]
        input_filename_wo_extension = os.path.basename(input_filename.split('.')[0])
        output_filename = os.path.join(output_dir, input_filename_wo_extension + f'_{date}_small.csv')
        print(f'Writing to: {output_filename}.')
        d_day.to_csv(output_filename, index=True)


def main():
    import sys

    if len(sys.argv) != 3:
        print('Specify a processed CSV filename from the convert_bitcoinchart_file.py script and an output folder.')
        exit(1)
    input_filename = sys.argv[1]
    output_dir = sys.argv[2]
    split_dataset_per_day(input_filename=input_filename, output_dir=output_dir)


if __name__ == '__main__':
    main()
