import re
from collections import Counter

def reader(filename):
    with open(filename) as f:
        file = f.read()

        regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

        final = re.findall(regex, file)

        return final

def count(final):
    print(Counter(final))



if __name__ == '__main__':
    file_name = input("Enter file name: ")
    count(reader(file_name))
