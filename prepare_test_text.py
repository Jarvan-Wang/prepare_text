#!/usr/bin/env python3
import sys,os
import argparse
#sys.path.append('./')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from importlib import reload
reload(sys)
from fenci.segjb import jieba_segment
from remove_punctuation import remove_punctuation, remove_marksign
from char_width_convert import half_width2full_width, full_width2half_width
from oovword2char import oovword2char
from insert_space import insert_space
full_width=False
def isempty(line):
	return line is None
def tolowercase(line):
	uttid, line = line.split(sep=" ", maxsplit=1)
	return uttid + " " + line.lower()
def prepare_line(line):
	if isempty(line):
		return None
	line = remove_marksign(line)
	if isempty(line):
		return None
	line = remove_punctuation(line)
	if isempty(line):
		return None
	#line = jieba_segment(line)
	#if isempty(line):
	#	return None
	if full_width:
		line = half_width2full_width(line)
	else:
		line = full_width2half_width(line)
	line = line.lower()
	if isempty(line):
		return None
	line = insert_space(line)
	if isempty(line):
		return None
	#line = oovword2char_wrap(line, word_list)
	#if isempty(line):
	#	return None
	return line
def load_word_list(symtab,codec):
	sym2int = {}
	with open(symtab, encoding=codec) as f:
		for line in f:
			splits = line.rstrip().split(maxsplit = 1)
			assert(len(splits) == 2)
			sym2int[splits[0]] = splits[1]
	word_list = sym2int.keys()
	return word_list

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="""Prepare kaldi text.
			1. remove marksign;
			2. word segmentation;
			3. remove punctuation;
			4. halt width alphabet to full width alphabet;
			5. oov_word2char;""")
	parser.add_argument("--codec", default="utf8",
	                    help="Codec to use, default=utf8")
	parser.add_argument("--full-width", action='store_true',
	                    help="Convert ascii to full width")
	parser.add_argument("input_transcription",
	                    help="Kaldi format text file")
	parser.add_argument("output_transcription",
	                    help="Kaldi format new text file")
	args = parser.parse_args()
	full_width =args.full_width
	with open(args.input_transcription, encoding=args.codec) as f_in, open(args.output_transcription, "w", encoding=args.codec) as f_out:
		i=0
		for line in f_in:
			i+=1
			line = line.rstrip()
			try:
				utt, text = line.split(maxsplit=1)
			except:
				utt = line
				text = ""
				print(f"Warning: Utterance {utt} has empty text: {line}")
			try:
				text = prepare_line(text)
				line = "{} {}".format(utt, text)
			except:
				print(f"Exception catched: {args.input_transcription} {i}th line : {line}")
				continue
			if line is not None:
				f_out.write(line+'\n')
