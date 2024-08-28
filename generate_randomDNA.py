#This script is for processing DNA secondary structures predictions on a batch profile
#Usage: bash generate_randomDNA.py --num_seq <number of sequences> --seq_len <length of each sequence> --output_folder <output folder>
#Example: bash generate_randomDNA.py --num_seq 100 --seq_len 100 --output_folder inputfiles
#First, generate 100 random DNA sequences of length 100
import os
import numpy as np
import argparse

def generate_random_seq(num_seq, seq_len):
    """Generates a list of random DNA sequences of a specified number and length."""
    bases = ['A', 'T', 'C', 'G']
    seq_list = [''.join(np.random.choice(bases, seq_len)) for _ in range(num_seq)]
    return seq_list

def write_seq_to_fasta(seq_list, output_folder):
    """Write the sequence list to a FASTA format file in the specified folder."""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # iterate over each sequence and write to a separate file
    for i, seq in enumerate(seq_list):
        file_path = os.path.join(output_folder, f'seq_{i}.fa')
        with open(file_path, 'w') as f:
            f.write(f'>seq_{i}\n{seq}\n')

def main():
    parser = argparse.ArgumentParser(description="Generate random DNA sequences and save as FASTA files.")
    parser.add_argument('--num_seq', type=int, default=100, help='The number of sequences to generate, default is 100.')
    parser.add_argument('--seq_len', type=int, default=100, help='The length of each sequence, default is 100.')
    parser.add_argument('--output_folder', type=str, default="inputfiles", help='the path of outputfolder，default to inputfiles。')
    args = parser.parse_args()
    
    # 生成随机序列
    seq_list = generate_random_seq(args.num_seq, args.seq_len)
    
    # 写入文件
    write_seq_to_fasta(seq_list, args.output_folder)
    print(f'Generated {args.num_seq} sequences with length {args.seq_len} in {args.output_folder}')

if __name__ == '__main__':
    main()

    