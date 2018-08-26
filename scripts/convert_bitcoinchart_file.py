def process_bitcoincharts_data(input_filename, output_filename):
    import warnings

    warnings.filterwarnings('ignore', message='numpy.dtype size changed')
    warnings.filterwarnings('ignore', message='numpy.ufunc size changed')

    import datetime
    import os
    import pandas as pd
    def unix_to_datetime(d):
        return datetime.datetime.fromtimestamp(d)

    def to_days(df):
        return [g[1] for g in df.groupby([df.index.year, df.index.month, df.index.day])]  # DataFrame to List<Day>

    if not os.path.isfile(input_filename):
        print('Could not find the CSV file with raw data. '
              'Browse http://api.bitcoincharts.com/v1/csv/ and '
              'download one (unzip it first).')
        exit(1)
    else:
        print(f'Processing {input_filename}.')

    d = pd.read_csv(input_filename, parse_dates=False, names=['timestamp', 'last', 'volume'])
    d['date'] = d['timestamp'].apply(unix_to_datetime)
    d.set_index(d['date'], inplace=True)
    d.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
    d = d[(d['last'] - d['last'].shift(1)) != 0]
    d.drop(labels=['date', 'volume', 'timestamp'], axis=1, inplace=True)
    d.to_csv(output_filename, index=True)
    # d_days = to_days(d)
    # for d_day in d_days:
    #     date = str(d_day.index[0]).split(' ')[0]
    #     input_filename_wo_extension, extension = os.path.splitext(input_filename)
    #     input_filename = input_filename
    #     output_filename = input_filename_wo_extension + f'_{date}_small.csv'
    #     print(f'Writing to: {output_filename}.')
    #     d_day.to_csv(output_filename, index=True)
    # print(pd.concat(d_days[select_day_start:select_day_end]).head(30))
    # print(len(d_days), len(d_days[select_day_start:select_day_end]))
    # pd.concat(d_days[select_day_start:select_day_end]).to_csv(output_filename, index=True)


def main():
    import sys

    if len(sys.argv) != 2:
        print('Specify a CSV file from http://api.bitcoincharts.com/v1/csv/.')
        exit(1)
    input_filename = sys.argv[1]
    output_filename = input_filename + '.processed'
    process_bitcoincharts_data(input_filename=input_filename,
                               output_filename=output_filename)


if __name__ == '__main__':
    main()
