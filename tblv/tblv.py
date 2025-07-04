import argparse
from tblv.parser import parse
from tblv.cli import plot_cli

def main():
    parser = argparse.ArgumentParser(prog = 'tblv')
    parser.add_argument('file_path', help = 'Path to log file')

    args = parser.parse_args()
    path = args.file_path

    data = parse(path)
    plot_cli(data)

if __name__ == '__main__':
    main()

