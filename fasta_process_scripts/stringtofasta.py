#This script converts a string to a fasta file
#Usage: python stringtofasta.py -s string_file -n <name> -o <output_folder>
import argparse
import os
from sys import exit
import pandas as pd

def stringtofasta(input_file,output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        filename,fileext = os.path.splitext(input_file)
        if fileext == '.string':
            with open(input_file, 'r') as input_file:
                lines = input_file.readlines()
                for line in lines:
                    input_data = line.strip().split(":")
                    name = input_data[0].strip()
                    sequence = input_data[1].strip()
            #if there are "-" inside input_data, it will be removed
                    if '-' in sequence:
                        sequence = sequence.replace('-', '')
                    output_file_path = os.path.join(output_dir, name + '.fasta')
                    with open(output_file_path, 'w') as output_file:  # 使用写入模式
                        output_file.write(f">{name}\n{sequence.upper()}")
            print(f"converted to fasta file and files are saved in {output_dir}")
            
        elif fileext == '.xlsx':
            try:
                df = pd.read_excel(input_file)
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                return

            if 'Name' not in df.columns or 'Sequence' not in df.columns:
                print("Error: DataFrame must contain 'Name' and 'Sequence' columns.")
                return

            for name, sequence in zip(df['Name'], df['Sequence']):
                output_file_path = os.path.join(output_dir, name + '.fasta')
                try:
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(f">{name}\n{sequence.upper()}")
                        print(f"converted to fasta file and files are saved in {output_dir}")
                        
                except Exception as e:
                    print(f"Error writing to {output_file_path}: {e}")
    except IOError as e:
            print(f"IOError: {e}")
            exit(1)
    except Exception as e:
            print(str(e))
            exit(1)



if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Convert to fasta Script")
        parser.add_argument("-s", "--string", help="String to be converted to fasta")
        parser.add_argument("-o", "--output", help="Output folder",required=True)
        args = parser.parse_args()
        stringtofasta(args.string, args.output)  # 直接调用函数，不需要打印返回值
    except Exception as e:
        print(str(e))
        exit(1)
