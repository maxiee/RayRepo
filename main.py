import argparse
import subprocess
import sys
import pathlib


def main():
    """
    Main function
    """
    # Call the function to create code path
    create_code_path()
    # Create a parser
    parser = argparse.ArgumentParser()
    # Subparser
    subparsers = parser.add_subparsers(dest="command")
    # Add an argument
    parser.add_argument("name", help="Name of the person")
    # Parse the argument
    args = parser.parse_args()
    # Print the name
    print(f"Hello, {args.name}")


def add_git_submodule(repo_url):
    """
    Add a git submodule
    """
    try:
        # Extract project name from URL
        project_name = repo_url.split("/")[-1].split(".")[0]
        # Clone submodule to projects directory
        subprocess.run(
            [
                "git",
                "submodule",
                "add",
                repo_url,
                str(
                    get_code_path()
                    / "projects"
                    / project_name
                ),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to add git submodule: {e}")
        sys.exit(1)


def get_code_path():
    """
    Code path in ~/Code/RaySystem
    """
    return pathlib.Path.home() / "Code" / "RaySystem"


def create_code_path():
    """
    Create code path if it doesn't exist
    """
    code_path = get_code_path()
    project_path = code_path / "projects"
    project_path.mkdir(parents=True, exist_ok=True)
