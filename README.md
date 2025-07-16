# tblv
TensorBoard Log Viewer

# Quick Start

- Linux
```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
tblv tblv/runs/segmentation.0
```
- Windows
```
python -m venv .venv
call .venv/Scripts/activate
pip install -e .
tblv tblv/runs/segmentation.0
```
# Default Keybindings
| Keys                          | Description                                                               |
| --------------                | ------------                                                              | 
| `h`                           | Select next plot                                                          |
| `l`                           | Select previous plot                                                      |
| `{number}j`                   | Go `{number}` folders/files down. Default is 1                            |
| `{number}k`                   | Go `{number}` folders/files up. Default is 1                              |
| `g`                           | Move to first line of selection                                           |
| `G`                           | Move to last line of selection                                            |
| `m`  `{arg1` `{arg2}`         | Merge two plots together. `{arg1}` `{arg2}` are indexes of plots          |
| `s`                           | Mark file as selected. To show plots of selected files press `Enter`      |
| `Enter`                       | Select folder/file                                                        |
| `q`                           | Quit/Open previous menu                                                   |

To change default keybindings edit ```tblv/keybindings.py```
