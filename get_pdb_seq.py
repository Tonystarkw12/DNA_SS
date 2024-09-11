import requests
import re

def fetch_pdb_data(pdb_id):
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for PDB ID {pdb_id}")
        return None

def extract_sequence_from_contents(contents):
    # 以逗号为分隔符分开每一部分
    parts = contents.split(',')
    sequences = set()  # 使用集合来存储找到的序列以避免重复
    for part in parts:
        # 寻找四个或更多连续的ATGC字符组成的序列
        match = re.findall(r'[ATGC]{4,}', part)
        sequences.update(match)
    if sequences:
        return ', '.join(sequences)  # 返回所有找到的唯一序列
    return "No sequence found"  # 如果没有找到序列，返回默认信息

def get_sequences(pdb_ids):
    results = {}
    for pdb_id in pdb_ids:
        data = fetch_pdb_data(pdb_id)
        if data:
            contents = data.get('pdbx_nmr_sample_details', [{}])[0].get('contents', "")
            sequence = extract_sequence_from_contents(contents)
            results[pdb_id] = sequence
        else:
            results[pdb_id] = "Data retrieval failed"
    return results

def main():
    # 输入PDB ID列表
    pdb_ids = ["1PQT", "2K71"]  # 这里输入你的PDB ID列表
    sequences = get_sequences(pdb_ids)
    for pdb_id, sequence in sequences.items():
        print(f"PDB ID: {pdb_id}, Extracted Sequence: {sequence}")

main()
