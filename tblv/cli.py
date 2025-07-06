from blessed import Terminal
from tblv.plot import (
        get_plot_string,
        get_multiple_datasets_plot_string
)
from tblv.parser import get_x_y_title

border_bl = u"└"
border_br = u"┘"
border_tl = u"┌"
border_tr = u"┐"
border_h = u"─"
border_v = u"│"

def plot_cli(data):
    tags = list(data.keys())

    def display_menu(selection, selection2 = None):
        print(term.clear)
        show_plot(selection, selection2)
        
    def show_plot(selection, selection2 = None):
        if selection2 is None:
            x, y, title = get_x_y_title(data, selection)
            plot = get_plot_string(x, y, title, plot_size = (term.width, term.height // 1.1))
        else:
            x1, y1, title1 = get_x_y_title(data, selection)
            x2, y2, title2 = get_x_y_title(data, selection2)
            title = f"Merge: {title1} and {title2}"
            plot = get_multiple_datasets_plot_string(x1, y1, x2, y2, title, plot_size = (term.width, term.height // 1.1))
        string = ""
        for idx, tag in enumerate(tags):
            if idx == selection:
                string += f'\t[{idx}] {term.bold_red_reverse(tag)}\t'
            else:
                string += f'\t[{idx}] {term.normal + tag}\t'

        print(term.center(string))
        print(term.center("\tTip: h/l to move left/right, q to exit"))
        print(term.center(plot))
        
    term = Terminal()
    selection = 0
    display_menu(selection)

    selection_inprogress = True
    with term.cbreak(), term.hidden_cursor():
        while selection_inprogress:
            key = term.inkey()
            if key.lower() == 'l':
                selection += 1
                selection = selection % len(tags)
                display_menu(selection)
            elif key.lower() == 'h':
                selection -= 1
                selection = selection % len(tags)
                display_menu(selection)
            elif key.lower() == 'm':
                # Unable to enter two-digit numbers
                key1 = term.inkey()
                key2 = term.inkey()
                display_menu(int(key1), int(key2))
            elif key.lower() == 'q':
                selection_inprogress = False
