import pandas as pd
import os
import sys

def create_dbn_files(input_file, output_folder):
    # 读取Excel文件
    df = pd.read_excel(input_file)
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历每一行，生成对应的.dbn文件
    for index, row in df.iterrows():
        pdb = row['PDB']
        sequence = row['Sequence']
        structure = row['Experimental secondary structure']
        
        # 创建.dbn文件内容
        dbn_content = f">{pdb}\n{sequence}\n{structure}"
        
        # 写入文件
        file_path = os.path.join(output_folder, f"{pdb}.dbn")
        with open(file_path, 'w') as file:
            file.write(dbn_content)
    
    print("所有.dbn文件已生成并保存到", output_folder)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script.py <input_file> <output_folder>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    
    create_dbn_files(input_file, output_folder)
