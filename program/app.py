import typer
import yaml
import sys
from os.path import exists

# Create an instance of Typer class
app = typer.Typer()


def list_entries(type: str, path: str) -> None:
    """
    Lists all the tasks or builds from the corresponding .yml(.yaml) files.

    Args:
    - `type`: what to list (tasks or builds);
    - `path`: path to the folder where .yml(.yaml) files are present.
    """
    sys.stdout.write(f"List of available {type}:\n")
    
    # Open the file
    with open(path + f"{type}.yml") as f:
        data = yaml.safe_load(f)[type]
    
    # Print out all of the file's entries
    # By their names
    for entry in data:
        name = entry["name"]
        sys.stdout.write(f"- {name}\n")


def get_dependencies(name: str, path: str) -> str:
    """
    Returns a string of dependencies of a task

    Args:
    - `name`: name of a task;
    - `path`: path to the folder where tasks.yml(.yaml) file is present.
    """
    
    # Open the file
    with open(path+"tasks.yml") as f:
        tasks = yaml.safe_load(f)["tasks"]

    # Create an empty string
    tasks_str = ""

    # Iterate through all of the file's entries
    # By their names
    for task in tasks:
        task_name = task["name"]
        # If the passed name is in the file
        if task_name == name:
            # Get all of the task's dependencies
            dependencies = task["dependencies"]
            for d in dependencies:
                # Add them to the string
                tasks_str += f"{d}, "
            # And the task itself at the end
            tasks_str += f"{task_name}, "
        
    return tasks_str


def get_entry(type: str, name: str, path: str) -> None:
    """
    Prints out information about a build or a task

    Args:
    - `type`: what is being listed;
    - `name`: name of a task/build;
    - `path`: path to the folder where .yml(.yaml) files are present.
    """
    
    # Open the file
    with open(path+f"{type}s.yml") as f:
        data = yaml.safe_load(f)[f"{type}s"]

    # Iterate through all of the file's entries
    # By their names
    for entry in data:
        entry_name = entry["name"]
        # If the passed name is in the file
        if entry_name == name:
            # Print out the header and name of the entry
            sys.stdout.write("Task info:\n")
            sys.stdout.write(f"- name: {entry_name}\n")
            
            # If task type was specified
            if type == "task":
                # Print out its dependencies
                sys.stdout.write("- dependencies: ")
                sys.stdout.write(get_dependencies(name, path)[:-2]+"\n")
            else:
                # If build type was specified
                # Print out the build's tasks header
                sys.stdout.write("- tasks: ")

                # Get build's tasks
                build_tasks = entry["tasks"]

                # Print out build's tasks
                # And their dependencies
                # In order of dependencies > task
                tasks_str = ""
                for build_task in build_tasks:
                    tasks_str += get_dependencies(build_task, path)

                sys.stdout.write(tasks_str[:-2]+"\n")
            
            # Exit the method
            return
    
    # Print out the error if no entries were found
    # By the passed name
    sys.stdout.write(f"Error: no such {type}\n")


def folder_correct(path: str) -> bool:
    """
    Checks if the folder exists or not

    Args:
    - `path`: path to the folder where .yml(.yaml) files are present.
    """

    if len(path) > 0 and not exists(path):
        sys.stdout.write("Error: folder does not exists\n")
        return False
    return True


@app.command()
def list(type: str, path: str="") -> None:
    """
    Reads the CLI command `list` and prints out list of builds or tasks from the .yml file

    Args:
    - `type`: what is being listed;
    - `path`: path to the folder where .yml(.yaml) files are present.
    """

    # Check if the folder exists
    if not folder_correct(path): return
    # If it does - add the slash to the end of it
    # In order to be handled correctly
    else:
        path += "\\"

    # If argument builds was passed
    if type.lower() == "builds":
        # List all of the available builds
        list_entries(type, path)
    # If argument tasks was passed
    elif type.lower() == "tasks":
        # List all of the available tasks
        list_entries(type, path)
    # If there is a typo or a wrong argument
    else:
        # Print out the error
        sys.stdout.write(f"Error: unexpected argument, should be 'builds' or 'tasks'\n")
        

@app.command()
def get(type: str, name: str, path: str="") -> None:
    """
    Reads the CLI command `get` and prints information about a single build or a task from the .yml file

    Args:
    - `type`: what is being listed;
    - `name`: name of a task/build;
    - `path`: path to the folder where .yml(.yaml) files are present.
    """
    
    # Check if the folder exists
    if folder_correct(path): return
    # If it does - add the slash to the end of it
    # In order to be handled correctly
    else:
        path += "\\"
    
    # If argument builds was passed
    if type.lower() == "build":
        # Print out the information about the build
        get_entry(type, name, path)
    # If argument tasks was passed
    elif type.lowe() == "task":
        # Print out the information about the task
        get_entry(type, name, path)
    # If there is a typo or a wrong argument
    else:
        # Print out the error
        sys.stdout.write(f"Error: unexpected argument, should be 'build' or 'task'\n")

# Main entry point
if __name__ == "__main__":
    app()