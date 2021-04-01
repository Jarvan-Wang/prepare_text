#!/usr/bin/env python
from __future__ import print_function
import re,argparse,sys
def full_width2half_width(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring
    
def half_width2full_width(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        #if inside_code == 32:                                 #半角空格直接转化                  
        #    inside_code = 12288
        if inside_code > 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += chr(inside_code)
    return rstring
def full_width2half_width_wrap(s):
	uttid, s = s.split(sep=" ", maxsplit=1)
	s = full_width2width_width(s)
	return uttid + " " + s
def half_width2full_width_wrap(s):
	uttid, s = s.split(sep=" ", maxsplit=1)
	s = half_width2full_width(s)
	return uttid + " " + s

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Change half-width alphabet to full-width alphabet in text.")
	parser.add_argument("--field_begin", type=int)
	parser.add_argument("--func", default="full_width2half_width_wrap")
	parser.add_argument("input_transcription",
	                    help="Input Transcription")
	parser.add_argument("output_transcription",
	                    help="Output Transcription")
	args = parser.parse_args()
	with open(args.input_transcription, encoding='gbk') as f_in, open(args.output_transcription, "w", encoding='gbk') as f_out:
		for line in f_in:
			splits = line.split()
			target = [eval(args.func)(split) for split in splits[args.field_begin:]]
			new_line = " ".join(splits[0:args.field_begin]+target)
			f_out.write(new_line + '\n')
