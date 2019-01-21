
"""

Created on Sat January 5th 18:01:29 2019



@author: zhj

"""
# 需要用到深拷贝
import copy

def print_cheet_without_infer(cheet):
    print()
    for line in cheet:
        for num in line:
            print('{:^3}'.format(num), end='')
        print()

def print_cheet_without_infer_to_input_again(cheet):
    print()
    for line in cheet:
        print(','.join([str(x) for x in line]).replace('-1', ' '))

def print_cheet_with_infer(cheet):
    print()
    for line in cheet:
        for infer in line:
            print('{:^15}'.format(str(infer).replace(' ', '')), end='')
        print()

def infer(cheet, cheet_origin):
    finish = True # 如果数组中的所有元素都已经推断出，则finish为True
    for i in range(9):
        for j in range(9):
            if cheet_origin[i][j] == -1:
                finish = False # 数组中尚有元素未推断出，finish为False
                infer_set = set(range(1, 10)) # 初始化推断信息
                # 通过行和列不能包含相同的数字进行推断
                for k in range(9):
                    if k != j and cheet_origin[i][k] != -1:
                        infer_set.discard(cheet[i][k])
                    if k != i and cheet_origin[k][j] != -1:
                        infer_set.discard(cheet[k][j])
                # 通过九宫格内不能包含相同的数字进行推断
                x = j // 3 * 3
                y = i // 3 * 3
                for m in range(y, y + 3):
                    for n in range(x, x + 3):
                        if (m != i or n != j) and cheet_origin[m][n] != -1:
                            infer_set.discard(cheet[m][n])
                # 判断此位置的推断信息，据此控制程序流程
                if len(infer_set) == 1:
                    cheet[i][j] = infer_set.pop()
                    cheet_origin[i][j] = cheet[i][j]
                    return 1
                elif len(infer_set) == 0:
                    return -1
                else:
                    cheet[i][j] = infer_set
    if finish:
        return 2
    else:
        return 0

def power_set(s):
    set_list = []
    l = list(s)
    n = len(l)
    # 非空，所以下界为1；真子集，所以上界是2的n次方
    for i in range(1, 2**n - 1):
        combo = set()
        for j in range(n):
            if (i >> j) % 2 == 1:
                combo.add(l[j])
        set_list.append(combo)
    set_list = sorted(set_list, key=lambda x: len(x))
    return set_list

def deep_infer(cheet, cheet_origin):
    change = False # 推断信息是否有修改的标志

    # 根据每一行已有的推断信息进行推断
    for i in range(9):
        # 求并集
        union_set = set()
        for j in range(9):
            if isinstance(cheet[i][j], set):
                union_set = union_set.union(cheet[i][j])
        # 遍历根据长度排序的所有非空真子集
        for s in power_set(union_set):
            contain_set_list = [] # 保存列号
            finish = True # 若此行中的所有列上的推断信息的长度都小于等于集合s的长度，则可以提前退出，finish为True
            satisfy = True # 若除了集合s的超集以外，此行还含有推断信息与集合s的交集不为空的位置，则不能进行推断，satisfy为False
            for j in range(9):
                if isinstance(cheet[i][j], set):
                    if len(cheet[i][j]) > len(s):
                        finish = False
                    if s.issubset(cheet[i][j]):
                        contain_set_list.append(j)
                    elif len(s.intersection(cheet[i][j])) > 0:
                        satisfy = False
            if finish:
                break
            if not satisfy:
                continue
            if len(contain_set_list) <= len(s) and len(contain_set_list) > 0:
                # 若s长度为1，则表明已经明确推断出此位置的数字，于是将set中的元素提取出来放到此位置上
                if len(s) == 1:
                    j = contain_set_list[0]
                    cheet[i][j] = s.pop()
                    cheet_origin[i][j] = cheet[i][j]
                    return 1
                for j in contain_set_list:
                    if len(cheet[i][j]) > len(s):
                        cheet[i][j] = s.copy()
                        change = True
    # 根据每一列已有的推断信息进行推断，和前面类似
    for j in range(9):
        union_set = set()
        for i in range(9):
            if isinstance(cheet[i][j], set):
                union_set = union_set.union(cheet[i][j])
        for s in power_set(union_set):
            contain_set_list = []
            finish = True
            satisfy = True
            for i in range(9):
                if isinstance(cheet[i][j], set):
                    if len(cheet[i][j]) > len(s):
                        finish = False
                    if s.issubset(cheet[i][j]):
                        contain_set_list.append(i)
                    elif len(s.intersection(cheet[i][j])) > 0:
                        satisfy = False
            if finish:
                break
            if not satisfy:
                continue
            if len(contain_set_list) <= len(s) and len(contain_set_list) > 0:
                if len(s) == 1:
                    i = contain_set_list[0]
                    cheet[i][j] = s.pop()
                    cheet_origin[i][j] = cheet[i][j]
                    return 1
                for i in contain_set_list:
                    if len(cheet[i][j]) > len(s):
                        cheet[i][j] = s.copy()
                        change = True
    # 根据每一九宫格已有的推断信息进行推断，和前面类似
    for m in range(3):
        for n in range(3):
            union_set = set()
            for i in range(m * 3, m * 3 + 3):
                for j in range(n * 3, n * 3 + 3):
                    if isinstance(cheet[i][j], set):
                        union_set = union_set.union(cheet[i][j])
            for s in power_set(union_set):
                contain_set_list = []
                finish = True
                satisfy = True
                for i in range(m * 3, m * 3 + 3):
                    for j in range(n * 3, n * 3 + 3):
                        if isinstance(cheet[i][j], set):
                            if len(cheet[i][j]) > len(s):
                                finish = False
                            if s.issubset(cheet[i][j]):
                                contain_set_list.append((i, j))
                            elif len(s.intersection(cheet[i][j])) > 0:
                                satisfy = False
                if finish:
                    break
                if not satisfy:
                    continue
                if len(contain_set_list) <= len(s) and len(contain_set_list) > 0:
                    if len(s) == 1:
                        i, j = contain_set_list[0]
                        cheet[i][j] = s.pop()
                        cheet_origin[i][j] = cheet[i][j]
                        return 1
                    for i, j in contain_set_list:
                        if len(cheet[i][j]) > len(s):
                            cheet[i][j] = s.copy()
                            change = True

    if not change:
        return 2
    else:
        return 0

