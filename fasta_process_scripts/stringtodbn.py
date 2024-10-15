#This script is for transfer a string to a dbn file
#usage python stringtodbn.py -s <string> -n <name> -e <energy> -d <dbn> 
import argparse
import os
from sys import exit
import sys
def stringtodbn(string,name,energy,dbn):
    """Transfer a string to a dbn file"""
    # Create a directory to store the individual RNA files
    output_dir = 'converted_dbn'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Write the RNA sequence to the file,注意这里使用追加因为循环反复写入
    output_file = os.path.join(output_dir, f"{name}.dbn")
    with open(output_file, 'a') as file:
        file.write(f">ENERGY = {energy} {name}\n{string.upper()}\n{dbn}\n")
    return output_file
def main():
    """
    Main function to integrate all components of the RNA analysis script.
    """
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="RNA Structure Analysis Script")
    parser.add_argument("-s","--string", help="RNA string")
    parser.add_argument("-n","--name", help="RNA name")
    parser.add_argument("-e","--energy", help="RNA energy")
    parser.add_argument("-d","--dbn", help="RNA dbn")
    args = parser.parse_args()
    try:
        # Read and process DBN file
        output_file = stringtodbn(args.string,args.name,args.energy,args.dbn)
        # Output results
        print(f"RNA sequences have been processed into correct .dbn format: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        exit(1)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        exit(1)
if __name__ == "__main__":
    main()