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
    assert folder_correct(str(folder_path)) == (str(folder_path)+"\\", False)

# Test when folder does not exists
def test_folder_correct_not_exists(capsys):
    # Try non-existing folder
    assert folder_correct("non_existing_folder") == (None, True)
    captured = capsys.readouterr()
    # Check if the output is correct
    assert captured.out == "Error: folder does not exist\n"

# Test when folder path is empty
def test_folder_correct_empty_path():    
    assert folder_correct("") == ("", False)
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
                       os.path.dirname(correct_file_yml)+"\\") == ("correct.yml", False)

# Test when file does not exists
def test_file_not_exists_yml(capsys, tmp_path):
    # Check if the output is correct
    assert file_exists(os.path.basename("not_correct.yml")[:-4],
                       str(tmp_path)+"\\") == (None, True)
    captured = capsys.readouterr()
    assert captured.out == "Error: file does not exist not_correct.yml(.yaml)\n"

# Define correct .yaml file fixture
@pytest.fixture
def correct_file_yaml(tmpdir):
    # Create a temporary .yaml file
    correct_file = tmpdir.join("correct.yaml")
    correct_file.write("")
    # Return the temporary .yaml file
    yield str(correct_file)

# Test when file exists
def test_file_exists_yaml(correct_file_yaml):
    # Check if the output is correct
    assert file_exists(os.path.basename(correct_file_yaml)[:-5],
                       os.path.dirname(correct_file_yaml)+"\\") == ("correct.yaml", False)

# Test when file does not exists
def test_file_not_exists_yaml(capsys, tmp_path):
    # Check if the output is correct
    assert file_exists(os.path.basename("not_correct.yaml")[:-5],
                       str(tmp_path)+"\\") == (None, True)
    captured = capsys.readouterr()
    assert captured.out == "Error: file does not exist not_correct.yml(.yaml)\n"
#endregion


#region List tasks tests
# Define correct tasks fixture
@pytest.fixture
def list_tasks_file(tmpdir):
    # Create a temporary tasks.yml file
    tasks_file = tmpdir.join("tasks.yml")
    # Fill the temporary tasks.yml file
    tasks_file.write(
        """
        tasks:
          - name: Task 1
          - name: Task 2
        """
    )
    # Return the temporary tasks.yml file
    yield str(tasks_file)

# Test when the file is correct
def test_list_tasks(capsys, list_tasks_file):
    # Call the function to list tasks
    list_entries("tasks", os.path.dirname(list_tasks_file)+"\\")

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
def test_list_tasks_empty(capsys, empty_tasks_file):
    # Call the function to list tasks
    list_entries("tasks", os.path.dirname(empty_tasks_file)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "There are no tasks\n"
#endregion


#region List build tests
# Define correct builds fixture
@pytest.fixture
def list_builds_file(tmpdir):
    # Create a temporary builds.yml file
    builds_file = tmpdir.join("builds.yml")
    # Fill a temporary builds.yml file
    builds_file.write(
        """
        builds:
          - name: Build 1
          - name: Build 2
        """
    )
    # Return a temporary builds.yml file
    yield str(builds_file)

# Test when the file is correct
def test_list_builds(capsys, list_builds_file):
    # Call the function to list builds
    list_entries("builds", os.path.dirname(list_builds_file)+"\\")

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


#region Get dependecies tests
# Define dependencies fixture
@pytest.fixture
def file_get_dependencies(tmpdir):
    # Create a temporary tasks.yml file
    tasks_file = tmpdir.join("tasks.yml")
    # Fill the temporary tasks.yml file
    tasks_file.write(
        """
        tasks:
          - name: Task 1
            dependencies: 
                - a
                - b
          - name: Task 2
            dependencies: []
        """
    )
    # Return the temporary tasks.yml file
    yield str(tasks_file)

# Test when the file is correct
def test_get_dependencies(file_get_dependencies):
    # Check if the output is correct
    assert get_dependencies(
            "Task 1",
            os.path.dirname(file_get_dependencies)+"\\") == "a, b, Task 1, "
    assert get_dependencies(
            "Task 2",
            os.path.dirname(file_get_dependencies)+"\\") == "Task 2, "
#endregion


#region Get tests
# Define get task fixture
@pytest.fixture
def correct_tasks_get(tmpdir):
    # Create a temporary tasks.yml file
    tasks_file = tmpdir.join("tasks.yml")
    # Fill the temporary tasks.yml file
    tasks_file.write(
        """
        tasks:
          - name: Task 1
            dependencies: 
                - a
                - b
          - name: Task 2
            dependencies: []
        """
    )
    # Return the temporary tasks.yml file
    yield str(tasks_file)

# Test when the file is correct
def test_get_task(capsys, correct_tasks_get):
    # Call the function to get a task
    get_entry("task", "Task 1", os.path.dirname(correct_tasks_get)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "Task info:\n- name: Task 1\n- dependencies: a, b, Task 1\n"

    # Call the function to get a task
    get_entry("task", "Task 2", os.path.dirname(correct_tasks_get)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "Task info:\n- name: Task 2\n- dependencies: Task 2\n"
    
    # Call the function to get a task
    get_entry("task", "Task 3", os.path.dirname(correct_tasks_get)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "Error: no such task\n"

# Define get build fixture
@pytest.fixture
def correct_build_get(tmpdir):
    # Create a temporary tasks.yml file
    tasks_file = tmpdir.join("tasks.yml")
    # Fill the temporary tasks.yml file
    tasks_file.write(
        """
        tasks:
          - name: Task 1
            dependencies: 
                - a
                - b
          - name: Task 2
            dependencies: []
        """
    )
    
    # Create a temporary builds.yml file
    builds_file = tmpdir.join("builds.yml")
    # Fill the temporary builds.yml file
    builds_file.write(
        """
        builds:
          - name: Build 1
            tasks: 
                - Task 1
                - Task 2
          - name: Build 2
            tasks:
                - Task 2
        """
    )
    # Return the temporary tasks.yml file
    yield str(builds_file)

# Test when the file is correct
def test_get_build(capsys, correct_build_get):
    # Call the function to get a bulid
    get_entry("build", "Build 1", os.path.dirname(correct_build_get)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "Build info:\n- name: Build 1\n- tasks: a, b, Task 1, Task 2\n"

    # Call the function to get a bulid
    get_entry("build", "Build 2", os.path.dirname(correct_build_get)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "Build info:\n- name: Build 2\n- tasks: Task 2\n"
    
    # Call the function to get a bulid
    get_entry("build", "Build 3", os.path.dirname(correct_build_get)+"\\")

    # Check if the output is correct
    captured = capsys.readouterr()
    assert captured.out == "Error: no such build\n"
#endregion
