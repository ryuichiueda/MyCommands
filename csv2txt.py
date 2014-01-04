#!/usr/bin/python
#coding: utf-8

import os,sys

buf = ""

def bufFlush(ret):
	global buf
	if ret:
		if len(buf) != 0:
			print buf.encode("utf_8")
		else:
			print "_"
	else:
		if len(buf) != 0:
			print buf.encode("utf_8"),
		else:
			print "_",
	

def trans(ch,state):
	global buf
	start = 0
	no_esc = 1
	quote = 3
	escaped = 4
	double_quote = 5

	if state == start:
		if ch == "\n":
			bufFlush(True)
		elif ch == ",":
			bufFlush(False)
		elif ch == '"':
			state = quote
		elif ch == ' ':
			state = no_esc 
			buf += '_'
		elif ch == '_':
			state = no_esc 
			buf += '\\_'
		elif ch == '\\':
			state = no_esc 
			buf += '\\\\'
		else:
			state = no_esc 
			buf += ch
	elif state == no_esc:
		if ch == "\n":
			state = start
			bufFlush(True)
			buf = ""
		elif ch == ",":
			state = start
			bufFlush(False)
			buf = ""
		elif ch == '"':
			sys.exit(1)
		elif ch == ' ':
			buf += '_'
		elif ch == '_':
			buf += '\\_'
		elif ch == '\\':
			buf += '\\\\'
		else:
			buf += ch
	elif state == quote:
		if ch == "\n":
			buf += "\\n"
			state = escaped
		elif ch == '"':
			state = double_quote
		else:
			buf += ch
			state = escaped
	elif state == escaped:
		if ch == "\n":
			buf += "\\n"
		elif ch == '"':
			state = double_quote
		elif ch == ' ':
			buf += '_'
		elif ch == '_':
			buf += '\\_'
		elif ch == '\\':
			buf += '\\\\'
		else:
			buf += ch
	elif state == double_quote:
		if ch == "\n":
			bufFlush(True)
			buf = ""
			state = start
		elif ch == ",":
			bufFlush(False)
			buf = ""
			state = start
		elif ch == '"':
			buf += '"'
			state = quote
		else:
			buf += ch
			state = no_esc

	return state

if __name__ == "__main__":

	state = 0

	for line in sys.stdin:
		line = line.decode("utf_8")
		if line[-1] != '\n':
			line = line + '\n'
		for ch in line:
			state = trans(ch,state)
