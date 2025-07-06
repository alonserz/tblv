import plotext as plt
from functools import lru_cache

@lru_cache()
def get_plot_string(x, y, title = 'Plot', theme = 'dark', plot_size = None):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel('Epochs')
    plt.ylabel('Metric values')
    plt.theme(theme)
    if plot_size is not None:
        plt.plot_size(plot_size[0], plot_size[1])
    plt.limit_size(True, True)
    plot_string = plt.build()
    plt.cld()
    return plot_string

@lru_cache()
def get_multiple_datasets_plot_string(x1, y1, x2, y2, title = 'Plot', theme = 'dark', plot_size = None):
    plt.plot(x1, y1)
    plt.plot(x2, y2)
    plt.title(title)
    plt.xlabel('Epochs')
    plt.ylabel('Metric values')
    plt.theme(theme)
    if plot_size is not None:
        plt.plot_size(plot_size[0], plot_size[1])
    plt.limit_size(True, True)
    plot_string = plt.build()
    plt.cld()
    return plot_string

