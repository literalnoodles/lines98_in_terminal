import json,os,time
from termcolor import colored
os.system('color')
os.system('cls')
with open('name.json') as data_file:
    data = json.load(data_file)

def print_grid(arr):
    row = len(arr)
    col = len(arr[0])
    str = '+---'*col+'+\n'
    for i in range(row):
        for j in range(col):
            if (arr[i][j]==1):
                str += '| ' + colored('O','blue') + ' '
            elif (arr[i][j]==2):
                str += '| ' + colored('-','cyan') + ' '
            else:
                str += '|   '
        str += '|\n' + '+---'*col + '+\n'
    return str

# while True:
#     for i in range(len(data)):
#         for j in range(len(data[0])):
#             data[i][j] += 1
#             if (data[i][j] > 2):
#                 data[i][j] = 0
#             print(print_grid(data))
#             time.sleep(0.5)
#             os.system('cls')

