import os
import hashlib as hl
import zipfile as zf
import requests as rq
import re
import csv
#распаковать архив и зайти в папку
archive = zf.ZipFile("tiff-4.2.0_lab1.zip")
archive.extractall(os.getcwd())
os.chdir("tiff-4.2.0")
tmp = list(os.walk("."))
res2 = []
#найти текстовые файлы и их хеши
for i in tmp:
    for fn in i[2]:
        path = i[0] + "/" + fn
        if ".txt" in path:
            res2.append(fn)
            f = open(path, "rb")
            res2.append(hl.md5(f.read()).hexdigest())
            f.close()
#вывести текстовые файлы и их хеши
for i in res2:
    if ".txt" in i:
        print(i, end = " ")
    else:
        print(i)
#найти нужный файл и сохранить ссылку на сайт
target = "4636f9ae9fef12ebd56cd39586d33cfb"
link = ""
for i in tmp:
    for fn in i[2]:
        path = i[0] + "/" + fn
        f = open(path, "rb")
        if hl.md5(f.read()).hexdigest() == target:
            f.close()
            f = open(path, "r")
            link = f.read()
        f.close()
os.chdir("..")
info = rq.get(link)
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', info.text)

countries = {}
counter = 0
headers = []
for line in lines:
    if counter == 0:
        headers = re.sub("<.*?>", " ",line)
        headers = re.findall("Заболели|Умерли|Вылечились|Активные случаи", headers)
        print(headers)
    else:
        temp = re.sub('<.*?>', ';', line)
        temp = re.sub('\(.*?\)', '', temp)
        temp = re.sub(';+', ';', temp)
        temp = temp[1: len(temp)-1]
        temp = re.sub('\s(?=\d)', '', temp)
        temp = re.sub('(?<=\d)\s', '', temp)
        temp = re.sub('(?<=0)\*', '', temp)
        temp = re.sub('_', '-1', temp)
        tables = temp.split(';')
        if len(tables) == 6:
            tables.pop(0)
        country_name = re.sub('.*\s\s', '', tables[0])
        col1_val = int(tables[1])
        col2_val = int(tables[2])
        col3_val = int(tables[3])
        col4_val = int(tables[4])
        countries[country_name] = [col1_val, col2_val, col3_val, col4_val]
    counter += 1

s = open('result.csv', 'w')
s.write("\"\";"+headers[0]+";"+headers[1]+";"+headers[2]+";"+headers[3]+"\n")
for key in countries.keys():
    s.write(key+";"+str(countries[key][0])+";"+str(countries[key][1])+";"+str(countries[key][2])+";"+str(countries[key][3])+"\n")
s.close()

req = input("Введите название страны: ")
for i in range(4):
    print(headers[i], countries[req][i])