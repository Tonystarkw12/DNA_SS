#This script is used to generate the correspondence between RNA and DNA sequences.
#Usage: python generate_correspondRNA.py <input_folder> <output_folder>
import os
import sys

def convert_t_to_u(input_dir, output_dir):
    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error, input {input_dir} dosen't exist！")
        sys.exit(1)

    # make sure the output folder exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Iterate over each file in the input directory
    try:
        for filename in os.listdir(input_dir):
            if filename.endswith('.fa'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                # Read the content of the file
                with open(input_path, 'r') as file:
                    content = file.read()
                
                # Replace all 'T' with 'U'
                modified_content = content.replace('T', 'U')
                
                # write to file
                with open(output_path, 'w') as file:
                    file.write(modified_content)
        
        print("Conversion completed！")
    except Exception as e:
        print(f"Error ：{e}")
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_folder> <output_folder>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    convert_t_to_u(input_directory, output_directory)
