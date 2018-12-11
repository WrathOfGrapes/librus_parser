import hashlib
from lxml import etree
import os






#%%
path = "data/024853.fb2"

# print(open(path, 'r', encoding='cp1251').read())

#%%

with open(path, 'rb') as fobj:
    xml = fobj.read()

# print(xml)
#%%

root = etree.XML(xml, parser=etree.XMLParser())

#%%
%%time
import xml.etree.ElementTree as ET
root = ET.parse(path)

#%%



for appt in root.getiterator():
    # paths = []
    for elem in appt.getchildren():
        # paths.append(elem.tag)
        if not elem.text:
            text = "None"
        else:
            text = elem.text

        print(appt.tag + ':::' + elem.tag + " => " + text)
        # print(':'.join(paths) + " => " + text)

#%%

import xml.etree.ElementTree as ET
def get_dict(fpath):
    res = {}
    root = ET.parse(fpath)
    for appt in root.getiterator():
        for elem in appt.getchildren():
            # text = elem.text i
            # if not elem.text:
            #     text = "None"
            # else:
            #     text = elem.text
            tag1 = appt.tag
            tag2 = elem.tag
            assert '}' in tag1 and '}' in tag2
            value = elem.text
            tag = "%s:%s" % (tag1.split('}')[-1], tag2.split('}')[-1])
            res[tag] = value
    return res
            # print(appt.tag + ':::' + elem.tag + " => " + str(elem.text))




#%%

def all_tags(fpath):
    tags = set()
    root = ET.parse(fpath)
    for appt in root.getiterator():
        tags.add(appt.tag)
    return tags
            # print(appt.tag + ':::' + elem.tag + " => " + str(elem.text))

# tags_list = []
# for file in os.listdir('data'):
#     try:
#         tags_list.append(all_tags(os.path.join('data', file)))
#     except AssertionError:
#         print(file)
#
# all_tags = set([el for one_list in tags_list for el in one_list])
# trunc_tags = [i.split('}')[-1] for i in all_tags]





#%%
import os

dicts = []

for file in os.listdir('data'):
    try:
        dicts.append(get_dict(os.path.join('data', file)))
    except AssertionError:
        print(file)



#%%




#%%
import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os

keyword_list = [
    'author:first-name',
    'author:last-name',
    'author:middle-name',
    'author:nickname',
    'publish-info:book-name',
    'publish-info:year',
    'translator:last-name',
    'translator:first-name',
    'translator:middle-name',
    'title-info:book-title']

def get_selected_tags(file_string, log, extra_text, tag_list):
    res = {}
    root = ET.fromstring(file_string)
    for appt in root.getiterator():
        tag1 = appt.tag
        if tag1 == '{http://www.gribuser.ru/xml/fictionbook/2.0}p':
            # text of the book. can ignore
            continue
        for elem in appt.getchildren():
            tag2 = elem.tag
            # assert '}' in tag1 and '}' in tag2
            value = elem.text
            tag = "%s:%s" % (tag1.split('}')[-1], tag2.split('}')[-1])
            if tag in tag_list:
                res[tag] = value
    if len(res.keys()) == 0:
        log.write("Empty file '%s\n" % extra_text)
    return res

def index_zip(zip_path, tag_list, start_from=None,):
    result_path = 'results/indexes/%s.csv' % os.path.split(zip_path)[-1][:-4]
    if os.path.exists(result_path):
        return
    z = zipfile.ZipFile(zip_path)
    zip_name = os.path.split(zip_path)[-1]
    file_list = z.namelist()
    if start_from is not None:
        file_list = [f for f in file_list if f > start_from]
    dicts = []
    for book in file_list:
        book_text = z.read(book)
        book_dict = get_selected_tags(book_text, open('D:\projects\\fb2_parser\\results\log.txt', 'w+'),
                          zip_name + '::' + book, tag_list=tag_list)
        dicts.append(book_dict)
    df = pd.DataFrame(dicts)
    df.to_csv(result_path)

# zip_dir = "D:\\data\\librusec\\librusEC\\"
# sample_zip = "D:\data\librusec\librusEC\\fb2-00-000110-067325-RUSSIAN.zip"
import glob
for zip_path in tqdm(glob.glob("D:\\data\\librusec\\librusEC\\*.zip")):
    if not 'information' in os.path.split(zip_path)[-1]:
        index_zip(zip_path, keyword_list)



#%%
import os
import pandas as pd
from tqdm import tqdm

dicts = []



with open('results/log.txt', 'w') as log_file:
    for file in tqdm(os.listdir('data')):
        try:
            tag_dict = get_selected_tags(os.path.join('data', file), log_file, '', tag_list=keyword_list)
            tag_dict['file'] = file
            dicts.append(tag_dict)
        except AssertionError:
            log_file.write("Problem with file '%s'\n" % file)

df = pd.DataFrame(dicts)


#%%


import zipfile
full_data_path = 'D:\data\librusec\librusEC'
sample_zip = "D:\data\librusec\librusEC\\fb2-00-000110-067325-RUSSIAN.zip"

z = zipfile.ZipFile(sample_zip)
# print(sorted(z.namelist()))
print(get_selected_tags(z.read('000110.fb2'), open('./log.txt', 'w'), '', tag_list=keyword_list))

z.close()

#%%
import re
import numpy as np

df = pd.read_csv(open('D:\projects\\fb2_parser\\results\indexes\\united.csv', 'r', encoding='utf-8'))
df = df[df.columns[1:]]

def normalize(year):
    try:
        digit = int(re.sub(r"[^0-9]", '', str(year)))
        if digit < 1600 or digit > 2020:
            return None
        else:
            return digit
    except ValueError:
        return None

df['year'] = df['publish-info:year'].apply(normalize)


