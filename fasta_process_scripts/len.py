# This script is used to get the length of a sequence
# Usage: python len.py .fa / string
import sys
import os

# Check if the input is a file
if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1], 'r') as f:
        # Skip the first line (usually the header in FASTA files) and join the rest as a sequence
        sequence = ''.join(line.strip() for line in f.readlines()[1:])
else:
    sequence = sys.argv[1]

# Remove any spaces in the sequence
sequence = sequence.replace(" ", "")
print(f"The length of the sequence is {len(sequence)}")
