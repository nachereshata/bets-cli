from functools import partial
from multiprocessing import Process
from subprocess import call


def open_file(file_path: str):
    """Makes the system open a file with the default handler for the file type"""

    Process(target=partial(call, ["cmd", "/c", file_path]), daemon=True).start()
