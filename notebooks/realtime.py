from collections import deque

import matplotlib.pyplot as plt
import numpy as np

from lead_lag import LeadLag

plt.ion()


def generate_data():
    t_x = np.arange(0, 15000, 1)
    t_y = np.arange(0, 15000, 1)

    # first 5000 have a lag of 10 units of time.
    np.random.seed(124)
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

    # We want to make something asynchronous.
    t_x = sorted(np.random.choice(range(len(t_x)), size=8000, replace=False))
    t_y = sorted(np.random.choice(range(len(t_y)), size=8000, replace=False))
    x = x[t_x]
    y = y[t_y]

    assert not np.isnan(x).any()
    assert not np.isnan(y).any()
    return x, y, t_x, t_y


class RealTimeAggregator:

    def __init__(self, history_length):
        self.ts = deque(maxlen=history_length)

    def add(self, value: float, timestamp: int):
        self.ts.append((timestamp, value))

    def get(self):
        return np.vstack(self.ts)


def main():
    # x is lagging, y is leading.
    # x contains 14,000 randomly sampled points.
    # y contains 8,000 randomly sampled points.
    x, y, t_x, t_y = generate_data()

    realtime = True

    if realtime:

        history_length = 300
        x_rt = RealTimeAggregator(history_length)
        y_rt = RealTimeAggregator(history_length)

        llr_list = []
        timestamps = sorted(set(t_x).union(t_y))
        time_index_x = 0
        time_index_y = 0
        for t in timestamps:
            while time_index_x < len(t_x) and t_x[time_index_x] <= t:
                x_rt.add(value=x[time_index_x], timestamp=t_x[time_index_x])
                time_index_x += 1
            while time_index_y < len(t_y) and t_y[time_index_y] <= t:
                y_rt.add(value=y[time_index_y], timestamp=t_y[time_index_y])
                time_index_y += 1

            if t > 100:
                plt.plot(x_rt.get()[:, 0], x_rt.get()[:, -1], 'b', linewidth=1.5)
                plt.plot(y_rt.get()[:, 0], y_rt.get()[:, -1], 'g', linewidth=1.5)
                plt.legend(['x', 'y'])
                plt.pause(0.01)
                plt.clf()

                # llr > 0 means that y leads and x follows.
                ll = LeadLag(arr_1_with_ts=y_rt.get(),
                             arr_2_with_ts=x_rt.get(),
                             max_absolute_lag=30,  # +/- @max_absolute_lag seconds.
                             verbose=False)

                # x = np.arange(0, 4 * np.pi, 0.1)
                #
                # while True:
                #     plt.plot(x, [np.random.rand() for i in x], 'g-', linewidth=1.5, markersize=4)
                #     plt.pause(0.01)
                #     plt.clf()

                ll.run_inference(multi_threading=False)
                llr_list.append(ll.llr)
                # print(f'LLR = {np.nanmean(llr_list):.2f}.')
                print(f'i = {t}, '
                      f'lead_lag = {ll.lead_lag}, '
                      f'llr = {ll.llr:.2f}, '
                      f'inference_time = {1000 * ll.inference_time:.1f} ms.')
    else:
        ll = LeadLag(arr_1_with_ts=np.transpose(np.vstack([t_y, y])),
                     arr_2_with_ts=np.transpose(np.vstack([t_x, x])),
                     max_absolute_lag=40,  # +/- @max_absolute_lag seconds.
                     verbose=True)
        ll.run_inference(multi_threading=True)
        print(ll.llr)
        print(ll.lead_lag)
        ll.plot_results()
        ll.plot_data()


if __name__ == '__main__':
    main()
