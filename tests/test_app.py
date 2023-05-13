import os
import io
import sys
import yaml
from typer.testing import CliRunner
from program.app import list_entries, get_dependencies, get_entry, folder_correct

def test_folder_correct_exists(tmp_path):
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()
    assert folder_correct(str(folder_path)) == True

def test_folder_correct_not_exists(capsys):
    assert folder_correct("non_existing_folder") == False
    captured = capsys.readouterr()
    assert captured.out == "Error: folder does not exists\n"

def test_folder_correct_empty_path():    
    assert folder_correct("") == True
