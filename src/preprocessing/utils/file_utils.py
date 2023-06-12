import os, shutil

def get_file_with_extension(path: str, extension: str) -> str:
    """
    Retrieves the first file in a directory that matches the specified extension.

    Parameters:
        path (str): The path to the directory where the files are located.
        extension (str): The desired file extension (e.g., '.txt', '.csv').

    Returns:
        str: The path of the first file found with the specified extension.

    Raises:
        FileNotFoundError: If the specified directory does not exist or is inaccessible.
        IndexError: If no file with the specified extension is found in the directory.

    Example:
        file_path = get_file_with_extension('/path/to/files', '.txt')
        print(file_path)
    """
    # Get the list of files in the specified directory
    files = os.listdir(path)

    # Filter the files based on the specified extension
    matching_files = [file for file in files if file.endswith(extension)]

    # Check if any matching files were found
    if len(matching_files) > 0:
        # Return the path of the first matching file
        return os.path.join(path, matching_files[0])
    else:
        print(path)
        # Raise an exception if no matching files were found
        raise IndexError("No file with the specified extension was found in the directory.")

def clean_dir(path: str):
    try:
        shutil.rmtree(path=path)
    except OSError:
        pass
    os.makedirs(path)