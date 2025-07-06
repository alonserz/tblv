import plotext as plt
from functools import lru_cache

@lru_cache()
def get_plot_string(*args, title = 'Plot', theme = 'dark', plot_size = None):
    for plot in args:
        x, y, title_ = plot[0], plot[1], plot[2]
        # label argument cause IndexError if x and y are empty
        if len(x) == len(y) == 0:
            plt.plot(x, y)
        else:
            plt.plot(x, y, label = title_)
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
