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
| Keys                        | Description                                                               |
| --------------              | ------------                                                              | 
| h                           | Select next plot                                                          |
| l                           | Select previous plot                                                      |
| j                           | Select next folder/file                                                   |
| k                           | Select previous folder/file                                               |
| g                           | Move to first line of selection                                           |
| G                           | Move to last line of selection                                            |
| m ```{arg1}``` ```{arg2}``` | Merge two plots together. ```{arg1}``` ```{arg2}``` are indexes of plots  |
| Enter                       | Select folder/file                                                        |
| q                           | Quit/Open previous menu                                                   |

To change default keybindings edit ```tblv/keybindings.py```
