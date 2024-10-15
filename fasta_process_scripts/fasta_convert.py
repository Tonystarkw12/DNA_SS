#!/home/tony/anaconda3/bin/python
#This script is used to get the lowerstem sequence of the fasta file
#Usage: python fasta_convert.py <input_folder> <output_folder>
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import os
import sys
def process_fasta_files(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            file_path = os.path.join(input_dir, filename)
            # Add 'lowerstem' suffix to the file name
            base, ext = os.path.splitext(filename)
            output_filename = f"{base}_lowerstem{ext}"
            output_file_path = os.path.join(output_dir, output_filename)

            # Read and process the fasta file
            with open(file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                for record in SeqIO.parse(input_file, "fasta"):
                    # Extract the first 19 and last 19 bases, and join them with "CUUCGG"
                    new_sequence_str = str(record.seq[:19]) + "CUUCGG" + str(record.seq[-19:])
                    new_sequence = Seq(new_sequence_str)
                    new_record = SeqRecord(new_sequence, id=record.id, description=record.description)
                    # Write the new sequence record to the output file
                    SeqIO.write([new_record], output_file, "fasta-2line")

# Example usage
# process_fasta_files("path/to/input_dir", "path/to/output_dir")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fasta_convert.py <input_folder> <output_folder>")
        sys.exit(1)
    process_fasta_files(sys.argv[1], sys.argv[2])
