#!/usr/bin/env python
def Mymd5(str):
	import hashlib
	import types
	if type(str) is types.StringType:
		md = hashlib.md5()
		md.update(str)
		return md.hexdigest()
	else:
		return ''