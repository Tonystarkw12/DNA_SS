import argparse
import os
#usage = "python split_fasta.py -dtr <filename> -o <out_put_dir>"


def split_fasta(fasta_file, output_dir):
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

# 使用示例
# split_fasta('path/to/your/fasta_file.fasta', 'path/to/output/directory')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Fasta Script")
    parser.add_argument('-dtr',"--filename", help="Path to the FASTA file containing DNA sequences")
    parser.add_argument('-o', "--output_dir", help="Path to the output directory")
    args = parser.parse_args()
    try:
        if not os.path.exists(args.filename):
            print(f"Error: File {args.filename} does not exist.")
        output_dir = args.output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        split_fasta(args.filename, output_dir)
    except Exception as e:
        print(f"Error: {e}")

