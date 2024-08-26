import os
import shutil

def compare_and_retain_common_files(folder1, folder2):
    # 获取两个文件夹中的文件名列表
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)

    # 创建集合存储前四个字母相同的文件名
    common_files1 = set()
    common_files2 = set()

    for file1 in files1:
        for file2 in files2:
            if file1[:4] == file2[:4]:
                common_files1.add(file1)
                common_files2.add(file2)

    # 删除不在common_files1中的文件
    for file1 in files1:
        if file1 not in common_files1:
            os.remove(os.path.join(folder1, file1))

    # 删除不在common_files2中的文件
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
