import re
n = '每年缴纳金额贰拾壹万零壹佰伍拾分伍元分柒陆, 500元/千元处罚'
l = '乙方承诺年度信息化收入新增发展目标6000元，差额部分按500元/千元处罚，1213324元， 1212万元，123234万， 1212.00万元元'
chn_index=[]
chn_num=[]
alab_index=[]
alab_num=[]
chn_num_iter = re.finditer(r'(?<!\d)[壹贰叁肆伍陆柒捌玖万仟千佰百拾亿零/]+元+[零壹贰叁肆伍陆柒捌玖角分]*', n)
alab_num_iter = re.finditer(r'([\d./]+[千万]*元)', l)
for item in chn_num_iter:
        chn_index.append(item.span()[0])
        chn_num.append(item.group())
for item in alab_num_iter:
    #print(item.span()[0], item.group())
    alab_index.append(item.span()[0])
    alab_num.append(item.group())
print(alab_num)
print(chn_num)

for i in chn_num:
    if i.find('/')!=-1:
        chn_num.remove(i)

print(chn_num)
