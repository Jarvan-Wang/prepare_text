#!/usr/bin/env python
from __future__ import print_function
import re,argparse,sys
def strQ2B(ustring):
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
    
def strB2Q(ustring):
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
def full_width2half_width(line):
	return strQ2B(line)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Change full-width alphabet to half-width alphabet in text.")
	parser.add_argument("--field_begin", type=int)
	parser.add_argument("input_transcription",
	                    help="Input Transcription")
	parser.add_argument("output_transcription",
	                    help="Output Transcription")
	args = parser.parse_args()
	with open(args.input_transcription, encoding='gbk') as f_in, open(args.output_transcription, "w", encoding='gbk') as f_out:
		for line in f_in:
			splits = line.split()
			target = [strQ2B(split) for split in splits[args.field_begin:]]
			new_line = " ".join(splits[0:args.field_begin]+target)
			f_out.write(new_line + '\n')
