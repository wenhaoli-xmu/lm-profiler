from pygments import console
import numpy as np


class Dummy:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_type(exc_val)
        

LOG_HISTORY = set()


def profile_log(info, **kwargs):
    print(console.colorize("yellow", "profile: ") + f"{info}", **kwargs)


def profile_log_once(info, **kwargs):
    if info in LOG_HISTORY:
        return
    LOG_HISTORY.add(info)
    profile_log(info, **kwargs)


def remove_outliers(data):
    data = np.array(data)
    mean = np.mean(data)
    std = np.std(data)
    filtered_data = [x for x in data if (mean - 3 * std) <= x <= (mean + 3 * std)]
    return filtered_data