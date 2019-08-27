# coding=utf-8
import jieba
import gensim

print(jieba.user_word_tag_tab)
string=['上海市浦东新区世纪大道100号楼501','上海市世纪大道100号楼501']

texts_list=[]
for sentence in string:
    sentence_list=[ word for word in jieba.cut(sentence)]
    texts_list.append(sentence_list)

dictionary=gensim.corpora.Dictionary(texts_list)
print(dictionary)
print(dictionary.token2id)
