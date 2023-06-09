#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Thêm các thư viện
import re
import numpy as np
import pandas as pd
# Tạo hàm kiểm tra tính hợp lệ của dữ liệu
def check_valid(line):
    lines = line.split(",")
    check_first_item = re.match('N\d{8}', lines[0])
    if len(lines) == 26 and check_first_item:
        return True
    else:
        return False
# Tạo hàm kiểm tra sự vi phạm trường hợp số lượng câu trả lời
def check_valid1(line):
    lines = line.split(",")
    if len(lines) == 26:
        return True
    else:
        return False
# Tạo hàm kiểm tra sự vi phạm trường hợp sai mã số của học sinh
def check_valid2(x):
    lines = x.split(",")
    first_item = re.match('N\d{8}',lines[0])
    if first_item:
        return True
    else:
        return False
# Tạo hàm tính điểm thi
def check_point(line):
    lines = line.split(",")
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    ans = answer_key.split(",")
    point=0
    for i in range(len(ans)):
        if lines[i+1] == ans[i]:
            point=point+4
        elif lines[i+1] =="":
            point=point+0
        else:
            point=point-1
    return point
# Tạo hàm đánh dấu kết quả của từng câu
def check_skip_false(line):
    lines = line.split(",")
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    ans = answer_key.split(",")
    list_skip = [line[0:9]]
    for i in range(len(ans)):
        if lines[i+1] == ans[i]:
            list_skip.append("T")
        elif lines[i+1] =="":
            list_skip.append("SK")
        else:
            list_skip.append("F")
    return list_skip
# Nhập đầu vào
f = input("Enter a class to grade: ")
duoi = ".txt"
k= f+duoi
list_diem = [] # Biến liệt kê điểm
list_all_skip =[] # Biến tổng hợp đánh giá tất cả câu trả lời của học sinh
tonghop =[] # Biến tổng hợp danh sách mã học sinh và điểm thi
line_count =0 # Biến đếm số lượng học sinh
lineinvalid_count=0 # Biến đếm số dòng dữ liệu không hợp lệ
# Chạy dữ liệu kiểm tra từng hàng và thống kê kết quả
try:
    a= open(k,"r")
    print("Successfully opened",k)
    print("**** ANALYZING ****")
    b=a.readlines()
    for line in b:
        line_count=line_count+1
        status = check_valid(line)
        if status == True:
            diem = check_point(line)
            skip = check_skip_false(line)
            list_diem.append(diem)
            list_all_skip.append(tuple(skip))
            str1=[line[0:9],str(diem)]
            str2=','.join(str1)
            tonghop.append(str2)
        else:
            lineinvalid_count=lineinvalid_count+1
            sai = check_valid1(line)
            sai2= check_valid2(line)
            if sai2 == False:
                print("Invalid line of data: N# is invalid")
                print(line)
            elif sai== False:
                print("Invalid line of data: does not contain exactly 26 values")
                print(line)
    if lineinvalid_count == 0:
        print("No errors found!")
    # Tạo mảng bằng thư viện numpy để thống kê
    a=np.array(list_diem)
    filter_arr= a > 80
    x=a[filter_arr]
    mean_a=str("{:.2f}".format(round(a.mean(),3)))
    max_a=a.max()
    min_a=a.min()
    range_score_a=max_a - min_a
    median_a=np.median(a)
except:
    print("Sorry, I can't find this filename")
# Tạo dataframe tổng hợp số liệu của tất cả học sinh
df=pd.DataFrame(data=list_all_skip,
                    columns=["No",1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
#Tìm câu trả lời bỏ qua nhiều nhất, số lượng học sinh tương ứng
list_skip = []
max_1=0
for i in range(1,26):
    j=df[i]
    h=j.where(j=="SK").count()
    if max_1 < h:
        max_1=h
    else:
        max_1=max_1+0
for i in range(1,26):
    j=df[i]
    h=j.where(j=="SK").count()
    if h== max_1:
        str3=[str(i),str(h),str("{:.2f}".format(h/line_count))]
        str4=" - ".join(str3)
        list_skip.append(str4)
    else:
        g=1
#Tìm câu trả lời sai nhiều nhất, số lượng học sinh tương ứng
list_false= []
max_2=0
for i in range(1,26):
    j=df[i]
    h=j.where(j=="F").count()
    if max_2 < h:
        max_2=h
    else:
        max_2=max_2+0 
for i in range(1,26):
    j=df[i]
    h=j.where(j=="F").count()
    if h== max_2:
        str5=[str(i),str(h),str("{:.2f}".format(h/line_count))]
        str6=" - ".join(str5)
        list_false.append(str6)
    else:
        g=1
# Tạo file output
new = "_grade.txt"
n= f+new
p="\n".join(tonghop)
c=open(n,'w')
c.write(p)
c.close()
#In kết quả thống kê mô tả
print("**** REPORT ****")
print("Total lines of data: ",line_count)
print("Total invalid lines of data: ",lineinvalid_count)
print("Total student of high scores:",len(x))
print("Mean score: ",mean_a)
print("Highest score: ",max_a)
print("Lowest score: ",min_a)
print("Range of scores: ",range_score_a)
print("Median score: ",median_a)
#In kết quả câu trả lời bỏ qua nhiều nhất, sai nhiều nhất
most_skip=", ".join(list_skip)
print("Question that most people skip: ",most_skip)
most_false=", ".join(list_false)
print("Question that most people answer incorrectly: ",most_false)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




