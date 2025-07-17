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
    parser.add_argument('path', help = 'Path to log file', nargs = '+')
    args = parser.parse_args()
    paths = args.path
    term = Terminal()
    # file parser:
    if all(path.endswith('.0') for path in paths):
        show_plot(term, {path: parse_file(path) for path in paths})
    # dir parser
    else:
        # may be i can open previous menu without while true loop
        while True:
            data = parse_dir(tuple(paths))
            folder_idx, start_pos, end_pos = show_directory_selection_menu(term, data)
            file_path = show_file_selection_menu(term, data, folder_idx, start_pos, end_pos)
            if file_path is None:
                continue
            file_data = parse_multiple_files(file_path)
            show_plot(term, file_data)

if __name__ == '__main__':
    main()
