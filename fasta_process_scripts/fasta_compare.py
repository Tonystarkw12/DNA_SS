#This script is for comparing different fasta files
#This script accepts two kinds of parameters, pure string and fasta file
#总共存在几种情况，互补，相同
#1.两个参数都是纯字符串，比较两个字符串是否相同或者互补
#2.两个参数都是fasta文件，比较两个fasta文件是否相同或者互补
#3.一个参数是纯字符串，一个参数是fasta文件，比较两者是否相同或者互补
#用法：python fasta_compare.py -s1 <filename1> -s2 <filename2>
import argparse
import os
from sys import exit
def read_fasta(file_path):
    """Reads a FASTA file and returns the sequence."""
    with open(file_path, 'rt') as file:
        # Skip the header line
        sequences = file.readlines()[1:]
    return sequences

def is_complementary(seq1, seq2):
    """Checks if two sequences are complementary."""
    complementary = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'U': 'A','A': 'U'}
    return all(complementary[base1] == base2 for base1, base2 in zip(seq1, seq2))

def is_part(seq1, seq2):
    """Checks if one sequence is part of the other."""
    return seq1 in seq2 or seq2 in seq1

def compare_sequences(seq1, seq2):
    """Compares two sequences to check if they are identical or complementary."""
    if seq1 == seq2:
        return "Identical"
    elif is_complementary(seq1, seq2):
        return "Complementary"
    elif is_part(seq1, seq2):
        return "They are part of each other"
    else:
        return "Neither"

# Example usage
# For demonstration, let's assume seq1 and seq2 are strings or file paths
def main():
    parser = argparse.ArgumentParser(description="Compare two sequences")
    parser.add_argument("-s1", "--filename1", help="First sequence")
    parser.add_argument("-s2", "--filename2", help="Second sequence")
    args = parser.parse_args()
    seq1 = args.filename1
    seq2 = args.filename2
    if isinstance(seq1, str):
        if isinstance(seq2, str):
            result = compare_sequences(seq1, seq2)
            print(result)
        else:
            seq2 = read_fasta(seq2)
            result = compare_sequences(seq1, seq2)
            print(result)
    else:
        seq1 = read_fasta(seq1)
        if isinstance(seq2, str):
            result = compare_sequences(seq1, seq2)
            print(result)
        else:
            seq2 = read_fasta(seq2)
            result = compare_sequences(seq1, seq2)
            print(result)

if __name__ == '__main__':
    main()
    