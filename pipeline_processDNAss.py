#This script is used for processing DNA secondary structures predictions on a batch profile
#Usage: bash pipeline_processDNAss.sh <input directory>
import os
import subprocess
import glob
import filecmp
import argparse
import hashlib

def cleanup_nonct_files(output_folder):
    all_files = os.listdir(output_folder)
    for file in all_files:
        file_path = os.path.join(output_folder, file)
        if os.path.isfile(file_path) and not file.endswith('.ct'):
            os.remove(file_path)

def run_mfold(input_file, output_folder, type='DNA'):
    input_path = os.path.abspath(input_file)
    if type == 'DNA':
        cmd = f'mfold SEQ={input_path} NA=DNA'
    else:
        cmd = f'mfold SEQ={input_path}'
    subprocess.run(cmd, shell=True, cwd=output_folder)
    cleanup_nonct_files(output_folder)

def rename_files(folder):
    files = glob.glob(os.path.join(folder, '*.ct'))
    for file in files:
        new_name = file.replace('.fa', '')
        os.rename(file, new_name)
        print(f"Renamed {file} to {new_name}")


#Run RNAstructure
def run_RNAstructure(input_file, output_folder,type='DNA'):
    input_path = os.path.abspath(input_file)
    output_file = os.path.join(output_folder, os.path.basename(input_file).replace('.fa', '.ct'))
    if type == 'DNA':
        cmd = f'Fold -d "{input_path}" "{output_file}"'
    else:
        cmd = f'Fold "{input_path}" "{output_file}"'
    subprocess.run(cmd, shell=True)



def process_RNAss_output(rnastructure_folder):
    ct_files = glob.glob(os.path.join(rnastructure_folder, '*.ct'))
    for file in ct_files:
        cmd = f'python split_dnass.py -ss "{file}"'
        subprocess.run(cmd, shell=True)


#Draw the plots
def plot(mfold_folder, rnastructure_folder, mfold_plot_folder, rnastructure_plot_folder):
    os.makedirs(mfold_plot_folder, exist_ok=True)
    os.makedirs(rnastructure_plot_folder, exist_ok=True)
    cmd_mfold = f'bash visualization_RNAss.bash {mfold_folder} {mfold_plot_folder}'
    cmd_rnastructure = f'bash visualization_RNAss.bash {rnastructure_folder} {rnastructure_plot_folder}'
    subprocess.run(cmd_mfold, shell=True)
    subprocess.run(cmd_rnastructure, shell=True)
    
    
#Remove the original ct files
def clean_originalct(directory):
    try:
        for filename in os.listdir(directory):
            if "_" not in filename:
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
#Remove duplicates
def hash_file(file_path):
    """Generate a SHA-256 hash of the file"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def removeduplicates(directory):
    """Delete duplicate files in the specified directory and its subdirectories"""
    hashes = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = hash_file(file_path)

            if file_hash in hashes:
                duplicates.append(file_path)
            else:
                hashes[file_hash] = file_path

def main():
    parser = argparse.ArgumentParser(description="Processing DNA secondary structure prediction files.")
    parser.add_argument('-i', '--input_folder', type=str, required=True, help='The path of the input folder')
    parser.add_argument('-o', '--output_folder', type=str, required=True, help='THe path of the output folder')
    parser.add_argument('-t','--type', type=str, default='DNA', help='Specifies whether to process DNA or RNA. The default is DNA.')
    args = parser.parse_args()
    
    results_folder = os.path.join(args.output_folder, 'results')
    mfold_folder = os.path.join(results_folder, 'mfold')
    rnastructure_folder = os.path.join(results_folder, 'RNAstructure')
    plot_folder = os.path.join(args.output_folder, 'plots')
    mfold_plot_folder = os.path.join(plot_folder, 'mfold_plots')
    rnastructure_plot_folder = os.path.join(plot_folder, 'RNAstructure_plots')

    os.makedirs(mfold_folder, exist_ok=True)
    os.makedirs(rnastructure_folder, exist_ok=True)
    os.makedirs(mfold_plot_folder, exist_ok=True)
    os.makedirs(rnastructure_plot_folder, exist_ok=True)
    
    input_files = glob.glob(os.path.join(args.input_folder, '*.fa'))
    
    for input_file in input_files:
        #Run mfold and RNAstructure
        run_mfold(input_file, mfold_folder, args.type)
        run_RNAstructure(input_file, rnastructure_folder, args.type)
    #Process RNAstructure output
    process_RNAss_output(rnastructure_folder)
    #process_RNAss_output(mfold_folder) (It seems that mfold will automatically split itself and does not need to be split again)
    clean_originalct(rnastructure_folder)
    removeduplicates(rnastructure_folder)
    
    #Process mfold output
    cleanup_nonct_files(mfold_folder)
    clean_originalct(mfold_folder)
    rename_files(mfold_folder)
    removeduplicates(mfold_folder)
    
    #Draw the plots
    plot(mfold_folder, rnastructure_folder, mfold_plot_folder, rnastructure_plot_folder)
    
    print(f'Processed {len(input_files)} DNA sequences in {args.input_folder}')

if __name__ == '__main__':
    main()


