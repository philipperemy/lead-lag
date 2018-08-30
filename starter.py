import lead_lag

ll = lead_lag.LeadLag('data/bitflyerJPY_2018-08-12_small.csv',
                      'data/btcboxJPY_2018-08-12_small.csv',
                      max_absolute_lag=60,
                      verbose=True)

ll.run_inference()

print('contrast values =', ll.contrasts)
print('Estimated lag (in seconds):', ll.lead_lag)
print('Positive means bitflyer is leading.')
print(ll.inference_time, 'seconds')
ll.plot()
