#This script is used to predict the secondary structure of DNA sequences using mxfold2 on a large scale.
#The input is a directory containing DNA sequences in fasta format.
import os
import sys
import argparse
import subprocess

# 运行mxfold2
def run_mxfold2(input_file, results_folder):
    try:
        file_name = os.path.basename(input_file).replace('.fa', '')
        output_file = os.path.join(results_folder, file_name + '.dbn')
        cmd = f'mxfold2 predict {input_file} > {output_file}'
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running mxfold2 on {input_file}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# 处理mxfold2的输出
def process_mxfold2(results_folder):
    try:
        files = os.listdir(results_folder)
        for file in files:
            if file.endswith('.dbn'):
                with open(os.path.join(results_folder, file), 'r') as f:
                    lines = f.readlines()
                    if len(lines) < 3:
                        print(f"Invalid .dbn file format: {file}")
                        continue
                    name = lines[0].strip().replace('>', '')
                    seq = lines[1].strip()
                    dbn = lines[2].strip().split()[0]
                    energy = lines[2].strip().split()[-1].replace('(', '').replace(')', '')
                    with open(os.path.join(results_folder, name + '.dbn'), 'w') as out:
                        out.write(f'>ENERGY = {energy} {name}\n{seq}\n{dbn}')
    except Exception as e:
        print(f"Error processing mxfold2 output: {e}")

# 画图
def plot(results_folder, plots_folder):
    try:
        os.makedirs(plots_folder, exist_ok=True)
        cmd = f'bash visualization_RNAss.bash {results_folder} {plots_folder}'
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running visualization script: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    try:
        parser = argparse.ArgumentParser(description='Process DNA secondary structures predictions on a batch profile using mxfold2')
        parser.add_argument('-i', '--input', help='Input directory containing DNA sequences in fasta format', required=True)
        parser.add_argument('-o', '--output', help='Output directory', required=True)
        args = parser.parse_args()
        
        input_folder = args.input
        output_folder = args.output
        results_folder = os.path.join(output_folder, 'results')
        plots_folder = os.path.join(output_folder, 'plots')
        
        os.makedirs(results_folder, exist_ok=True)
        
        files = os.listdir(input_folder)
        for file in files:
            if file.endswith('.fa'):
                input_file = os.path.join(input_folder, file)
                run_mxfold2(input_file, results_folder)
                
        process_mxfold2(results_folder)
        plot(results_folder, plots_folder)
    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == '__main__':
    main()
