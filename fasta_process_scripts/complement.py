# This script is used to generate the complement of a given sequence
# Usage: python complement.py <input_file>
# The input can either be a fasta file or a string of sequence

import sys

def complement(sequence):
    # Complementary base pairing rules
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    # Generate the complement sequence
    return "".join([complement[base] for base in sequence])

def main():
    if len(sys.argv) < 2:
        print("Usage: python complement.py <input_sequence>")
        sys.exit(1)
    
    input_string = sys.argv[1]
    # Convert the input string to upper case and remove any white spaces
    input_string = input_string.upper().strip().replace(" ", "")
    
    # Get the complement sequence
    complement_sequence = complement(input_string)
    
    # Reverse the complement sequence to maintain the 5' to 3' orientation
    reversed_complement_sequence = complement_sequence[::-1]
    
    print("The complement (5' to 3') of the given sequence is:", reversed_complement_sequence)

if __name__ == "__main__":
    main()
