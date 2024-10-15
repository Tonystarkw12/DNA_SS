#This is a main class contains all the functions that are used to process the fasta file
#The functions include:complement, transcribe, fasta_info, fastatostring, stringtofasta, stringtodbn, etc
#The main function is used to call the functions and process the fasta file
import sys
import os
import argparse
class fasta_process:
    def __init__(self):
        pass
    def complement(self,sequence):
        # Complementary base pairing rules
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        # Generate the complement sequence
        input_string = sequence.upper().strip().replace(" ", "")
        complement_sequence = "".join([complement[base] for base in input_string])
        reversed_complement_sequence = complement_sequence[::-1]
        return reversed_complement_sequence
    def split_fasta(self,fasta_file, output_dir):
        with open(fasta_file, 'r') as file:
            content = file.read().strip()
        sequences = content.split('>')[1:]  # Splitting at each new sequence
        for seq in sequences:
            lines = seq.split('\n')
            header = lines[0].strip()
            sequence_data = '\n'.join(lines[1:])
            output_file_path = os.path.join(output_dir, f"{header}.fasta")
            with open(output_file_path, 'w') as out_file:
                out_file.write(f'>{header}\n{sequence_data}')
        print(f"Split done! {len(sequences)} sequences saved in {output_dir}")
    def 
   