# author :  Wang Peng
# Topic : Match Alab Num with Chinese Num
from __future__ import unicode_literals
import re
import os
import docx
from glob import glob
import json


def write_result(doc, para_no, alab_chn_list, crt_chn_list, cor_ornot):

    val_text_all = []
    doc = os.path.splitext(os.path.split(doc)[1])[0]

    #with open('./test_result/alab_chn_cpy-wuxi1-1.txt', 'a') as f:

    dict_num = zip(para_no, alab_chn_list, crt_chn_list, cor_ornot)
    ft_str = []
    m_str = []
    dict_num_w ={}
    for fn, ft, m, rw in dict_num:
            ft_str = ''.join(str(ft).replace('[','',1).rsplit(']',1))
            m_str = ''.join(str(m).replace('[','',1).rsplit(']',1))
            dict_num_w[doc]=fn, ft_str, m_str, rw
    #dict_num_w = dict(zip(para_no, ft_str, m_str, cor_ornot))
    print(json.dumps(dict_num_w,  indent=4, ensure_ascii=False))

    #return val_text_all

dict_len ={1:'', 2:'拾', 3:'佰', 4:'仟', 5:'万', 6:'拾万', 7:'佰万', 8:'仟万', 9:'亿'}
dict_num = {1:'壹', 2:'贰', 3:'叁', 4:'肆', 5:'伍', 6:'陆', 7:'柒', 8:'捌', 9:'玖', 0:'零'}

def alab_tf_chn(num):
    chn_str = ''
    length = len(num)
    num_1 = enumerate(num)
    #for _,n in num_1:
    #    print('number is {}'.format(n))
    index=0
    numlist = {}
    for i, n in num_1:
        #print(i,n)
        if n != '0':
            numlist[index] = [length-i]
            numlist[index].append(dict_num[int(n)])
            numlist[index].append(dict_len[length-i])
            index = index + 1

        #elif n=='0' and len(num_1)!=1 and i==0:

        elif n == '0' and len(num) == 1:
            chn_str = dict_num[0]

    for idx in numlist:
        if idx + 1 >= len(numlist):
            break
        elif numlist[idx][0]-numlist[idx+1][0] > 1:
            numlist[idx].append('零')
    #print('numlist={}'.format(numlist))
    #print(numlist)

    for i in numlist:
        chn_str = chn_str + ''.join(numlist[i][1:])

    return  chn_str


