import os


# this function returns the absolute path of the
# file specified with filename. it searches for
# the file recursively and returns all possible
# answers.
# root_dir is the top directory of our search
def get_absolute_path(root_dir, filename):
    result = []
    contents = os.listdir(root_dir)
    for content in contents:
        # determining contents absolute path
        content = os.path.join(root_dir, content)

        if os.path.isdir(content):
            res = get_absolute_path(content, filename)
            if res:
                # this for loop is needed for avoiding nested python lists.
                for item in res:
                    result.append(item)

        # if the file path ends with our desired filename, then it is our case!
        elif content.endswith(filename):
            result.append(content)

    return result


# this module will join txt files together.
# file1 and file2 are abs path for two files.
# it adds file2 to the end of file1 in a new file.
def join_files(file1, file2, newfile_path):
    with open(newfile_path, 'w') as out_file:
        for file in (file1, file2):
            with open(file) as in_file:
                out_file.write(in_file.read())
    return newfile_path


# this will add a txt to a text file(abs path required).
# add_to_top is True is adds it to the top of the text file.
def add_to_file(text, file, add_to_top=False):
    with open(file) as file:
        file_contents = file.read()
    print(file_contents)


add_to_file("helllo", '/home/amir/Desktop/sezar.py')

