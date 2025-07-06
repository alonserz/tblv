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
# Keybindings
| Keys                        | Description  |
| --------------              | ------------ | 
| h                           | Move left    |
| l                           | Move right   |
| m ```{arg1}``` ```{arg2}``` | Merge two plots together. ```{arg1}``` ```{arg2}``` are indexes of plots  |
