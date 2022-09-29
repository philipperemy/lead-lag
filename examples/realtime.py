from datetime import timedelta, datetime

import matplotlib.pyplot as plt
import numpy as np

from lead_lag import LeadLag, RealTimeAggregator


class Color:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_data(n):
    plt.ion()
    t_x = np.arange(0, n, 1)
    t_y = np.arange(0, n, 1)

    np.random.seed(124)
    x1 = np.cumsum(np.random.randn(n // 2))
    y1 = np.zeros_like(x1)
    y1[:-2] = x1[2:]  # x is lagging.

    # last 100 ts have a lag of -10 units of time.
    x2 = np.cumsum(np.random.randn(n // 2))
    y2 = np.zeros_like(x1)
    y2[:-5] = x2[5:]  # x is lagging even more.

    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))

    # We want to make something asynchronous.

    def random_num_ts():
        return int(int(3 / 4 * n) + np.random.uniform(low=-n // 5, high=n // 5))

    origin = datetime.utcnow()
    t_x = sorted(np.random.choice(range(len(t_x)), size=random_num_ts(), replace=False))
    t_y = sorted(np.random.choice(range(len(t_y)), size=random_num_ts(), replace=False))
    x = x[t_x]
    y = y[t_y]
    assert not np.isnan(x).any()
    assert not np.isnan(y).any()
    t_x = [origin + timedelta(seconds=a * 0.1) for a in t_x]
    t_y = [origin + timedelta(seconds=a * 0.1) for a in t_y]
    return x, y, t_x, t_y


def main():
    # x is lagging, y is leading.
    # x contains 14,000 randomly sampled points.
    # y contains 8,000 randomly sampled points.
    n = 200
    x, y, t_x, t_y = generate_data(n)

    history_length = n // 4
    x_rt = RealTimeAggregator(history_length)
    y_rt = RealTimeAggregator(history_length)

    timestamps = sorted(set(t_x).union(t_y))
    time_index_x = 0
    time_index_y = 0
    for i, t in enumerate(timestamps):
        while time_index_x < len(t_x) and t_x[time_index_x] <= t:
            x_rt.add(value=x[time_index_x], timestamp=t_x[time_index_x])
            time_index_x += 1
        while time_index_y < len(t_y) and t_y[time_index_y] <= t:
            y_rt.add(value=y[time_index_y], timestamp=t_y[time_index_y])
            time_index_y += 1

        if i > 20:
            xx = x_rt.get()
            yy = y_rt.get()
            plt.plot(xx.index, xx.values, 'b-')
            plt.plot(yy.index, yy.values, 'g-')
            plt.legend(['x', 'y'])
            plt.pause(0.01)
            plt.clf()

            ll = LeadLag(
                ts1=xx,
                ts2=yy,
                max_lag=5,  # +/- @max_absolute_lag seconds.
                verbose=False
            )

            ll.run_inference()
            if ll.llr > 0:  # llr > 0 means that y leads and x follows.
                who_is_leading = f'{Color.OK_GREEN}y is leading{Color.END_C}'
            else:
                who_is_leading = f'{Color.OK_BLUE}x is leading{Color.END_C}'
            print(f'i = {t}, estimated lag = {ll.lead_lag}, llr = {ll.llr:.2f}, {who_is_leading}.')


if __name__ == '__main__':
    main()
