#!/usr/bin/env python
from __future__ import print_function
import re,fileinput,argparse,sys
from zhon.hanzi import characters as zh_chars
def insert_space_wrap(s):
	uttid, s = s.split(sep=" ", maxsplit=1)
	s = insert_space(s)
	return uttid + " " + s
def insert_space(text):
	pattern1=r'([%s])([%s])' % (zh_chars,zh_chars)
	pattern2=r'([%s])([0-9a-zA-Z])' % (zh_chars)
	pattern3=r'([0-9a-zA-Z])([%s])' % (zh_chars)
	while re.search(pattern1, text) is not None:
		text=re.sub(pattern1,r'\1 \2',text)
	while re.search(pattern2, text) is not None:
		text=re.sub(pattern2,r'\1 \2',text)
	while re.search(pattern3, text) is not None:
		text=re.sub(pattern3,r'\1 \2',text)
	return text
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Add space between chinese words in text and print to stdout.")
	parser.add_argument('text')
	args=parser.parse_args()
	text=""
	for line in fileinput.input(args.text):
		text+=line
	text_inserted = insert_space(text)
	print(text_inserted, end='')
