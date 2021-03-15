#!/usr/bin/env python
from __future__ import print_function
import re,fileinput,argparse,sys
from zhon.hanzi import punctuation as zh_punctuation
from string import punctuation as en_punctuation
def remove_punctuation_wrap(s, utt2text=True):
	return remove_punctuation(s, utt2text)
def remove_punctuation(s, utt2text=True):
	if utt2text:
		uttid, s = s.split(sep=" ", maxsplit=1)
	s=re.sub("[{}]+".format(en_punctuation+zh_punctuation)," ",s.strip())
	if utt2text:
		return uttid + " " + s
	else:
		return s
def remove_marksign_wrap(s, utt2text=True):
	if utt2text:
		uttid, s = s.split(sep=" ", maxsplit=1)
	s = remove_marksign(s, utt2text)
	if utt2text:
		return uttid + " " + s
	else:
		return s
def remove_marksign(s, utt2text=True):
	if utt2text:
		uttid, s = s.split(sep=" ", maxsplit=1)
	s=re.sub("\[\S+\]", " ", s.strip())
	if utt2text:
		return uttid + " " + s
	else:
		return s
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Remove punctuation in text and print to stdout.")
	parser.add_argument('text')
	args=parser.parse_args()
	text=""
	with fileinput.input(args.text) as f:
		for line in f:
			text+=line
	text_ = remove_punctuation(text, True)
	print(text_, end='')