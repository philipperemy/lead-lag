#!/usr/bin/env bash

python convert_bitcoinchart_file.py ~/Dropbox/lead-lag/raw-data/bitstampUSD.csv /tmp/bitstampUSD.csv.processed
python convert_bitcoinchart_file.py ~/Dropbox/lead-lag/raw-data/wexUSD.csv /tmp/wexUSD.csv.processed

python split_dataset_per_day.py /tmp/bitstampUSD.csv.processed /tmp/bitcoin
python split_dataset_per_day.py /tmp/wexUSD.csv.processed /tmp/bitcoin

python main.py /tmp/bitcoin /tmp/bitcoin_contrasts/