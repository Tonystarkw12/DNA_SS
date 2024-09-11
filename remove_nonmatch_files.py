import os
import shutil

def compare_and_retain_common_files(folder1, folder2):
    # Get a list of file names in two folders
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)

    # Create a collection to store file names with the same first four letters
    common_files1 = set()
    common_files2 = set()

    for file1 in files1:
        for file2 in files2:
            if file1[:4] == file2[:4]:
                common_files1.add(file1)
                common_files2.add(file2)

    # Delete files that are not in common_files1
    for file1 in files1:
        if file1 not in common_files1:
            os.remove(os.path.join(folder1, file1))

    # Delete files that are not in common_files2
    for file2 in files2:
        if file2 not in common_files2:
            os.remove(os.path.join(folder2, file2))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Compare two folders and retain only common files based on the first four characters of the filenames.')
    parser.add_argument('folder1', type=str, help='Path to the first folder')
    parser.add_argument('folder2', type=str, help='Path to the second folder')

    args = parser.parse_args()

    compare_and_retain_common_files(args.folder1, args.folder2)
