from tblv.keybindings import *
from tblv.parser import get_x_y_title
from tblv.plot import get_plot_string

SELECTED_FILES = []
SELECTED_PLOTS = []

def handle_input(term):
    move_number = ''
    last_key = None
    while True:
        key = term.inkey()
        if not key.isdigit():
            last_key = key
            break
        else:
            move_number += str(key)
    if move_number == '':
        move_number = '1'
    return int(move_number), last_key

# Shows plot
def show_plot(term, data):
    def display(args, start_pos, end_pos):
        # Shows selected plot
        plots_data = []
        title_list = []
        # TODO: Fix string when too many files opened at same time
        files_name_string = ''.join((
            f'\t[{int(idx) + start_pos}] {term.bold_green_reverse(filename)}\t' if idx + start_pos == selected_file_idx
            else f'\t[{term.normal + str(int(idx) + start_pos)}]\t'
            for idx, filename in enumerate(files[start_pos:end_pos])
        ))
        for selection in args:
            if selection is None:
                continue
            x, y, title = get_x_y_title(data, selection[0], selection[1])
            title_list.append(title)
            plots_data.append((x, y, title))

        title = ' and '.join(title_list)
        # unpack plots_data to provide it as tuples
        plot = get_plot_string(*plots_data, title = title, plot_size = (term.width, term.height // 1.1))
        selection = args[0][1]
        plots_name = ''.join((
            f'\t[{idx}] {term.bold_green_reverse(tag)}\t' if idx == selection
            else f'\t[{idx}] {term.normal + tag}\t'
            for idx, tag in enumerate(tags)
        ))
        print(term.clear + term.center(files_name_string) + '\n' + term.center(plots_name) + '\n' + term.center(plot))

    selected_plot_idx = 0
    selected_file_idx = 0
    start_pos = 0
    end_pos = 3
    selected = ((selected_file_idx, selected_plot_idx),)
    selection_inprogress = True
    files = list(data.keys())
    tags = data[files[selected_file_idx]]
    display(selected, start_pos, end_pos)
    with term.cbreak(), term.hidden_cursor():
        # Plot selection
        while selection_inprogress:
            key = term.inkey()
            if key == KEY_MOVE_RIGHT:
                selected_plot_idx += 1
                selected_plot_idx = selected_plot_idx % len(tags)
                selected = ((selected_file_idx, selected_plot_idx),)
            elif key == KEY_MOVE_LEFT:
                selected_plot_idx -= 1
                selected_plot_idx = selected_plot_idx % len(tags)
                selected = ((selected_file_idx, selected_plot_idx),)
            elif key == KEY_MERGE:
                # Unable to enter two-digit numbers
                # TODO: support two-digit numbers
                key1 = term.inkey()
                key2 = term.inkey()
                selected = ((selected_file_idx, key1), (selected_file_idx, key2),)
            elif key == KEY_MOVE_NEXT_FILE:
                selected_file_idx += 1
                selected_file_idx = selected_file_idx % len(files)
                selected = ((selected_file_idx, selected_plot_idx),)
            elif key == KEY_MOVE_PREVIOUS_FILE:
                selected_file_idx -= 1
                selected_file_idx = selected_file_idx % len(files)
                selected = ((selected_file_idx, selected_plot_idx),)
            elif key == KEY_SELECT_PLOT_TO_MERGE:
                SELECTED_PLOTS.append((selected_file_idx, selected_plot_idx))
            elif key in KEY_SELECT:
                selected = SELECTED_PLOTS.copy()
                SELECTED_PLOTS.clear()
            elif key == KEY_QUIT:
                selection_inprogress = False

            start_pos = selected_file_idx - 3 if (selected_file_idx - 3) >= 0 else 0
            end_pos = selected_file_idx + 3 if(selected_file_idx + 3) <= len(files) else len(files)
            display(selected, start_pos, end_pos)

# Shows menu to choose file
def show_directory_selection_menu(term, data):
    # Shows all folders, when hover on it shows all files in this folder
    def is_selected(filepath):
        return filepath in SELECTED_FILES

    def display(selection, start_pos, end_pos):
        string = ''.join((
            f'[{idx + start_pos}] {term.bold_green_reverse(folder)}\n' + ''.join(( # show chosen folder as selected
                f'\t [{checkmark if is_selected(f"{folder}/{file}") else idx}] {file}\n' #show files of chosen folder
                for idx, file in enumerate(data[folder]) # iterate through all files in folder
            )) if idx + start_pos == selection 
            else f'[{idx + start_pos}] {term.normal + folder}\t\n' # show non-selected folders
            for idx, folder in enumerate(folders[start_pos:end_pos]) # iterate through batch of folders
        ))

        print(term.clear + string)
    
    # When you select folder moves selection to file which this folder contains
    
    selection = 0
    term_lines = term.height // 2
    start_pos = 0
    end_pos = term_lines 
    folders = list(data.keys())
    checkmark = '✓'
    display(selection, start_pos, end_pos)
    with term.cbreak(), term.hidden_cursor():
        # Loop while folder isn't selected
        while True:
            move_number, key = handle_input(term)
            if key == KEY_MOVE_DOWN:
                if move_number > 1 and move_number >= len(folders) - selection:
                    selection = len(folders) - 1
                else:
                    selection += move_number
                    selection = selection % len(folders)
            elif key == KEY_MOVE_UP:
                if move_number > 1 and move_number >= selection: # if you move like 100 lines up will select first one
                    selection = 0
                else:
                    selection -= move_number
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

def show_file_selection_menu(term, data, idx, start_pos, end_pos):
    def is_selected(filepath):
        return filepath in SELECTED_FILES

    def display(selection_file, selected_folder_idx):
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
            else f'\t [{checkmark if is_selected(f"{folder_by_idx}/{file}") else idx}] {term.normal + file}\n'
            for idx, file in enumerate(data[folders[selected_folder_idx]]) 
        ))
        # Shows rest of folders
        strings.append(''.join(
            f'[{idx}] {folders[idx]}\n'
            for idx in range(selected_folder_idx + 1, len(folders[:end_pos]))
        ))
        string = ''.join(strings)

        print(term.clear + string)

    folders = list(data.keys())
    folder_by_idx = folders[idx]
    selection = 0
    checkmark = '✓'
    global SELECTED_FILES
    display(selection, idx)
    # Loop while file isn't selected
    with term.hidden_cursor(), term.cbreak():
        while True:
            move_number, key = handle_input(term)
            if key == KEY_MOVE_DOWN:
                if move_number > 1 and move_number >= len(data[folder_by_idx]) - selection:
                    selection = len(data[folder_by_idx]) - 1
                else:
                    selection += move_number 
                    selection = selection % len(data[folder_by_idx])
            elif key == KEY_MOVE_UP:
                if move_number > 1 and move_number >= selection:
                    selection = 0
                else:
                    selection -= move_number 
                    selection = selection % len(data[folder_by_idx])
            elif key == KEY_MOVE_BOTTOM:
                selection = len(data[folder_by_idx])
                selection = selection - 1 % len(data[folder_by_idx])
            elif key == KEY_MOVE_TOP:
                selection = 0
                selection = selection % len(data[folder_by_idx])
            elif key == KEY_MULTIPLE_FILES_SELECTION:
                filepath = f'{folder_by_idx}/{data[folder_by_idx][selection]}'
                if not is_selected(filepath): SELECTED_FILES.append(filepath) 
            elif key == KEY_REMOVE_SELECTED_FILE:
                filepath = f'{folder_by_idx}/{data[folder_by_idx][selection]}'
                if is_selected(filepath): SELECTED_FILES.remove(filepath) 
            elif key in KEY_SELECT:
                SELECTED_FILES.append(f'{folder_by_idx}/{data[folder_by_idx][selection]}')
                _ = SELECTED_FILES.copy()
                SELECTED_FILES.clear()
                return set(_)
            elif key == KEY_QUIT:
                return None
            display(selection, idx)
