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
    file_name, file_extension = os.path.splitext(file_path)  # 使用完整路径
    file_counter = 1
    output_file = None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # 如果行中包含"ENERGY"并且output_file不为空，则关闭当前文件并准备写入新文件
                if "ENERGY" in line and output_file:
                    output_file.close()
                    print(f"完成：{output_file.name}")
                    file_counter += 1
                
                # 如果行中包含"ENERGY"或者output_file为空，则创建新文件
                if "ENERGY" in line or output_file is None:
                    new_file_name = f"{file_name}_{file_counter}{file_extension}"
                    if os.path.exists(new_file_name):
                        print(f"文件 {new_file_name} 已存在，跳过创建")
                        continue  # 如果文件已存在，则跳过创建并继续读取下一行
                    output_file = open(new_file_name, 'w')  # 新文件将在原路径下创建
                    print(f"创建新文件：{new_file_name}")
                
                output_file.write(line)

        if output_file:
            output_file.close()
            print(f"完成：{output_file.name}")

    except IOError as e:
        print(f"文件读写错误：{e}", file=sys.stderr)
    except Exception as e:
        print(f"发生错误：{e}", file=sys.stderr)
    finally:
        if output_file and not output_file.closed:
            output_file.close()

def main():
    """
    主函数，用于解析命令行参数并调用分割文件的函数。
    """
    parser = argparse.ArgumentParser(description="Split .ct or .dbn file into multiple files")
    parser.add_argument("-ss", "--filename", help="Path to the .ct or .dbn file", required=True)
    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print(f"错误：文件 {args.filename} 不存在.", file=sys.stderr)
        sys.exit(1)

    print("开始分割文件...")
    try:
        split_ss_file(args.filename)
        print("文件分割成功。")
    except Exception as e:
        print(f"无法分割文件：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

