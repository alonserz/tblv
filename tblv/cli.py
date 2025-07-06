from blessed import Terminal
from tblv.plot import get_plot_string
from tblv.parser import get_x_y_title

def plot_cli(data):
    tags = list(data.keys())

    def display(**kwargs):
        print(term.clear)
        show_plot(**kwargs)
        
    def show_plot(**kwargs):
        plots_data = []
        title = ""
        
        for selection in kwargs:
            x, y, title_ = get_x_y_title(data, kwargs[selection])
            title += title_
            plots_data.append((x, y, title_))

        # unpack plots_data to provide it as tuples
        plot = get_plot_string(*plots_data, title = title, plot_size = (term.width, term.height // 1.1))
        string = ""
        selection = kwargs['selection']
        for idx, tag in enumerate(tags):
            if idx == selection:
                string += f'\t[{idx}] {term.bold_red_reverse(tag)}\t'
            else:
                string += f'\t[{idx}] {term.normal + tag}\t'

        print(term.center(string))
        print(term.center(plot))
        
    term = Terminal()
    selection = 0
    display(selection = selection)

    selection_inprogress = True
    with term.cbreak(), term.hidden_cursor():
        while selection_inprogress:
            key = term.inkey()
            if key.lower() == 'l':
                selection += 1
                selection = selection % len(tags)
                display(selection = selection)
            elif key.lower() == 'h':
                selection -= 1
                selection = selection % len(tags)
                display(selection = selection)
            elif key.lower() == 'm':
                # Unable to enter two-digit numbers
                # TODO: support two-digit numbers
                key1 = term.inkey()
                key2 = term.inkey()
                display(selection = int(key1), selection1 = int(key2))
            elif key.lower() == 'q':
                selection_inprogress = False
