#This script is used to measure the predicted structure with realstructure and statistical analysis of f1 score.
#Usage: python cal_f1_batch.py -dir1 <directory1> -dir2 <directory2> -p <picture>
import sys
import os
sys.path.append('/mnt/StorageNaN/learn_ai/xueyi/scripts')
import nass
from nass import Nass
import argparse
import matplotlib.pyplot as plt
import numpy as np

def find_matching_files(directory, exclude_suffix="_2.ct"):
    matched_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(exclude_suffix):
                continue
            matched_files[file] = os.path.join(root, file)
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
    # Perform special processing on the first folder and remove all files ending with _2.ct
    files1 = find_matching_files(folder1, "_2.ct")
    files2 = find_matching_files(folder2)

    f1_scores = []
    for filename1 in files1:
        # Get the first four characters of the file name
        prefix1 = filename1[:4]
        for filename2 in files2:
            prefix2 = filename2[:4]
            if prefix1 == prefix2:
                f1 = cal_f1(files1[filename1], files2[filename2])
                if f1 is not None:
                    f1_scores.append(f1)
                break

    if not f1_scores:
        print("No valid F1 scores found.")
        return

    # output the mean F1 score and the F1 scores
    mean_f1_score = np.mean(f1_scores)
    print(f"Mean F1 Score: {mean_f1_score}")
    print(f"{f1_scores}")
    # Draw the plots
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    boxprops = dict(color='blue', linewidth=2)
    whiskerprops = dict(color='black', linewidth=2)
    capprops = dict(color='black', linewidth=2)
    medianprops = dict(color='orange', linewidth=2)
    plt.boxplot(f1_scores, vert=True, patch_artist=True, 
                boxprops=boxprops, whiskerprops=whiskerprops, 
                capprops=capprops, medianprops=medianprops)
    plt.title('Boxplot of F1 Scores')
    plt.ylabel('F1 Score')
    plt.subplot(1, 2, 2)
    plt.violinplot(f1_scores, vert=True)
    plt.title('Violin Plot of F1 Scores')
    plt.ylabel('F1 Score')

    plt.tight_layout()
    plt.savefig(picture)
    plt.show()  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate F1 scores between matched files in two directories")
    parser.add_argument("-dir1", "--folder1", type=str, help="Path to the first directory")
    parser.add_argument("-dir2", "--folder2", type=str, help="Path to the second directory")
    parser.add_argument("-p", "--picture", type=str, help="Path to save the picture")
    args = parser.parse_args()

    if args.folder1 and args.folder2:
        main(args.folder1, args.folder2, args.picture)
        print(f"F1 scores calculated successfully and the picture is saved in {args.picture}")
    else:
        print("Please provide two directories")
        sys.exit(1)

