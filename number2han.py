#!/usr/bin/env python
from __future__ import print_function
import re,argparse,sys

map_hash = {
65296:38646,
65297:19968,
65298:20108,
65299:19977,
65300:22235,
65301:20116,
65302:20845,
65303:19971,
65304:20843,
65305:20061
}
def number2han(ustring, convert_half=False, utt2text=False):
	if utt2text:
		uttid, ustring = ustring.split(sep=" ", maxsplit=1)
	rstring = ""
	for uchar in ustring:
		inside_code=ord(uchar)
		han_inside_code = map_hash.get(inside_code)
		han_inside_code_ = map_hash.get(inside_code+65248)
		if han_inside_code is not None:
			rstring += chr(han_inside_code)
		elif convert_half and han_inside_code_ is not None:
			rstring += chr(han_inside_code_)
		else:
			rstring += chr(inside_code)
	if utt2text:
		return uttid + " " + rstring
	else:
		return rstring

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="full width number to han")
	parser.add_argument("--convert-half", action='store_true')
	parser.add_argument("--field-begin", type=int, default=0)
	parser.add_argument("--utt2text", action='store_true')
	parser.add_argument("--input-charset", default='gbk')
	parser.add_argument("--output-charset", default='gbk')
	parser.add_argument("input_transcription",
	                    help="Input Transcription")
	parser.add_argument("output_transcription",
	                    help="Output Transcription")
	args = parser.parse_args()
	with open(args.input_transcription, encoding=args.input_charset) as f_in, open(args.output_transcription, "w", encoding=args.output_charset) as f_out:
		for line in f_in:
			splits = line.split()
			target = [number2han(split, args.convert_half, utt2text=False) for split in splits[args.field_begin:]]
			new_line = " ".join(splits[0:args.field_begin]+target)
			f_out.write(new_line + '\n')
