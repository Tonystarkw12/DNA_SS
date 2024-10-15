import sys

def fasta_to_string(file_path):
    with open(file_path, 'r') as file:
        # 跳过第一行（通常是描述行）
        next(file)
        # 读取剩余的行并合并为一个字符串
        sequence = ''.join(line.strip() for line in file)
        return sequence

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <fasta file path>")
        sys.exit(1)
    fasta_file_path = sys.argv[1]
    try:
        sequence = fasta_to_string(fasta_file_path)
        print(sequence)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
