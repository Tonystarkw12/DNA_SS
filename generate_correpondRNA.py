#This script is used to generate the correspondence between RNA and DNA sequences.
#Usage: python generate_correspondRNA.py <input_folder> <output_folder>
import os
import sys

def convert_t_to_u(input_dir, output_dir):
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误：输入目录 {input_dir} 不存在！")
        sys.exit(1)

    # 确保输出目录存在，如果不存在，则创建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历输入目录中的所有文件
    try:
        for filename in os.listdir(input_dir):
            if filename.endswith('.fa'):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                # 读取原始文件
                with open(input_path, 'r') as file:
                    content = file.read()
                
                # 替换"T"为"U"
                modified_content = content.replace('T', 'U')
                
                # 写入新文件
                with open(output_path, 'w') as file:
                    file.write(modified_content)
        
        print("转换完成！")
    except Exception as e:
        print(f"处理文件时出现错误：{e}")
        sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python script.py <输入文件夹路径> <输出文件夹路径>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    convert_t_to_u(input_directory, output_directory)
