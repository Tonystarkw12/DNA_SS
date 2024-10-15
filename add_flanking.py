
# This script is used to add flanking sequences to a given sequence
# Usage: python add_flanking.py -i <input file> -o <output file> 
import os
import sys
import argparse

# Flanking sequences
das_sequence_5prime = "GGAAAGGAAAGGGAAAGAAA"
das_sequence_3prime = "AAAACAAAACAAAGAAACAACAACAACAAC"

weeks_sequence_5prime = "GGGCCGAAGGCCAA"
weeks_sequence_3prime = "TCGATCCGGGAACCGGATCCATAACGGTCGAAGACCGTTAC"

def add_flanking(input_file, output_file_name):
    # Input a .fa file and output two .fa files with flanking sequences
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
        headers = [line.strip() for line in lines if line.startswith('>')]
        sequences = ''.join([line.strip() for line in lines if not line.startswith('>')])
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        sys.exit(1)

    # Add flanking sequences
    das_sequence = das_sequence_5prime + sequences + das_sequence_3prime
    weeks_sequence = weeks_sequence_5prime + sequences + weeks_sequence_3prime

    # Output file paths
    das_output_file = f"{output_file_name}_das.fa"
    weeks_output_file = f"{output_file_name}_weeks.fa"

    try:
        # Write DAS sequence to file
        with open(das_output_file, 'w') as file:
            for header in headers:
                file.write(header + '\n')
            file.write(das_sequence + '\n')

        # Write WEEKS sequence to file
        with open(weeks_output_file, 'w') as file:
            for header in headers:
                file.write(header + '\n')
            file.write(weeks_sequence + '\n')

        print(f"Output files created: {das_output_file} and {weeks_output_file}")

    except Exception as e:
        print(f"Error writing to output files: {e}")
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add flanking sequences to a given sequence')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file base name (without extension)')
    args = parser.parse_args()
    add_flanking(args.input, args.output)

