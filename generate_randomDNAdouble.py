#This script is used 

import os
import numpy as np
import argparse
#Usage: python generate_randomDNAdouble.py --num_seq <number of sequences> --seq_len <length of each sequence> --output_folder <output folder>
def complement(base):
    """Returns the complementary base of a given base."""
    base_complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return base_complement[base]

def generate_random_seq(num_seq, seq_len):
    """Generates a list of random DNA sequences of a specified number and length and adds complementary strands."""
    bases = ['A', 'T', 'C', 'G']
    seq_list = []
    for _ in range(num_seq):
        half_seq = ''.join(np.random.choice(bases, seq_len // 2))
        complement_seq = ''.join(complement(base) for base in half_seq[::-1])
        full_seq = half_seq + complement_seq
        seq_list.append(full_seq)
    return seq_list

def write_seq_to_fasta(seq_list, output_folder):
    """Write the sequence list to a FASTA format file in the specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, seq in enumerate(seq_list):
        file_path = os.path.join(output_folder, f'seq_{i}.fa')
        with open(file_path, 'w') as f:
            f.write(f'>seq_{i}\n{seq}\n')

def main():
    parser = argparse.ArgumentParser(description="Generate random DNA sequences and save as FASTA files.")
    parser.add_argument("-n", '--num_seq', type=int, default=100, help='The number of sequences to generate, default is 100.')
    parser.add_argument("-s", '--seq_len', type=int, default=100, help='The total length of each sequence, default is 100 (including the complementary strand).')
    parser.add_argument("-o", '--output_folder', type=str, default="inputfiles", help='the path of the output folder，default to inputfiles')
    args = parser.parse_args()
    
    seq_list = generate_random_seq(args.num_seq, args.seq_len)
    write_seq_to_fasta(seq_list, args.output_folder)
    print(f'Generated {args.num_seq} sequences with total length {args.seq_len} in {args.output_folder}')

if __name__ == '__main__':
    main()

