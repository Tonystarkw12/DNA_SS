#This script is for processing DNA secondary structures predictions on a batch profile
#Usage: bash generate_randomDNA.py --num_seq <number of sequences> --seq_len <length of each sequence> --output_folder <output folder>
#Example: bash generate_randomDNA.py --num_seq 100 --seq_len 100 --output_folder inputfiles
#首先生成100个长度为100的随机DNA序列
import os
import numpy as np
import argparse

def generate_random_seq(num_seq, seq_len):
    """生成指定数量和长度的随机DNA序列列表。"""
    bases = ['A', 'T', 'C', 'G']
    seq_list = [''.join(np.random.choice(bases, seq_len)) for _ in range(num_seq)]
    return seq_list

def write_seq_to_fasta(seq_list, output_folder):
    """将序列列表写入指定文件夹的FASTA格式文件中。"""
    # 确保输出文件夹存在，如果不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 为每个序列创建一个FASTA文件
    for i, seq in enumerate(seq_list):
        file_path = os.path.join(output_folder, f'seq_{i}.fa')
        with open(file_path, 'w') as f:
            f.write(f'>seq_{i}\n{seq}\n')

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="生成随机DNA序列并保存为FASTA文件。")
    parser.add_argument('--num_seq', type=int, default=100, help='生成的序列数量，默认为100。')
    parser.add_argument('--seq_len', type=int, default=100, help='每个序列的长度，默认为100。')
    parser.add_argument('--output_folder', type=str, default="inputfiles", help='输出文件夹的路径，默认为inputfiles。')
    args = parser.parse_args()
    
    # 生成随机序列
    seq_list = generate_random_seq(args.num_seq, args.seq_len)
    
    # 写入文件
    write_seq_to_fasta(seq_list, args.output_folder)
    print(f'Generated {args.num_seq} sequences with length {args.seq_len} in {args.output_folder}')

if __name__ == '__main__':
    main()

    