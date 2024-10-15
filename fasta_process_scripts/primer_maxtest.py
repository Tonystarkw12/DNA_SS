# This script is used to test two primer sequences and return the maximum number of matches between them
# Usage: python primer_maxtest.py <primer1> <primer2>
# Example: python primer_maxtest.py ATCGATCG ATCGATCG
import os
import sys
import argparse
complementary_bases = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
}

def find_longest_complementary_segment(seq1, seq2):
    
    seq2 = seq2[::-1]
    
    max_len = 0
    max_start_idx = -1
    current_len = 0
    current_start_idx = 0
    
    for i in range(min(len(seq1), len(seq2))):
        if complementary_bases.get(seq1[i]) == seq2[i]:
            # if the bases are complementary, increase the current length
            if current_len == 0:
                current_start_idx = i
            current_len += 1
            if current_len > max_len:
                max_len = current_len
                max_start_idx = current_start_idx
        else:
            # if the bases are not complementary, reset the current length
            current_len = 0
    
    # 输出结果
    if max_len > 0:
        print(f"The max of complementary bases are {max_len} at position {max_start_idx}")
    else:
        print("two sequences have no complementary segment")

# 输入两条DNA序列
def main():
    seq1 = sys.argv[1]
    seq2 = sys.argv[2]
    find_longest_complementary_segment(seq1, seq2)
    find_longest_complementary_segment(seq1,seq1)
    find_longest_complementary_segment(seq2,seq2)
    
if __name__ == "__main__":
    main()

