from blessed import Terminal
from tblv.keybindings import (
    KEY_MERGE,
    KEY_MOVE_LEFT,
    KEY_MOVE_RIGHT,
    KEY_MOVE_DOWN,
    KEY_MOVE_UP,
    KEY_SELECT,
    KEY_QUIT,
)
from tblv.parser import get_x_y_title
from tblv.plot import get_plot_string


# Shows plot
def show_plot(data):
    tags = list(data.keys())

    def display(**kwargs):
        print(term.clear)
        # Shows selected plot
        plots_data = []
        title = ""
        
        for idx, selection in enumerate(kwargs):
            x, y, title_ = get_x_y_title(data, kwargs[selection])
            title += title_
            if idx < len(kwargs) - 1:
                title += " and "
            plots_data.append((x, y, title_))

        # unpack plots_data to provide it as tuples
        plot = get_plot_string(*plots_data, title = title, plot_size = (term.width, term.height // 1.1))
        string = ""
        selection = kwargs['selection']
        for idx, tag in enumerate(tags):
            if idx == selection:
                string += f'\t[{idx}] {term.bold_green_reverse(tag)}\t'
            else:
                string += f'\t[{idx}] {term.normal + tag}\t'

        print(term.center(string))
        print(term.center(plot))

    term = Terminal()
    selection = 0
    display(selection = selection)

    selection_inprogress = True
    with term.cbreak(), term.hidden_cursor():
        # Plot selection
        while selection_inprogress:
            key = term.inkey()
            if key.lower() == KEY_MOVE_RIGHT:
                selection += 1
                selection = selection % len(tags)
                display(selection = selection)
            elif key.lower() == KEY_MOVE_LEFT:
                selection -= 1
                selection = selection % len(tags)
                display(selection = selection)
            elif key.lower() == KEY_MERGE:
                # Unable to enter two-digit numbers
                # TODO: support two-digit numbers
                key1 = term.inkey()
                key2 = term.inkey()
                display(selection = int(key1), selection1 = int(key2))
            elif key.lower() == KEY_QUIT:
                selection_inprogress = False

# Shows menu to choose file
def show_directory_selection_menu(data):
    # Shows all folders, when hover on it shows all files in this folder
    def display(data, selection, choose_files = False):
        print(term.clear)
        string = ''
        for idx, folder in enumerate(data):
            if idx == selection:
                string += f'[{idx}] {term.bold_green_reverse(folder)}\n'
                # Shows all files in folder
                for idx, file in enumerate(data[folder]):
                    string += f'\t [{idx}] {file}\n'
            else:
                string += f'[{idx}] {term.normal + folder}\t\n'
        print(string)
    
    # When you select folder moves selection to file which this folder contains
    
    term = Terminal()
    selection = 0
    folders = list(data.keys())

    display(data, selection)
    with term.cbreak(), term.hidden_cursor():
        # Loop while folder isn't selected
        while True:
            key = term.inkey()
            if key.lower() == KEY_MOVE_DOWN:
                selection += 1
                selection = selection % len(folders)
                display(data, selection)
            elif key.lower() == KEY_MOVE_UP:
                selection -= 1
                selection = selection % len(folders)
                display(data, selection)
            elif key.lower() == KEY_SELECT:
                return selection
            elif key.lower() == KEY_QUIT:
                exit()

def show_file_selection_menu(data, idx):
    def display(data, selection_file, selected_folder_idx):
        print(term.clear)
        string = ''
        idx_ = 0
        # Top of folders (before selected one)
        for idx, folder in enumerate(data):
            string += f'[{idx}] {folder}\n'
            if idx == selected_folder_idx:
                idx_ = idx 
                break
        # Selected folder and files in it
        for idx, file in enumerate(data[folder_by_idx]):
            if idx == selection_file:
                string += f'\t [{idx}] {term.bold_green_reverse(file)}\n'
            else:
                string += f'\t [{idx}] {term.normal + file}\n'
        # Shows rest of folders
        for idx in range(idx_ + 1, len(list(data.keys()))):
            string += f'[{idx}] {list(data.keys())[idx]}\n'

        print(string)

    folder_by_idx = list(data.keys())[idx]
    term = Terminal()
    selection = 0
    display(data, selection, idx)
    # Loop while file isn't selected
    with term.hidden_cursor(), term.cbreak():
        while True:
            key = term.inkey()
            if key.lower() == KEY_MOVE_DOWN:
                selection += 1
                selection = selection % len(data[folder_by_idx])
                display(data, selection, idx)
            elif key.lower() == KEY_MOVE_UP:
                selection -= 1
                selection = selection % len(data[folder_by_idx])
                display(data, selection, idx)
            elif key.lower() == KEY_SELECT:
                return folder_by_idx + f'/{data[folder_by_idx][selection]}'
            elif key.lower() == KEY_QUIT:
                return None
