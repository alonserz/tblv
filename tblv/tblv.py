import argparse
from tblv.parser import (
        parse_file,
        parse_dir,
)
from tblv.cli import (
        show_plot,
        show_directory_selection_menu,
        show_file_selection_menu,
)

def main():
    parser = argparse.ArgumentParser(prog = 'tblv')
    parser.add_argument('path', help = 'Path to log file')
    args = parser.parse_args()
    path = args.path

    # file parser:
    if path.endswith('.0'):
        data = parse_file(path)
        show_plot(data)
    # dir parser
    else:
        # may be i can open previous menu without while true loop
        while True:
            data = parse_dir(path)
            folder_idx = show_directory_selection_menu(data)
            file_path = show_file_selection_menu(data, folder_idx)
            if file_path is None:
                continue
            file_data = parse_file(file_path)
            show_plot(file_data)

if __name__ == '__main__':
    main()
