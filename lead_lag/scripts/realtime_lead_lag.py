from collections import deque

import numpy as np

from lead_lag import LeadLag

t_x = np.arange(0, 15000, 1)
t_y = np.arange(0, 15000, 1)

# first 5000 have a lag of 10 units of time.
np.random.seed(123)
x1 = np.cumsum(np.random.randn(5000))
y1 = np.zeros_like(x1)
y1[:-10] = x1[10:]  # x is lagging by 10 units.

# second 5000 have a lag of 20 units of time.
x2 = np.cumsum(np.random.randn(5000))
y2 = np.zeros_like(x2)
y2[:-20] = x2[20:]  # x is lagging by 20 units.

# last 5000 have a lag of -20 units of time.
x3 = np.cumsum(np.random.randn(5000))
y3 = np.zeros_like(x2)
y3[:-20] = x3[20:]  # x is lagging by 20 units.

# swap x and y.
a = y3
y3 = x3
x3 = a

x = np.concatenate((x1, x2, x3))
y = np.concatenate((y1, y2, y3))

assert not np.isnan(x).any()
assert not np.isnan(y).any()


# (x, t_x)
# (y, t_y)

class RealTimeAggregator:

    def __init__(self, history_length):
        self.ts = deque(maxlen=history_length)

    def add(self, value: float, timestamp: int):
        self.ts.append((timestamp, value))

    def get(self):
        return np.vstack(self.ts)


def main():
    history_length = 100
    x_rt = RealTimeAggregator(history_length)
    y_rt = RealTimeAggregator(history_length)

    for i in range(len(t_x)):
        x_rt.add(value=x[i], timestamp=t_x[i])
        y_rt.add(value=y[i], timestamp=t_y[i])

        if i > 1000 and i % 500 == 0:  # enough values.
            ll = LeadLag(arr_1_with_ts=y_rt.get(),
                         arr_2_with_ts=x_rt.get(),
                         max_absolute_lag=30,  # +/- 20 seconds.
                         verbose=False)

            ll.run_inference(multi_threading=False)
            # ll.plot_data()
            # ll.plot_results()
            print(f'i = {i}, lead_lag = {ll.lead_lag}, inference_time = {1000 * ll.inference_time:.1f} ms.')


if __name__ == '__main__':
    main()
