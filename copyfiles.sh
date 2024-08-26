#!/bin/bash
# This script copies files from one directory to another directory according to the file_list
# Example: ./copyfiles.sh <source_directory> <destination_directory> <file_list>
# 检查参数数量
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <source_directory> <destination_directory> <file_list>"
    exit 1
fi

# 获取参数
source_directory=$1
destination_directory=$2
file_list=$3

# 检查源目录是否存在
if [ ! -d "$source_directory" ]; then
    echo "Source directory does not exist: $source_directory"
    exit 1
fi

# 检查目标目录是否存在，不存在则创建
if [ ! -d "$destination_directory" ]; then
    mkdir -p "$destination_directory"
fi

# 读取文件列表并复制符合条件的文件
while IFS= read -r file_prefix; do
    # 查找以file_prefix开头的文件并复制
    find "$source_directory" -type f -name "${file_prefix}*" -exec cp {} "$destination_directory" \;
done < "$file_list"

echo "Files copied successfully to $destination_directory."