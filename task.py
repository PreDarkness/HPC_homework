import csv
import sys
#找出最大值，为了计算量，执行了多次排序，然后取最后一个值
def selection_sort(arr):
    """选择排序"""
    # 第一层for表示循环选择的遍数
    for i in range(len(arr) - 1):
        # 将起始元素设为最小元素
        min_index = i
        # 第二层for表示最小元素和后面的元素逐个比较
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                # 如果当前元素比最小元素小，则把当前元素角标记为最小元素角标
                min_index = j
        # 查找一遍后将最小元素与起始元素互换
        arr[min_index], arr[i] = arr[i], arr[min_index]
    return arr

role = sys.argv[1]
n = sys.argv[2]
if int(role) == -1:
    fh = open('data.csv')
else:
    fh = open('data'+role+'.csv')
data = csv.reader(fh)
li = []
for row in data:
    li = row

list = []
for i in li:
    list.append(int(i))
# print(list)
for i in range(1000):
    selection_sort(list)
print(list[-1])