def find_min_to_guess(cheet_with_infer):
    '''找到并返回一个推断信息的长度最小的位置'''
    min_length = 10 # 初始化最小长度标记
    for i in range(9):
        for j in range(9):
            if isinstance(cheet_with_infer[i][j], set):
                length = len(cheet_with_infer[i][j])
                if min_length > length:
                    min_length = length
                    m = i
                    n = j
    return m, n

def start(cheet_with_infer, cheet_without_infer):
    '''开始进行推断，若推断成功，则返回True，否则返回False'''
    while True:
        print_cheet_without_infer(cheet_without_infer)
        res = infer(cheet_with_infer, cheet_without_infer)
        if res == 1:
            continue
        elif res == 2:
            return True
        elif res == -1:
            return False
        while True:
            res = deep_infer(cheet_with_infer, cheet_without_infer)
            if res == 1:
                break
            elif res == 2:
                # 无法继续进行推断，于是在推断信息长度最小的位置进行假设，然后继续进行推断（递归），若猜测错误，则进行回溯
                print_cheet_without_infer_to_input_again(cheet_without_infer)
                print_cheet_with_infer(cheet_with_infer)
                print('Can not continue refer! Begin guess!')
                i, j = find_min_to_guess(cheet_with_infer)
                for num in cheet_with_infer[i][j]:
                    new_cheet_with_infer = copy.deepcopy(cheet_with_infer)
                    new_cheet_without_infer = copy.deepcopy(cheet_without_infer)
                    new_cheet_with_infer[i][j] = num
                    new_cheet_without_infer[i][j] = num
                    res = start(new_cheet_with_infer, new_cheet_without_infer)
                    if res:
                        cheet_with_infer.clear()
                        cheet_with_infer.extend(new_cheet_with_infer)
                        cheet_without_infer.clear()
                        cheet_without_infer.extend(new_cheet_without_infer)
                        return True
                    else:
                        print('Guess error, begin next guess!')


# 用户通过图形界面输入题目信息，程序通过图形界面展示结果
import tkinter
import tkinter.messagebox

def infer_handler():
    # 没有推断信息的数组
    cheet_without_infer = []
    for labels in all_labels:
        nums = []
        for label in labels:
            if label['text']:
                nums.append(int(label['text']))
            else:
                nums.append(-1)
        cheet_without_infer.append(nums)

    # 有推断信息的数组，推断信息在推断的过程中加入
    cheet_with_infer = copy.deepcopy(cheet_without_infer)

    # 开始推断
    res = start(cheet_with_infer, cheet_without_infer)
    if not res:
        tkinter.messagebox.showerror('题目信息有误，无法进行推断！')

    for i in range(9):
        for j in range(9):
            all_labels[i][j]['text'] = str(cheet_without_infer[i][j])

def clear_handler():
    for labels in all_labels:
        for label in labels:
            label['text'] = ''

def change_bg(source, origin_color):
    for labels in all_labels:
        for label in labels:
            label['bg'] = origin_color
    source['bg'] = 'skyblue'

def keyboard_handler(event):
    if event.char.isdigit() or event.keycode == 8:
        for labels in all_labels:
            for label in labels:
                if label['bg'] == 'skyblue':
                    if event.keycode == 8:
                        label['text'] = ''
                    else:
                        label['text'] = event.char

root = tkinter.Tk()
root.resizable(False, False)
root.title('数独解题器')
root.bind_all('<Any-KeyPress>', keyboard_handler)
# 九宫格面板
top_frame = tkinter.Frame(root)
top_frame.pack()
all_labels = []
for i in range(9):
    row_labels = []
    for j in range(9):
        label = tkinter.Label(top_frame, font=('', 18), width=2, height=1, relief=tkinter.RAISED)
        origin_color = label['bg']
        label.bind('<Button-1>', lambda event, label=label:change_bg(label, origin_color))
        label.grid(row=i, column=j)
        row_labels.append(label)
    all_labels.append(row_labels)
# 底部按钮面板
bottom_frame = tkinter.Frame(root)
bottom_frame.pack()
infer_button = tkinter.Button(bottom_frame, text='推断', font=('', 18), command=infer_handler)
infer_button.pack(side=tkinter.LEFT, padx=5, pady=5)
clear_button = tkinter.Button(bottom_frame, text='清空', font=('', 18), command=clear_handler)
clear_button.pack(side=tkinter.LEFT, padx=5, pady=5)
root.mainloop()