def text_num_match(doc_path):
    for doc in sorted(doc_path):

        try:
            file = docx.Document(doc)
            print('The Doc name is {}'.format(doc))
        except:
            print('*******The File {} Is No Support To Read!*********'.format(doc))
            continue

        error_para_list = []
        doc_error_list = []
        doc_corr_chn = []
        CoW = []
        error_tab_list = []
        tab_error_list = []
        tab_corr_chn = []
        tRoW = []
        for para in file.paragraphs: # read the content from word documents
            alab_num_1 = []
            chn_num_1 = []
            alab_num_tf = []
            alab_index = []
            chn_index = []
            para_index = []
            para_error_list = []
            para_corr_chn = []
            alab_num = []
            chn_num = []
            #if re.match('\d', para.text):
                #para_num = para.text

            para_index = para.text[:10]
            #if para.text == '' | '\d':
                #break
            #print("段落数:{}".format(para_index))

            white_text = re.sub("[{}+' '+\s+\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）+]", '', para.text)
            #print('the content: {}'.format(white_text))

            alab_num_iter = re.finditer(r'([\d.]+[万元])', white_text)

            for item in alab_num_iter:
                #print(item.span()[0], item.group())
                alab_index.append(item.span()[0])
                alab_num.append(item.group())
            #print(alab_num)

            chn_num_iter = re.finditer(r'(?<!\d)[壹贰叁肆伍陆柒捌玖万仟千佰百拾亿零]+元+[零壹贰叁肆伍陆柒捌玖角分]*', white_text)

            for item in chn_num_iter:
                chn_index.append(item.span()[0])
                chn_num.append(item.group())
            #print(chn_num)

            #print(chn_index)
            alab_dict = dict(zip(alab_index, alab_num))
            #print(alab_dict)
            chn_dict = dict(zip(chn_index, chn_num))
            #print(chn_dict)
            mth_item = 0
            alab_num_reg = []
            chn_num_reg = []
            if len(alab_num)!=0 and len(chn_num)!=0:
                #print('alab_num ={}'.format(alab_num))
                #print('chn_num={}'.format(chn_num))
                if len(alab_num) != len(chn_num):   # find the match pairs of (alab_num, chn_num)
                    if chn_index[0]>alab_index[0]:
                        for item in chn_index:
                            for item1 in alab_index:
                                if 0 < item - item1 < item - mth_item:
                                    mth_item = item1
                                    alab_index.remove(item1)

                            alab_num_reg.append(alab_dict[mth_item])

                            chn_num_reg.append(chn_dict[item])
                        #print('chn_num_reg is {}'.format(chn_num_reg))
                    else:
                        for item in alab_index:
                            k = mth_item
                            for item1 in chn_index:
                                if 0 < item - item1 < item - mth_item:
                                    mth_item = item1

                            if k != mth_item:
                                alab_num_reg.append(alab_dict[item])
                                chn_num_reg.append(chn_dict[mth_item])
                        print(alab_num_reg)
                        print(chn_num_reg)
                else:
                    #
                    alab_num_reg = alab_num
                    #print('alab_num_reg is {}'.format(alab_num_reg))
                    chn_num_reg = chn_num
                    #print('chn_num_reg is {}'.format(chn_num_reg))
            #else:
                #alab_num_reg = []
                #chn_num_reg = []

            for item in alab_num_reg:
                item = item.strip('元')
                alab_num_1.append(item)  # alab_num_1 去掉‘元’字的序列
            for item in chn_num_reg:
                item = item.strip('元')
                chn_num_1.append(item) # chn_num_1 去掉‘元’字的序列


            #transfer alab_num to chn_num
            for num in alab_num_1:
                num_k = ''
                num_a = ''
                num_t = ''
                chn_str_t = ''
                zerolen=0
                if num.find('万')!=-1:
                    num_k = num
                    num = num.strip('万')
                    num_s = num.split('.')
                    num = num_s[0]

                    if len(num_s)>1:
                        if len(num_s[1])<4:
                            zerolen = 4-len(num_s[1])
                        for i in range(zerolen):
                            num_s[1] = num_s[1] + '0'
                        num_t = num_s[1]

                elif num.find('万')==-1:
                    if num.find('.')!=-1:
                        num_s = num.split('.')
                        num = num_s[0] #小数点前位数
                        num_a = num_s[1] #小数点后位数


                chn_str = alab_tf_chn(num) # alab num tranform to chn num

                if num_t != '':
                    chn_str_t = alab_tf_chn(num_t)
                    if num_t[0] == '0':
                        chn_str_t = '零'+ chn_str_t


                #print('chn_str={}'.format(chn_str))
                #print(chn_str)
                #print('num_k is {}'.format(num_k))
                if num_k.find('万') != -1 and num != '0':
                    chn_str = chn_str + '万'
                #print('chn_str is {}'.format(chn_str))
                if chn_str == '零' and chn_str_t != '':
                    chn_str = ''
                chn_str = chn_str + chn_str_t
                chn_str_1 = re.findall('万',chn_str)

                if len(chn_str_1)>1:
                    #print(len(chn_str_1))
                    chn_str=chn_str.replace('万', '', (chn_str.count('万')-1))

                #print('the alab tranfer to chn is:{}'.format(chn_str))
                num_a_chn = '' #小数点后数字的中文
                if len(num_a)!=0:
                    num_a_chn += '元'
                    num_a_chn += dict_num[int(num_a[0])]+'角'
                    if len(num_a)==2:
                        num_a_chn += dict_num[int(num_a[1])]+'分'
                    chn_str = chn_str + num_a_chn

                alab_num_tf.append(chn_str) # alab数字对应的正确大写数字列表
                #print('alab_num_tf={}'.format(alab_num_tf))
            #compare chn_str with chn_num
            for index, correct_chn in enumerate(alab_num_tf):
                if correct_chn != chn_num_1[index]:

                    para_error_list.append([alab_num_1[index],chn_num_1[index]])
                    para_corr_chn.append(alab_num_tf[index])

            #print('正确的大写数字是{}'.format(para_corr_chn))
            #if len(para_corr_chn) != 0:

            #print('para_error_list: {}'.format(para_error_list))
            if len(para_error_list) > 0:
                error_para_list.append(para_index)
                doc_error_list.append(para_error_list)
                doc_corr_chn.append(para_corr_chn)
                CoW.append('不一致')


        #print(error_para_list)
        #print('正确的大写数字是{}'.format(doc_corr_chn))
        #print('******{}'.format(doc_error_list))


        if len(error_para_list) > 0:
            #CoW = ['不一致']
            write_result(doc, error_para_list, doc_error_list, doc_corr_chn, CoW)

        else:
            error_para_list = doc_error_list = doc_corr_chn = [' ']
            CoW = ['一致']
            write_result(doc, error_para_list, doc_error_list, doc_corr_chn, CoW)




        '''
        if len(error) > 0:
            print('*****The {} paragraph has wrong num, the error items are:{}, the correct chinese number\
            should be:{}\n'.format(para_num, error, chn_str))

        else:
            print('*****The {} paragraph is total correct!\n'.format(para_num))
        para_index = para_index + 1
        '''
