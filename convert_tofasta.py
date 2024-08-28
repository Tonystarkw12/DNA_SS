import pandas as pd
import os
import sys
#Usage: python convert_tofasta.py <input_file> <output_folder>
def create_fasta_files(input_file, output_folder):
    # Read an excel file
    df = pd.read_excel(input_file)
    
    # make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # iterate over each row and generate the corresponding .fa file
    for index, row in df.iterrows():
        pdb = row['PDB']
        sequence = row['Sequence']
        
        
        fasta_content = f">{pdb}\n{sequence}"
        
        # write to file
        file_path = os.path.join(output_folder, f"{pdb}.fa")
        with open(file_path, 'w') as file:
            file.write(fasta_content)
    
    print("All fa files have been saved to ", output_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_folder>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    
    create_fasta_files(input_file, output_folder)
