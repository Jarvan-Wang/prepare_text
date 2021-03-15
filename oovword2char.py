#!/usr/bin/env python
import sys
import argparse
import re
def oovword2char_wrap(line, word_list, utt2text=True):
	if utt2text:
		uttid, line = line.split(sep=" ", maxsplit=1)
	new_words, _, oov_chars = oovword2char(line, word_list)
	if utt2text:
		line = " ".join([uttid] + new_words)
	else:
		line = " ".join(new_words)
	if len(oov_chars) == 0:
		return line
	else:
		return None
def oovword2char_wrap_with_oov(line, word_list, utt2text=True):
	if utt2text:
		uttid, line = line.split(sep=" ", maxsplit=1)
	new_words, _, oov_chars = oovword2char(line, word_list)
	if utt2text:
		line = " ".join([uttid] + new_words)
	else:
		line = " ".join(new_words)
	return line
def oovword2char(line, word_list):
	if type(line) is str:
		line = line.rstrip().split(" ")
	new_words = []
	oov_words = set()
	oov_chars = set()
	for word in line:
		if word not in word_list:
			oov_words.add(word)
			if not re.match('[a-zA-Z\uff21-\uff3a\uff41-\uff5a]',  word):
				for char in word:
					if char not in word_list:
						oov_chars.add(char)
					else:
						new_words.append(char)
			else:
				oov_chars.add(word)
		else:
			new_words.append(word)
	return new_words, oov_words, oov_chars

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Replace Chinese words not in dict with chars.")
	parser.add_argument("-f", dest='field',
	                    help="Field option")
	parser.add_argument("symtab",
	                    help="Symbol table, like words.txt")
	parser.add_argument("input_transcription",
	                    help="Input Transcription")
	parser.add_argument("output_transcription",
	                    help="Output Transcription")
	args = parser.parse_args()
	field_begin = 0
	field_end = None
	if args.field is not None:
		field_range = args.field.split("-")
		if len(field_range) == 1:
			field_begin = field_range[0]
			field_end = field_range[0]
		elif len(field_range) == 2:
			field_begin =  int(field_range[0]) if field_range[0] != "" else 0
			field_end = int(field_range[1]) if field_range[1] != "" else None
		else:
			raise "Bad argument to -f option: %s" % args.field
	sym2int = {}
	with open(args.symtab, encoding='gbk') as f:
		for line in f:
			splits = line.rstrip().split(maxsplit = 1)
			assert(len(splits) == 2)
			sym2int[splits[0]] = splits[1]
	oov_words = set()
	oov_chars = set()
	with open(args.input_transcription, encoding='gbk') as f_in, open(args.output_transcription, "w", encoding='gbk') as f_out:
		for line in f_in:
			new_words, current_oov_words, current_oov_chars = oovword2char(line.split()[field_begin,field_end], sym2int.keys())
			if len(current_oov_chars) == 0:
					f_out.write(" ".join(new_words) + "\n")
			oov_words = oov_words.union(current_oov_words)
			oov_chars = oov_chars.union(current_oov_chars)
	print("OOV chars are:\n%s\n" % " ".join(oov_chars),file=sys.stderr)
