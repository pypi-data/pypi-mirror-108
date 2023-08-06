import glob
import subprocess
import tempfile
from pathlib import Path


def format_note(note):
    return f"\n{note}"  # todo


def read_note_in_vim():
    with tempfile.NamedTemporaryFile(suffix='task') as temp:
        subprocess.call(['vim', temp.name])
        return open(temp.name, 'r').read()


def save_note(note, scope, name, work_path):
    parent_path = f"{work_path}/{scope}"
    Path(parent_path).mkdir( parent_path=True, exist_ok=True)

    filepath = f"{parent_path}/{name}.md"
    note_file = open(filepath, "a+")

    note_file.writelines(format_note(note))

    print(f"note saved to {filepath}")


def read_note(work_path):
    # print(f"read path: {work_path} : {path.isfile(work_path)}")
    files = glob.glob(work_path)
    if len(files) < 1:
        print("nothing here...")
        print("you can append note to default scope and name via command;")
        print("$ python3 snos -ac \"test\" # or,")
        print("$ python3 snos -av # via vim")
    for file in files:
        print(open(file).read())


def print_note(scope, name, work_path):
    note = open(f"{work_path}/{scope}/{name}", "r+")
    print(note.read())


def list_note_names(home_path, work_path):
    for file in glob.glob(work_path):
        print(file.replace(home_path, ""))
