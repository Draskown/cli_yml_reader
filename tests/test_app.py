import os
import pytest
from program.app import list_entries, get_dependencies, get_entry, folder_correct, file_exists

#region Folder tests
# Test when folder exists
def test_folder_correct_exists(tmp_path):
    # Create temporary folder
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()
    # Check if the output is correct
    assert folder_correct(str(folder_path)) == True

# Test when folder does not exists
def test_folder_correct_not_exists(capsys):
    # Try non-existing folder
    assert folder_correct("non_existing_folder") == False
    captured = capsys.readouterr()
    # Check if the output is correct
    assert captured.out == "Error: folder does not exist\n"

# Test when folder path is empty
def test_folder_correct_empty_path():    
    assert folder_correct("") == True
#endregion

#region File tests
# Define correct .yml file fixture
@pytest.fixture
def correct_file_yml(tmpdir):
    # Create a temporary .yml file
    correct_file = tmpdir.join("correct.yml")
    correct_file.write("")
    # Return the temporary .yml file
    yield str(correct_file)

# Test when file exists
def test_file_exists_yml(correct_file_yml):
    # Check if the output is correct
    assert file_exists(os.path.basename(correct_file_yml)[:-4],
                       os.path.dirname(correct_file_yml)+"\\") == True

# Test when file does not exists
def test_file_not_exists_yml(capsys, tmp_path):
    # Check if the output is correct
    assert file_exists(os.path.basename("not_correct.yml")[:-4],
                       str(tmp_path)+"\\") == False
    captured = capsys.readouterr()
    assert captured.out == "Error: file does not exist not_correct.yml(.yaml)\n"

# Define correct .yaml file fixture
@pytest.fixture
def correct_file_yaml(tmpdir):
    # Create a temporary .yml file
    correct_file = tmpdir.join("correct.yaml")
    correct_file.write("")
    # Return the temporary .yml file
    yield str(correct_file)

# Test when file exists
def test_file_exists_yaml(correct_file_yaml):
    # Check if the output is correct
    assert file_exists(os.path.basename(correct_file_yaml)[:-5],
                       os.path.dirname(correct_file_yaml)+"\\") == True

# Test when file does not exists
def test_file_not_exists_yaml(capsys, tmp_path):
    # Check if the output is correct
    assert file_exists(os.path.basename("not_correct.yaml")[:-5],
                       str(tmp_path)+"\\") == False
    captured = capsys.readouterr()
    assert captured.out == "Error: file does not exist not_correct.yml(.yaml)\n"
#endregion

#region List tasks tests
# Define correct tasks fixture
@pytest.fixture
def correct_file(tmpdir):
    # Create a temporary tasks.yml file
    tasks_file = tmpdir.join("tasks.yml")
    # Fill the temporary tasks.yml file
    tasks_file.write(
        """
        tasks:
          - name: Task 1
            dependencies: Do something
          - name: Task 2
            dependencies: Do something else
        """
    )
    # Return the temporary tasks.yml file
    yield str(tasks_file)

# Test when the file is correct
def test_list_tasks_correct(capsys, correct_file):
    # Call the function to list tasks
    list_entries("tasks", os.path.dirname(correct_file)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "List of available tasks:\n- Task 1\n- Task 2\n"

# Define empty tasks fixture
@pytest.fixture
def empty_tasks_file(tmpdir):
    # Create a temporary tasks.yml file
    tasks_file = tmpdir.join("tasks.yml")
    # Fill the temporary tasks.yml file
    tasks_file.write(
        """
        tasks:
        """
    )
    # Return the temporary tasks.yml file
    yield str(tasks_file)

# Test when the file is empty
def test_list_tasks_empty_file(capsys, empty_tasks_file):
    # Call the function to list tasks
    list_entries("tasks", os.path.dirname(empty_tasks_file)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "There are no tasks\n"
#endregion

#region List build tests
# Define correct builds fixture
@pytest.fixture
def correct_builds_file(tmpdir):
    # Create a temporary builds.yml file
    builds_file = tmpdir.join("builds.yml")
    # Fill a temporary builds.yml file
    builds_file.write(
        """
        builds:
          - name: Build 1
            description: Build something
          - name: Build 2
            description: Build something else
        """
    )
    # Return a temporary builds.yml file
    yield str(builds_file)

# Test when the file is correct
def test_list_builds_correct(capsys, correct_builds_file):
    # Call the function to list builds
    list_entries("builds", os.path.dirname(correct_builds_file)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "List of available builds:\n- Build 1\n- Build 2\n"

# Define correct builds fixture
@pytest.fixture
def empty_builds_file(tmpdir):
    # Create a temporary builds.yml file
    builds_file = tmpdir.join("builds.yml")
    # Fill a temporary builds.yml file
    builds_file.write(
        """
        builds:
        """
    )
    # Return a temporary builds.yml file
    yield str(builds_file)

# Test when the file is correct
def test_list_builds_empty(capsys, empty_builds_file):
    # Call the function to list builds
    list_entries("builds", os.path.dirname(empty_builds_file)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "There are no builds\n"
#endregion

