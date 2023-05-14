# CYD - Cli Yml Reader

## Description
A program to read .yml/.yaml files specified by the arguments that are passed to the command line, built using Typer.

## Installation

Download the source code, run `python app.py`.

## Usage

The app will not run by itself, it needs one of the two commands passed:

- `list` with arguments `tasks` or `builds` to list all of the available tasks or builds from .yml(.yaml) files. An option `--path` enables to set an absoulte path to the folder containing those files. By default the files are set to be located in the same directory where the `app.py` file is.
- `get` with argumetns `tasks` or `builds` and `<name>` to get information about specific task or build. An option `--path` enables to set an absoulte path to the folder containing those files. By default the files are set to be located in the same directory where the `app.py` file is.

## Examples

- Command line: `python app.py get task train_silver_centaurs --path "D:\Projects\Python\Jun Saber\program"`
- Output:
```
Task info:
- name: train_silver_centaurs
- dependencies: design_black_centaurs, upgrade_blue_centaurs, train_silver_centaurs
```

- Command line: `python app.py get build train_silver_centaurs --path "D:\Projects\Python\Jun Saber\program"`
- Output:
```
Error: no such build
```

- Command line: `python app.py get build audience_stand`
- Output:
```
Build info:
- name: audience_stand
- tasks: enable_fuchsia_fairies, read_blue_witches, upgrade_olive_gnomes
```

- Command line: `python app.py list build`
- Output:
```
Error: unexpected argument, should be 'builds' or 'tasks'
```

- Command line: `python app.py list builds`
- Output:
```
List of available builds:
- approach_important
- audience_stand
- time_alone
```
