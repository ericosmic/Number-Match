import re

'''
dic = {1:['2','dsfa'], 2: ['qi','df','4tre','fddf']}
str=''
for i in dic:
    print(dic[i][1:])
    str = str + ''.join(dic[i][1:])

print(str)

l = ['qishi元', 'etyl元']
for i in l:
    k=i.strip('元')
    l.append(k)

print(l)
'''

s = '总租金   2500000  元，（大写：贰佰伍万元），2009年总销售额为350 万元/年,大写：叁佰伍拾万元。地方0元'
white_text = re.sub("[{}+' '+\s+\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）+]", '', s)
print(white_text)
#edit_text = enumerate(white_text)
#for i, word in edit_text:
    #print(i,word)
    #e_text.append([i,word])
#print(alab_num)
alab_index = []
chn_index = []
alab_num_reg = []
chn_num_reg = []
alab_num = []
chn_num = []

alab_num_iter = re.finditer(r'(\d+[万元])', white_text)

#print(alab_num)
for item in alab_num_iter:
    print(item.span()[0], item.group())
    alab_index.append(item.span()[0])
    alab_num.append(item.group())


print(alab_num)
chn_num_iter = re.finditer(r'(?<!\d)[壹贰叁肆伍陆柒捌玖万仟千佰拾亿]+元', white_text)
for item in chn_num_iter:

    chn_index.append(item.span()[0])
    chn_num.append(item.group())

alab_dict = dict(zip(alab_index, alab_num))
chn_dict = dict(zip(chn_index, chn_num))
print(alab_dict)
print(chn_dict)
#for i, n in alab_dict:
#    print(i,n)
mth_item = 0
match_num = []
if len(alab_num)!=0 and len(chn_num)!=0:

    if len(alab_num) != len(chn_num):   # find the match pairs of (alab_num, chn_num)
        for item in chn_index:
            for item1 in alab_index:
                if 0 < item - item1 < item - mth_item:
                    mth_item = item1
            alab_num_reg.append(alab_dict[mth_item])
            #print('alab_num is {}'.format(alab_num_reg))
            chn_num_reg.append(chn_dict[item])

print(alab_num_reg)
print(chn_num_reg)
