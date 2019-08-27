#from text_num_json import text_num_match
from text_num import text_num_match
from table_num import table_num_match
from glob import glob
import os

file_list = []
def readoc(doc_path):
    doc_list = os.listdir(doc_path)
    #print(doc_list)
    for doc in doc_list:
        doc = os.path.join(doc_path, doc)
        if os.path.isdir(doc):
            readoc(doc)
        else:
            file_list.append(doc)

    return file_list

if __name__=='__main__':
    #file_list = readoc('./contract_zxj/wuxihetong/wxht1')
    #file_list = readoc('./contract_zxj/weituojiamenglei/wtjm2')
    file_list = readoc('./test_doc')
    print(file_list)
    text_num_match(file_list)
    #table_num_match(file_list)
