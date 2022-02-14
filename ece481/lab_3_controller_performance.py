import numpy as np


def get_controller_performance(rising_start=6, falling_start=12):
    t = np.loadtxt('t.txt')
    y = np.loadtxt('y.txt')
    t_1 = min(np.argwhere(t >= rising_start).flatten())
    t_2 = min(np.argwhere(t >= falling_start).flatten())

    overshoot_rising = max(0, 100 * (max(y[t_1:t_2 - 1]) - 25) / 15)
    overshoot_rising = np.round(overshoot_rising, decimals=3)
    print(f'Max Overshoot (rising): {overshoot_rising}%')

    overshoot_falling = max(0, 100 * (10 - min(y[t_2:])) / 15)
    overshoot_falling = np.round(overshoot_falling, decimals=3)
    print(f'Max Overshoot (falling): {overshoot_falling}%')

    outside_two_percent_rising = np.logical_or(
        y[t_1:t_2 - 1] > 25 + 0.02 * 15,
        y[t_1:t_2 - 1] < 25 - 0.02 * 15)
    overshoot_index_rising = \
        max(np.argwhere(outside_two_percent_rising).flatten())
    settling_time_rising = t[overshoot_index_rising + t_1] - rising_start
    settling_time_rising = np.round(settling_time_rising, decimals=3)
    print(f'2% Settling Time (rising): {settling_time_rising}s')

    outside_two_percent_falling = np.logical_or(
        y[t_2:] > 10 + 0.02 * 15,
        y[t_2:] < 10 - 0.02 * 15)
    overshoot_index_falling = \
        max(np.argwhere(outside_two_percent_falling).flatten())
    settling_time_falling = t[overshoot_index_falling + t_2] - falling_start
    settling_time_falling = np.round(settling_time_falling, decimals=3)
    print(f'2% Settling Time (falling): {settling_time_falling}s')


if __name__ == '__main__':
    get_controller_performance()
