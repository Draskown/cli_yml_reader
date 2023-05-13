import os
import io
import sys
import yaml
from typer.testing import CliRunner
from program.app import list_entries, get_dependencies, get_entry, folder_correct


# Test if list_entries() function works as expected
def test_list_entries(tmp_path):
    # Create a test file
    with open(os.path.join(tmp_path, "tasks.yml"), "w") as f:
        data = {"tasks": [{"name": "task1"}, {"name": "task2"}]}
        yaml.dump(data, f)
    # Test that list_entries() function returns the correct output
    assert list_entries("task", str(tmp_path) + "/") == "- task1\n- task2\n"


# Test if get_dependencies() function works as expected
def test_get_dependencies(tmp_path):
    # Create a test file
    with open(os.path.join(tmp_path, "tasks.yml"), "w") as f:
        data = {"tasks": [{"name": "task1", "dependencies": ["task2", "task3"]}, {"name": "task2", "dependencies": []}]}
        yaml.dump(data, f)
    # Test that get_dependencies() function returns the correct output
    assert get_dependencies("task1", str(tmp_path) + "/") == "task2, task3, task1, "
