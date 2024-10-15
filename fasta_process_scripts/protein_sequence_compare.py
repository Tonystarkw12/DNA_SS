from termcolor import colored
import argparse
def compare_strings(str1, str2):
    # 获取两个字符串的长度
    len1, len2 = len(str1), len(str2)
    print("字符串1的长度:", len1)
    print("字符串2的长度:", len2)

    # 比较长度较长的字符串
    max_len = max(len1, len2)
    differences = []
    
    # 比较字符串，并用颜色高亮不同的字符
    for i in range(max_len):
        if i < len1 and i < len2:
            if str1[i] == str2[i]:
                differences.append(str1[i])
            else:
                differences.append(colored(str1[i], 'red') + '/' + colored(str2[i], 'green'))
        elif i < len1:
            differences.append(colored(str1[i], 'red'))
        elif i < len2:
            differences.append(colored(str2[i], 'green'))
    
    # 输出带颜色的结果
    print("比较结果：")
    print(''.join(differences))

def main():
    parser = argparse.ArgumentParser(description="Compare two protein sequences")
    parser.add_argument("-s1", "--string1", help="First protein sequence")
    parser.add_argument("-s2", "--string2", help="Second protein sequence")
    args = parser.parse_args()
    str1 = args.string1
    str2 = args.string2
    compare_strings(str1, str2)
    

if __name__ == '__main__':
    main()
    
