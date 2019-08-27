import os

def norm_filename(filename_list):
    for fn in filename_list:
        name = os.path.splitext(fn)[0]
        suffix = os.path.splitext(fn)[1]
        if suffix == '.doc':
            newname = name +'.docx'
            os.rename(fn,newname)
    return filename_list


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

    #doc_path = glob('./test_doc/*.*')
    file_list = readoc('./contract_zxj/wuxihetong/wxht1')
    #file_list = readoc('./test1')
    #print(file_list)
    nfilename = norm_filename(file_list)
    print(nfilename)
