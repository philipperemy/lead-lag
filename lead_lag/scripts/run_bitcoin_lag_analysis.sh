#!/usr/bin/env bash

TMP_DIR=/tmp/lead-lag

if [[ $# -eq 0 ]] ; then
    echo 'Specify the http://api.bitcoincharts.com/v1/csv/ files like:'
    echo '/path/to/bitflyerJPY.csv /path/to/btcboxJPY.csv'
    exit 0
fi

set -e

rm -rf ${TMP_DIR} && mkdir ${TMP_DIR}

FILE_1=$(basename $1)
FILE_2=$(basename $2)

python bitcoin/convert_bitcoinchart_file.py $1 ${TMP_DIR}/${FILE_1}.processed
python bitcoin/convert_bitcoinchart_file.py $2 ${TMP_DIR}/${FILE_2}.processed

mkdir ${TMP_DIR}/data-per-day/

python bitcoin/split_dataset_per_day.py ${TMP_DIR}/${FILE_1}.processed ${TMP_DIR}/data-per-day/
python bitcoin/split_dataset_per_day.py ${TMP_DIR}/${FILE_2}.processed ${TMP_DIR}/data-per-day/

# 0 => single thread.
# 1 => use all the physical cores of the machine.

python main_bitcoin.py ${TMP_DIR}/data-per-day ${TMP_DIR}/bitcoin_contrasts/ 1 >> ${TMP_DIR}/lead_lag.log


