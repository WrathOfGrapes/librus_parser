import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
import glob

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


def index_zip(zip_path, tag_list, target_folder, start_from=None, ):
    result_path = '%s/%s.csv' % (target_folder, os.path.split(zip_path)[-1][:-4])
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

zip_wildcard = "D:\\data\\librusec\\librusEC\\*.zip"
target_folder = 'results/indexes'

for zip_path in tqdm(glob.glob(zip_wildcard)):
    if not 'information' in os.path.split(zip_path)[-1]:
        index_zip(zip_path, keyword_list, target_folder)

with open(f"{target_folder}/united.csv", 'w', encoding='utf8') as united_csv:
    header_not_written = True
    for csv_file in glob.glob(f"{target_folder}/*.csv"):
        if 'united.csv' in csv_file:
            continue
        with open(csv_file, 'r', encoding='utf8') as f:
            try:
                if header_not_written:
                    header_not_written = False
                    line = ' '
                else:
                    line = f.readline()
                while len(line) > 0:
                    line = f.readline()
                    united_csv.write(line)
            except Exception as e:
                print(e)
                print(csv_file)
                print(line)
