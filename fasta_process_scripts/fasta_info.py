#This script is used for getting the information of fasta file
#Usage: python fasta_info.py -f fasta_file
import sys
import os
import argparse
from sys import exit
import dna2rna
def parse_fasta(filename):
    count =0 #代表fasta文件中序列的个数
    #对fasta文件进行分类，总共三种，DNA,RNA and protein
    with open(filename, 'rt') as file:
        fasta_content = file.readlines()
    for line in fasta_content:
        if line.startswith('>'):
            count += 1

    if count > 1:
        #print("This is a multi-fasta file")
        sequences = dna2rna.parse_fasta(fasta_content)
        for seq in sequences:
            discription = seq[0].strip()
            fasta_type = classify_fasta(seq[1])
            name = discription.split()[1]
            length = 0
            for line in seq[1]:
                length += len(line.strip())
            print(f"{discription}\nThe name of {fasta_type} file is {name},the length is {length}\n")
    else:
        discription = fasta_content[0].strip()
        fasta_type = classify_fasta(fasta_content)
        name = discription.split()[1]
        length = 0
        for line in fasta_content:
            length += len(line.strip())
        print(f"{discription}\nThe name of {fasta_type} file is {name},the length is {length}")
def classify_fasta(fasta_content):
    # Define the unique characters for each type
    dna_chars = set("ATGC")
    rna_chars = set("AUGC")

    # Remove line breaks and other non-sequence characters
    fasta_content = ''.join(fasta_content)
    sequence = ''.join(filter(str.isalpha, fasta_content.upper()))

    # Check if the sequence is DNA: Only A, T, G, C
    if set(sequence) <= dna_chars:
        return "DNA"
    # Check if the sequence is RNA: Only A, U, G, C
    elif set(sequence) <= rna_chars:
        return "RNA"
    # Otherwise, classify as Protein
    else:
        return "Protein"
def main():
    try:
        parser = argparse.ArgumentParser(description="This script is used for getting the information of fasta file")
        parser.add_argument('-f', '--filename', type=str, metavar='', required=True, help='The fasta file')
        args = parser.parse_args()
        filename = args.filename
        parse_fasta(filename)
    except Exception as e:
        print(e)
        exit(1)
    except FileNotFoundError as e:
        print(e)
        exit(1)
    
if __name__ == '__main__':
    main()
    