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

python scripts/bitcoin/convert_bitcoinchart_file.py $1 ${TMP_DIR}/${FILE_1}.processed
python scripts/bitcoin/convert_bitcoinchart_file.py $2 ${TMP_DIR}/${FILE_2}.processed

mkdir ${TMP_DIR}/data-per-day/

python scripts/bitcoin/split_dataset_per_day.py ${TMP_DIR}/${FILE_1}.processed ${TMP_DIR}/data-per-day/
python scripts/bitcoin/split_dataset_per_day.py ${TMP_DIR}/${FILE_2}.processed ${TMP_DIR}/data-per-day/


# Comparison of the different executions (single thread vs multi thread, Common Python vs C-Python.
# 1 - single thread - Common Python
# 2 - multi thread - Common Python
# 3 - single thread - C Python
# 4 - multi thread - C Python


make clean
rm -rf *.so

# 0 => single thread.
# 1 => use all the physical cores of the machine.

time python main_bitcoin.py ${TMP_DIR}/data-per-day ${TMP_DIR}/bitcoin_contrasts_1/ 0 >> ${TMP_DIR}/1.txt
time python main_bitcoin.py ${TMP_DIR}/data-per-day ${TMP_DIR}/bitcoin_contrasts_2/ 1 >> ${TMP_DIR}/2.txt


# QUITE UNSTABLE WITH THE LATEST IMPL. SOMETIMES IT RETURNS NAN. SO I DO NOT ADVISE TO USE IT IN PRODUCTION.
#make clean
#make # using the C Python
#
#time python main_bitcoin.py ${TMP_DIR}/data-per-day ${TMP_DIR}/bitcoin_contrasts_3/ 0 >> ${TMP_DIR}/3.txt
#time python main_bitcoin.py ${TMP_DIR}/data-per-day ${TMP_DIR}/bitcoin_contrasts_4/ 1 >> ${TMP_DIR}/4.txt