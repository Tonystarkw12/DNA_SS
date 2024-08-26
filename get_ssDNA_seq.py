import pandas as pd
import subprocess
import os
import argparse

def download_fasta(pdb_id, download_dir):
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
    output_file = os.path.join(download_dir, f"{pdb_id}.fasta")
    try:
        subprocess.run(["wget", "-O", output_file, url], check=True)
        if not os.path.exists(output_file):
            print(f"Error: File {output_file} does not exist after download attempt.")
            return None
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to download fasta file for PDB ID {pdb_id}. {e}")
        return None

def extract_dna_sequence(fasta_file):
    sequence = ""
    try:
        with open(fasta_file, "r") as file:
            for line in file.readlines():
                clean_line = line.strip()
                if all(c in 'ATGC' for c in clean_line) :
                    sequence = clean_line
                    print(f"Extracted DNA sequence: {clean_line}")
        return sequence
    except Exception as e:
        print(f"Error processing file {fasta_file}: {e}")
        return ""

def main(excel_file_path, download_dir):
    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        print(f"Error: Failed to read Excel file. {e}")
        return
    
    if 'PDB' not in df.columns or 'Size (nt)' not in df.columns:
        print("Error: 'PDB' or 'Size (nt)' column not found in the Excel file.")
        return

    df['Sequence'] = ""
    pdb_list = df['PDB'].tolist()

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for pdb_id in pdb_list:
        print(f"Processing PDB ID: {pdb_id}")
        fasta_file = download_fasta(pdb_id, download_dir)
        if fasta_file:
            sequence = extract_dna_sequence(fasta_file)
            expected_size = df.loc[df['PDB'] == pdb_id, 'Size (nt)'].values[0]
            if len(sequence) == expected_size:
                df.loc[df['PDB'] == pdb_id, 'Sequence'] = sequence
            else:
                print(f"Warning: Extracted sequence length for PDB ID {pdb_id} does not match expected size. Skipping.")
    
    output_file_path = f"updated_{os.path.basename(excel_file_path)}"
    try:
        df.to_excel(output_file_path, index=False)
        print(f"Updated Excel file saved as {output_file_path}")
    except Exception as e:
        print(f"Error: Failed to save updated Excel file. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download and process PDB fasta sequences.')
    parser.add_argument('excel_file_path', type=str, help='Path to the Excel file containing PDB IDs.')
    parser.add_argument('download_dir', type=str, help='Directory to download fasta files.')

    args = parser.parse_args()

    main(args.excel_file_path, args.download_dir)
