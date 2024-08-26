#This script is used to create .fa files based on rpc2.fa and other .fa files to create a new .fa file
#Usage: python rpc2_linkothers.py target.fa other1.fa other2.fa additional.fa output1.fa output2.fa

#定义已知的保护序列
prime_5 = 'GGCCGAAGGCCAA'
prime_3 = 'TCGATCCGGGAACCGGATCCATAACGGTCGAAGACCGTTAC'

import argparse
import os
import sys
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_fa_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        headers = [line.strip() for line in lines if line.startswith('>')]
        sequences = ''.join([line.strip() for line in lines if not line.startswith('>')])
        return headers, sequences
    except FileNotFoundError:
        logging.error(f"Error: File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        sys.exit(1)

def write_fa_file(file_path, headers, sequence):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            for header in headers:
                file.write(header + '\n')
            file.write(sequence + '\n')
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")
        sys.exit(1)

def replace_plus_signs(rpc2_sequence, seq1, seq2):
    parts = rpc2_sequence.split('+')
    if len(parts) != 3:
        raise ValueError("The rpc2.fa sequence should contain exactly two '+' signs.")
    
    seq1_first = parts[0] + seq1 + parts[1] + seq2 + parts[2]
    seq2_first = parts[0] + seq2 + parts[1] + seq1 + parts[2]
    return seq1_first, seq2_first

def split_sequence(sequence):
    mid_index = len(sequence) // 2
    if len(sequence) % 2 != 0:
        mid_index += 1
    return sequence[:mid_index], sequence[mid_index:]

def main(rpc2_file, other1_file, other2_file, additional_file, output1_file, output2_file):
    rpc2_headers, rpc2_sequence = read_fa_file(rpc2_file)
    _, other1_sequence = read_fa_file(other1_file)
    _, other2_sequence = read_fa_file(other2_file)
    _, additional_sequence = read_fa_file(additional_file)
    
    seq1_first, seq2_first = replace_plus_signs(rpc2_sequence, other1_sequence, other2_sequence)
    
    additional_seq_start, additional_seq_end = split_sequence(additional_sequence)
    
    seq1_first = prime_5 + additional_seq_start + seq1_first + additional_seq_end + prime_3
    seq2_first = prime_5 + additional_seq_start + seq2_first + additional_seq_end + prime_3
    
    write_fa_file(output1_file, rpc2_headers, seq1_first)
    write_fa_file(output2_file, rpc2_headers, seq2_first)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create .fa files based on rpc2.fa and other .fa files')
    parser.add_argument('-b','--rpc2_file', type=str, required=True, help='The rpc2.fa file')
    parser.add_argument('-i1','--other1_file', type=str, required=True, help='The first other .fa file')
    parser.add_argument('-i2','--other2_file', type=str, required=True, help='The second other .fa file')
    parser.add_argument('-i3','--additional_file', type=str, required=True, help='The additional .fa file')
    parser.add_argument('-o1','--output1_file', type=str, required=True, help='The first output .fa file')
    parser.add_argument('-o2','--output2_file', type=str, required=True, help='The second output .fa file')
    
    args = parser.parse_args()

    try:
        main(args.rpc2_file, args.other1_file, args.other2_file, args.additional_file, args.output1_file, args.output2_file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
