# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from ckip import CKIPSegmenter, CKIPParser
import codecs
import time
from collections import Counter
import io

f = codecs.open("target.txt",'r','utf8')
f2 = codecs.open("target_seg.txt",'w','utf8')
r_txt = f.readlines()
content = []
num_part_sentence = 0

for sentence in r_txt:
    part_sentence = []

    pos = sentence.find(u"。")
    if pos == -1:
        pos = sentence.find(u"？")

    while pos != -1:
        part_sentence.append(sentence[:pos])
        num_part_sentence += 1

        sentence = sentence[pos+1:]
        pos = sentence.find(u"。")
        if pos == -1:
            pos = sentence.find(u"？")

    if len(part_sentence) == 0:
        part_sentence.append(u"".join(sentence))
        num_part_sentence += 1

    content.append(part_sentence)

f_account = codecs.open("ckip_account.txt",'r')
account_info = f_account.readlines()

segmenter = CKIPSegmenter(account_info[0][:-1], account_info[1][:-1])

j = 0
words = []
for sentence in content:

    for line in sentence:
        if line == u"\n":
            continue

        j+=1
        print(str(j)+"/"+str(num_part_sentence))
        print(line)

        result = segmenter.process(line)
        if result['status_code'] != '0':
            print('Process Failure: ' + result['status'])

        for sent in result['result']:
            for term in sent:
                words.append(term['term'])

        time.sleep(3)

f2.write(u' '.join(words))
