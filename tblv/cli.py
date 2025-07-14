from blessed import Terminal
from tblv.keybindings import (
    KEY_MERGE,
    KEY_MOVE_LEFT,
    KEY_MOVE_RIGHT,
    KEY_MOVE_DOWN,
    KEY_MOVE_UP,
    KEY_SELECT,
    KEY_QUIT,
    KEY_MOVE_BOTTOM,
    KEY_MOVE_TOP
)
from tblv.parser import get_x_y_title
from tblv.plot import get_plot_string


# Shows plot
def show_plot(data):
    tags = list(data.keys())

    def display(*args):
        print(term.clear)
        # Shows selected plot
        plots_data = []
        title_list = []
        for selection in args:
            if selection is None:
                continue
            x, y, title_ = get_x_y_title(data, selection)
            title_list.append(title_)
            plots_data.append((x, y, title_))

        title = ' and '.join(title_list)
        # unpack plots_data to provide it as tuples
        plot = get_plot_string(*plots_data, title = title, plot_size = (term.width, term.height // 1.1))
        selection = args[0]
        string = ''.join((
            f'\t[{idx}] {term.bold_green_reverse(tag)}\t' if idx == selection
            else f'\t[{idx}] {term.normal + tag}\t'
            for idx, tag in enumerate(tags)
        ))

        print(term.center(string))
        print(term.center(plot))

    term = Terminal()
    selection = 0
    selected = (0, None)

    display(*selected)
    selection_inprogress = True
    with term.cbreak(), term.hidden_cursor():
        # Plot selection
        while selection_inprogress:
            key = term.inkey()
            if key == KEY_MOVE_RIGHT:
                selection += 1
                selection = selection % len(tags)
                selected = (selection, None)
            elif key == KEY_MOVE_LEFT:
                selection -= 1
                selection = selection % len(tags)
                selected = (selection, None)
            elif key == KEY_MERGE:
                # Unable to enter two-digit numbers
                # TODO: support two-digit numbers
                key1 = term.inkey()
                key2 = term.inkey()
                selected = (key1, key2)
            elif key == KEY_QUIT:
                selection_inprogress = False
            display(*selected)

dir_cached_strings = {}
# Shows menu to choose file
def show_directory_selection_menu(data):
    # Shows all folders, when hover on it shows all files in this folder
    def display(selection, start_pos, end_pos):
        print(term.clear)
        global dir_cached_string
        if selection not in dir_cached_strings:
            string = ''.join((
                f'[{idx + start_pos}] {term.bold_green_reverse(folder)}\n' + ''.join(( # show chosen folder as selected
                    f'\t [{idx}] {file}\n' #show files of chosen folder
                    for idx, file in enumerate(data[folder]) # iterate through all files in folder
                )) if idx + start_pos == selection 
                else f'[{idx + start_pos}] {term.normal + folder}\t\n' # show non-selected folders
                for idx, folder in enumerate(folders[start_pos:end_pos]) # iterate through batch of folders
            ))

            dir_cached_strings[selection] = string
        print(dir_cached_strings[selection])
    
    # When you select folder moves selection to file which this folder contains
    
    term = Terminal()
    selection = 0
    term_lines = term.height // 2
    start_pos = 0
    end_pos = term_lines 
    folders = list(data.keys())
    display(selection, start_pos, end_pos)
    with term.cbreak(), term.hidden_cursor():
        # Loop while folder isn't selected
        while True:
            key = term.inkey()
            if key == KEY_MOVE_DOWN:
                selection += 1
                selection = selection % len(folders)
            elif key == KEY_MOVE_UP:
                selection -= 1
                selection = selection % len(folders)
            elif key == KEY_MOVE_BOTTOM:
                selection = len(folders)
                selection = selection - 1 % len(folders)
            elif key == KEY_MOVE_TOP:
                selection = 0
                selection = selection % len(folders)
            elif key in KEY_SELECT:
                return selection, start_pos, end_pos
            elif key == KEY_QUIT:
                exit()
            start_pos = selection - term_lines if (selection - term_lines) >= 0 else 0
            end_pos = selection + term_lines if(selection + term_lines) <= len(folders) else len(folders)
            display(selection, start_pos, end_pos)

file_cached_string = {}
def show_file_selection_menu(data, idx, start_pos, end_pos):
    def display(selection_file, selected_folder_idx):
        print(term.clear)
        global file_cached_string
        if selected_folder_idx not in file_cached_string:
            file_cached_string[selected_folder_idx] = {}
        if selection_file not in file_cached_string[selected_folder_idx]:
            # Top of folders (before selected one)
            strings = []
            strings.append(''.join(
                f'[{idx + start_pos}] {folder}\n'
                for idx, folder in enumerate(folders[start_pos:end_pos])
                if idx + start_pos <= selected_folder_idx
            ))
            # show files
            strings.append(''.join(
                f'\t [{idx}] {term.bold_green_reverse(file)}\n' if idx == selection_file
                else f'\t [{idx}] {term.normal + file}\n'
                for idx, file in enumerate(data[folders[selected_folder_idx]]) 
            ))
            # Shows rest of folders
            strings.append(''.join(
                f'[{idx}] {folders[idx]}\n'
                for idx in range(selected_folder_idx + 1, len(folders[:end_pos]))
            ))
            string = ''.join(strings)
            file_cached_string[selected_folder_idx][selection_file] = string

        print(file_cached_string[selected_folder_idx][selection_file])

    folders = list(data.keys())
    folder_by_idx = folders[idx]
    term = Terminal()
    selection = 0
    display(selection, idx)
    # Loop while file isn't selected
    with term.hidden_cursor(), term.cbreak():
        while True:
            key = term.inkey()
            if key == KEY_MOVE_DOWN:
                selection += 1
                selection = selection % len(data[folder_by_idx])
            elif key == KEY_MOVE_UP:
                selection -= 1
                selection = selection % len(data[folder_by_idx])
            elif key == KEY_MOVE_BOTTOM:
                selection = len(data[folder_by_idx])
                selection = selection - 1 % len(data[folder_by_idx])
            elif key == KEY_MOVE_TOP:
                selection = 0
                selection = selection % len(data[folder_by_idx])
            elif key in KEY_SELECT:
                return folder_by_idx + f'/{data[folder_by_idx][selection]}'
            elif key == KEY_QUIT:
                return None
            display(selection, idx)
