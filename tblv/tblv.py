import argparse
from tblv.parser import (
        parse_file,
        parse_dir,
        parse_multiple_files,
)
from tblv.cli import (
        show_plot,
        show_directory_selection_menu,
        show_file_selection_menu,
)
from blessed import Terminal

def main():
    parser = argparse.ArgumentParser(prog = 'tblv')
    parser.add_argument('path', help = 'Path to log file')
    args = parser.parse_args()
    path = args.path
    term = Terminal()
    # file parser:
    if path.endswith('.0'):
        data = parse_file(path)
        show_plot(term, {path: data})
    # dir parser
    else:
        # may be i can open previous menu without while true loop
        while True:
            data = parse_dir(path)
            folder_idx, start_pos, end_pos = show_directory_selection_menu(term, data)
            file_path = show_file_selection_menu(term, data, folder_idx, start_pos, end_pos)
            if file_path is None:
                continue
            file_data = parse_multiple_files(file_path)
            show_plot(term, file_data)

if __name__ == '__main__':
    main()
