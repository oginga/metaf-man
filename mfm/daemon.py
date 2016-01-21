#!/usr/bin/env python  

import os
import json
import re
import MySQLdb
import ast
#import nose
#choose a root folder ie downloads
root_dir=os.path.abspath(os.path.join(os.getcwd(),'downloads'))
db_results=None

#check available files on the folder  with extensions--> .doc, .pdf, .xcl, .ppt
files= os.listdir(root_dir)


def retreive_data():
	global db_results
	db=MySQLdb.connect('localhost','root','526419','mfm')
	cursor=db.cursor()
	results=None

	sql='''SELECT * FROM meta'''
	try:
		cursor.execute(sql)
		db_results=cursor.fetchall()
		db.close()
		return True
	except:
		db.rollback
		db.close()
		return False



doc_pat=re.compile(".pdf|.txt|.docx|.pptx$")

print "FILES: ",files

doc_files_list=[file for file in files if re.findall(doc_pat,file)]
if retreive_data():
	for id in db_results:
		#print id[0],type(id[1]),list(id[1])
		
		print"IDS: ",id[0], id[2]
		meta_list=ast.literal_eval(id[2])
		for file_names in doc_files_list:
			matches={}

			print "FILE NAME: ",file_names.upper()
			for word in meta_list:
				if re.search(word.lower(),file_names.lower()):
					matches[id[0]]=matches.get(id[0],0)+1

					print matches
				else:pass


		#	if re.findall()
		#	matches[id[0]]=
'''
create dict : {filename:{26:1,27:4}}

'''

		


