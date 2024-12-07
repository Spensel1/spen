import os


def get_file_full_path(file_relative_path):
    return f"{os.path.join(os.path.dirname(__file__), file_relative_path)}"
