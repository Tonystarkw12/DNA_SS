import sys
import os
sys.path.append('/mnt/StorageNaN/learn_ai/xueyi/scripts')
import nass
from nass import Nass
import argparse
import matplotlib.pyplot as plt
from collections import defaultdict

def find_matching_files(directory):
    matched_files = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ct"):
                prefix = '_'.join(file.split('_')[:2])  # 获取前两个部分作为前缀
                matched_files[prefix].append(os.path.join(root, file))
    return matched_files

def cal_f1(nass1, nass2):
    try:
        rna1 = Nass(nass1)
        rna2 = Nass(nass2)
        f1 = nass.calcF1(rna1, rna2)
        return f1
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main(folder1, folder2, picture):
    files1 = find_matching_files(folder1)
    files2 = find_matching_files(folder2)

    f1_scores = []
    for prefix in files1:
        if prefix in files2:
            max_f1 = -1
            for file1 in files1[prefix]:
                for file2 in files2[prefix]:
                    f1 = cal_f1(file1, file2)
                    if f1 is not None and f1 > max_f1:
                        max_f1 = f1
            if max_f1 != -1:
                f1_scores.append(max_f1)

    if not f1_scores:
        print("No valid F1 scores found.")
        return

    # 准备绘图
    plt.figure(figsize=(12, 6))
    # 创建一个绘图区域，并设置1行2列布局
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)

    # 在第一个绘图区域绘制箱线图
    ax1.boxplot(f1_scores, vert=True, patch_artist=True)
    ax1.set_title('Boxplot of F1 Scores')
    ax1.set_ylabel('F1 Score')

    # 在第二个绘图区域绘制小提琴图
    ax2.violinplot(f1_scores, vert=True)
    ax2.set_title('Violin Plot of F1 Scores')
    ax2.set_ylabel('F1 Score')

    # 显示图表
    plt.tight_layout()
    plt.savefig(picture)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate F1 scores between matched files in two directories")
    parser.add_argument("-dir1", "--folder1", type=str, help="Path to the first directory")
    parser.add_argument("-dir2", "--folder2", type=str, help="Path to the second directory")
    parser.add_argument("-p", "--picture", type=str, help="Path to save the picture")
    args = parser.parse_args()

    if args.folder1 and args.folder2:
        main(args.folder1, args.folder2, args.picture)
    else:
        print("Please provide two directories")
        sys.exit(1)
