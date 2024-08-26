#This script is used 

import os
import numpy as np
import argparse

def complement(base):
    """返回给定碱基的互补碱基。"""
    base_complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return base_complement[base]

def generate_random_seq(num_seq, seq_len):
    """生成指定数量和长度的随机DNA序列列表，并添加互补链。"""
    bases = ['A', 'T', 'C', 'G']
    seq_list = []
    for _ in range(num_seq):
        half_seq = ''.join(np.random.choice(bases, seq_len // 2))
        complement_seq = ''.join(complement(base) for base in half_seq[::-1])
        full_seq = half_seq + complement_seq
        seq_list.append(full_seq)
    return seq_list

def write_seq_to_fasta(seq_list, output_folder):
    """将序列列表写入指定文件夹的FASTA格式文件中。"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, seq in enumerate(seq_list):
        file_path = os.path.join(output_folder, f'seq_{i}.fa')
        with open(file_path, 'w') as f:
            f.write(f'>seq_{i}\n{seq}\n')

def main():
    parser = argparse.ArgumentParser(description="生成随机DNA序列并保存为FASTA文件。")
    parser.add_argument("-n", '--num_seq', type=int, default=100, help='生成的序列数量，默认为100。')
    parser.add_argument("-s", '--seq_len', type=int, default=100, help='每个序列的总长度，默认为100（包括互补链）。')
    parser.add_argument("-o", '--output_folder', type=str, default="inputfiles", help='输出文件夹的路径，默认为inputfiles。')
    args = parser.parse_args()
    
    seq_list = generate_random_seq(args.num_seq, args.seq_len)
    write_seq_to_fasta(seq_list, args.output_folder)
    print(f'Generated {args.num_seq} sequences with total length {args.seq_len} in {args.output_folder}')

if __name__ == '__main__':
    main()

