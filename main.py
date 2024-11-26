import argparse
import os
import subprocess
import sys
import pathlib


def main():
    """
    Main function
    """
    # Call the function to create code path
    initialize_code_path()
    # Create a parser
    parser = argparse.ArgumentParser()
    # Subparser
    subparsers = parser.add_subparsers(dest="command")

    parser_add_submodule = subparsers.add_parser("add_submodule")
    parser_add_submodule.add_argument("repo_url", help="Repository URL")

    parser_update_submodules = subparsers.add_parser("update_submodules")

    args = parser.parse_args()
    if args.command == "add_submodule":
        add_git_submodule(args.repo_url)
    elif args.command == "update_submodules":
        update_git_submodules()
    else:
        parser.print_help()
        sys.exit(1)


def update_git_submodules():
    """
    Update git submodules
    """
    try:
        change_cwd_to_code_path()
        # 首先拉取主仓库最新代码
        print("Pulling main code")
        subprocess.run(["git", "pull"], check=True)
        print("Pulling submodules")
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "submodule",
                "foreach",
                "git",
                "pull",
            ],
            check=True,
        )
        print("Updated git submodules")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update git submodules: {e}")
        sys.exit(1)


def add_git_submodule(repo_url):
    """
    Add a git submodule
    """
    try:
        change_cwd_to_code_path()
        # Extract project name from URL
        project_name = repo_url.split("/")[-1].split(".")[0]
        # Clone submodule to projects directory
        subprocess.run(
            [
                "git",
                "submodule",
                "add",
                repo_url,
                f"projects/{project_name}",
            ],
            check=True,
        )
        print(f"Added git submodule: {project_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add git submodule: {e}")
        sys.exit(1)


def git_clone(repo_url, local_path):
    """
    Clone a git repository
    """
    try:
        subprocess.run(["git", "clone", repo_url, local_path], check=True)
        print(f"Cloned git repository: {repo_url}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone git repository: {e}")
        sys.exit(1)


def get_code_path():
    """
    Code path in ~/Code/RaySystem
    """
    return pathlib.Path.home() / "Code" / "RaySystem"


def change_cwd_to_code_path():
    """
    Change current working directory to code path
    """
    code_path = get_code_path()
    if not code_path.exists():
        print(f"Code path doesn't exist: {code_path}")
        sys.exit(1)
    os.chdir(code_path)


def initialize_code_path():
    """
    Create code path if it doesn't exist
    """
    code_path = get_code_path()
    if not code_path.exists():
        git_clone("git@github.com:maxiee/RaySystem.git", code_path)
    project_path = code_path / "projects"
    project_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
