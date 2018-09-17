import requests
import json
import re
import sys

with open(sys.argv[1],'r') as f:
     data_dict = json.load(f)
     from pprint import pprint
     #pprint(data_dict)

# load the database to firebase
url = 'https://inf551-hw1-chang.firebaseio.com/.json'
response = requests.put(url, json=data_dict)

# read stop words
stopwords = []
with open('stopwords.txt') as ff:
    for line in ff.readlines():
        line = line.strip('\n')
        stopwords.append(line)
# print stopwords
r1=re.compile(r'\<i\>')
r2='[^-a-zA-Z0-9]'
# create inverted index for the motivation content of laureates
inverted_dict_list = []
for i in data_dict['prizes']:
    for x in i['laureates']:
        x.setdefault('motivation', None)
        if x['motivation'] is None :
            continue
        else:
            for y in x['motivation'].strip('"').split():
                if y=='-':
                    continue
                y=re.sub(r1,'',y.lower())
                y=re.sub(r2,'',y.lower())
                if y.lower() not in stopwords:
                    inverted_dict_list.append({y.lower().strip(',') : x['id']})

new_dic = {}
new_inv_dict_list = []
for j in inverted_dict_list:
    for k, v in j.items():
        new_dic.setdefault(k, []).append(v)

new_inv_dict_list = [{k:v} for k, v in new_dic.items()]
# pprint(new_inv_dict_list)

for a in new_inv_dict_list:
    for b in stopwords:
        if b in a:
            del a[b]

while {} in new_inv_dict_list:
    new_inv_dict_list.remove({})

# pprint(new_inv_dict_list)
new_inv_dict={}
for dic in new_inv_dict_list:
    new_inv_dict.setdefault(dic.keys()[0],dic.values()[0])
#new_inv_dict = {'index': new_inv_dict}
pprint(new_inv_dict)

with open('index.json', 'w') as f2:
    json.dump(new_inv_dict, f2)

with open('index.json', 'r') as f3:
    index_data = json.load(f3)

response = requests.put('https://inf551-hw1-chang.firebaseio.com/index.json', json=new_inv_dict)