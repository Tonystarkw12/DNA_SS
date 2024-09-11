#This script is used to compare between RNA or DNA secondary structures
# Add path (assuming you need to append it to sys.path for module resolution)
import sys
import os
sys.path.append('/mnt/StorageNaN/learn_ai/xueyi/scripts')
import nass
from nass import Nass
import argparse

def cal_f1(nass1, nass2):
    try:
        # Load the secondary structures
        rna1 = Nass(nass1)
        rna2 = Nass(nass2)
        # Calculate F1 score
        f1 = nass.calcF1(rna1, rna2)
        return f1
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate F1 score between two RNA or DNA secondary structures")
    parser.add_argument("-ss1", "--nass1", required=True, type=str, help="Path to the first file containing RNA or DNA secondary structure data")
    parser.add_argument("-ss2", "--nass2", required=True, type=str, help="Path to the second file containing RNA or DNA secondary structure data")
    args = parser.parse_args()

    f1 = cal_f1(args.nass1, args.nass2)
    if f1 is not None:
        print(f"F1 score: {f1}")
    else:
        sys.exit(1)


