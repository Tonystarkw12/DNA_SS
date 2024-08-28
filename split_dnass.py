#This script is used for split any multiple DNA sequences in one ct or dbn file
#Usage python split_rnass.py -ss file

import os
import sys
import argparse

def split_ss_file(file_path):
    """
    分割包含多个DNA序列的ct或dbn文件。
    
    :param file_path: .ct或.dbn文件的路径
    """
    file_name, file_extension = os.path.splitext(file_path)  
    file_counter = 1
    output_file = None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # If the line contains "ENERGY" and output_file is not empty, close the current file and prepare to write to a new file
                if "ENERGY" in line and output_file:
                    output_file.close()
                    print(f"finished：{output_file.name}")
                    file_counter += 1
                
                # If the line contains "ENERGY" or output_file is empty, a new file is created
                if "ENERGY" in line or output_file is None:
                    new_file_name = f"{file_name}_{file_counter}{file_extension}"
                    if os.path.exists(new_file_name):
                        print(f"file {new_file_name} already exists，skipping creation")
                        continue  # If the file already exists, skip creating it and continue reading the next line.
                    output_file = open(new_file_name, 'w')  # The new file will be created in the original path
                    print(f"creating new file：{new_file_name}")
                
                output_file.write(line)

        if output_file:
            output_file.close()
            print(f"sucessfully finished：{output_file.name}")

    except IOError as e:
        print(f"file read or write error：{e}", file=sys.stderr)
    except Exception as e:
        print(f"Error：{e}", file=sys.stderr)
    finally:
        if output_file and not output_file.closed:
            output_file.close()

def main():

    parser = argparse.ArgumentParser(description="Split .ct or .dbn file into multiple files")
    parser.add_argument("-ss", "--filename", help="Path to the .ct or .dbn file", required=True)
    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print(f"Error：file {args.filename} doesn't exist.", file=sys.stderr)
        sys.exit(1)

    print("Starting spliting files...")
    try:
        split_ss_file(args.filename)
        print("files ssplited successfully.")
    except Exception as e:
        print(f"can't split file：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

