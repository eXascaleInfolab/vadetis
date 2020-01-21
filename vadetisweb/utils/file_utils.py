import tempfile, os, errno


def write_to_tempfile(raw_file, delete=False):
    """
    Write byte contents to a temporary file (it is saved in temp folder)
    :return: a copy of the raw file as a temporary file
    """

    random_file = tempfile.NamedTemporaryFile(delete=delete)

    with open(random_file.name, 'wb+') as temp_file:
        for chunk in raw_file.chunks():
            temp_file.write(chunk)

    return random_file


def silent_remove(filename):
    """
    Silently removes a file from the file system
    :param filename: the filename to remove
    """
    try:
        os.remove(filename)
        print("File removed: ", filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
        else:
            pass  # no such file or directory so pass
