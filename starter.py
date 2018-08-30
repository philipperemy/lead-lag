import lead_lag

from scripts.read_bitcoin_data import bitcoin_data

bitflyer_with_ts, btcbox_with_ts = bitcoin_data('data/bitflyerJPY_2018-08-12_small.csv',
                                                'data/btcboxJPY_2018-08-12_small.csv')

ll = lead_lag.LeadLag(arr_1_with_ts=bitflyer_with_ts,
                      arr_2_with_ts=btcbox_with_ts,
                      max_absolute_lag=60,
                      verbose=True)

ll.run_inference()

print('contrast values =', ll.contrasts)
print('Estimated lag (in seconds):', ll.lead_lag)
print('Positive means bitflyer is leading.')
print(ll.inference_time, 'seconds')
ll.plot_results()
