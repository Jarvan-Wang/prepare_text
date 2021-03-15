#!/usr/bin/env python
#coding:utf-8

import sys
import re
#sys.path.append("jieba")
#sys.path.append('./')
#from importlib import reload
#reload(sys)
from . import jieba
#sys.setdefaultencoding('utf-8')
re_han = re.compile(r"([\u4E00-\u9FD5]+)",re.U)
def jieba_segment(line):
    line = line.strip()
    uttid, sentence = line.split(sep=" ", maxsplit=1)
    #sentence = sentence.decode('utf-8')
    blocks = re_han.split(sentence)
    seg_sentence = []
    for blk in blocks:
        blk = blk.strip("\n")
        if re_han.match(blk) and len(blk) >= 2:
            seg_list = jieba.cut(blk, HMM=False)
            seg_sentence.append(" ".join(seg_list))
        elif blk != " ":
            seg_sentence.append(blk)
    return " ".join([uttid] + seg_sentence).strip()
def main(text, new_text):
    with open(text) as f_in, open(new_text, 'w') as f_out:
        for line in f_in:
            new_line = jieba_segment(line)
            f_out.write(new_line+'\n')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Jieba segmentation for kaldi text.""")
    parser.add_argument("text",
                        help="Kaldi format text file, utf8.")
    parser.add_argument("new_text",
                        help="Kaldi format new text file, utf8")
    main(parser.text, parser.new_text)
