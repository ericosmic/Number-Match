# -*- coding:utf-8 -*-
# /usr/bin/python


from simhash import Simhash
import jieba.posseg as pseg

class SimHaming:
    '''利用64位数，计算海明距离'''
    def haming_distance(self, code_s1, code_s2):
        x = (code_s1 ^ code_s2) & ((1 << 64) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans
    '''利用相似度计算方式,计算全文编码相似度'''
    def get_similarity(self, a, b):
        if a > b :
            return b / a
        else:
            return a / b

    '''对全文进行分词,提取全文特征,使用词性将虚词等无关字符去重'''
    def get_features(self, string):
        word_list=[word.word for word in pseg.cut(string) if word.flag[0] not in ['u','x','w','o','p','c','m','q']]   #pseg.cut(string)
        return word_list

    '''计算两个全文编码的距离'''
    def get_distance(self, code_s1, code_s2):
        return self.haming_distance(code_s1, code_s2)

    '''对全文进行编码'''
    def get_code(self, string):
        return Simhash(self.get_features(string)).value

    '''计算s1与s2之间的距离'''
    def distance(self, s1, s2):
        code_s1 = self.get_code(s1)
        code_s2 = self.get_code(s2)
        similarity = (100 - self.haming_distance(code_s1,code_s2)*100/64)/100
        return similarity


def match(text1, text2):
    #text1 = '中国移动通信公司江苏有限公司'
    #text2 = '中国联通公司江苏有限公司'
    #text2 = '中国农业银行股份有限公司'
    simer = SimHaming()
    sim = simer.distance(text1, text2)
    return sim

'''
if __name__ == '__main__':
    main()
'''
