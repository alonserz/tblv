from blessed import Terminal
from tblv.plot import get_plot_string
from tblv.parser import get_x_y_title

border_bl = u"└"
border_br = u"┘"
border_tl = u"┌"
border_tr = u"┐"
border_h = u"─"
border_v = u"│"

def plot_cli(data):
    tags = list(data.keys())

    def display_menu(selection):
        print(term.clear)
        show_plot(selection)
        
    def show_plot(selection):
        x, y, title = get_x_y_title(data, selection)
        plot = get_plot_string(x, y, title, plot_size = (term.width // 1.2, term.height // 1.2))
        splited_string = plot.splitlines()
        string = ""
        for idx, tag in enumerate(tags):
            if idx == selection:
                string += f'\t{term.bold_red_reverse(tag)}\t'
            else:
                string += f'\t{term.normal + tag}\t'
        print(term.center(string))
        print(term.center("\tTip: h/l to move left/right, q to exit"))

        for line in splited_string:
            print(term.center(line))

    term = Terminal()
    selection = 0
    display_menu(selection)

    selection_inprogress = True
    with term.cbreak(), term.hidden_cursor():
        while selection_inprogress:
            key = term.inkey()
            if key.lower() == 'l':
                selection += 1
            if key.lower() == 'h':
                selection -= 1
            if key.lower() == 'q':
                selection_inprogress = False
            selection = selection % len(tags)

            display_menu(selection)
