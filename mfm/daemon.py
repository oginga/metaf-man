#!/usr/bin/env python  

import os
import json
import re
import MySQLdb
import ast
import operator
import shutil

#handle same number of matches
#test cases
#create daemon
#import nose
#choose a root folder ie downloads
root_dir=os.path.abspath(os.path.join(os.getcwd(),'downloads'))
db_results=None

#check available files on the folder  with extensions--> .doc, .pdf, .xcl, .ppt
files= os.listdir(root_dir)



def transfer_files(key,matches_list):
'''
Copies the files to their new location
key:string
matches_list:list

'''
	fromLocation=os.path.join(root_dir,key)
	toLocation=''
	for row in db_results:
		if row[0]==matches_list[0][0] and matches_list[0][1]!=0:
			toLocation=row[1]
			try:
				shutil.copy2(fromLocation,toLocation)
				print "Copy successful"
			except:
				print 'Error occured'

		else:pass

def retreive_data():
	'''
	Retrieves data from the database
	'''
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

print "FILES: ",files,"\n\n\n"



doc_files_list=[file for file in files if re.findall(doc_pat,file)]
matches={}
if retreive_data():
	print db_results

	for file_name in doc_files_list:
	

		tally={}	
		for id in db_results:
		
			meta_list=ast.literal_eval(id[2])
			
			count=0

			for word in meta_list:
			
				if re.search(word.lower(),file_name.lower()):
				
					count +=1

				else:
					pass

			tally[id[0]]=count
			
		matches[file_name]=tally
	print matches

ordered_matches=[]
for k,v in matches.items():
	ordered_matches=sorted(v.items(),key=operator.itemgetter(1),reverse=True)	
	#print ordered_matches
	transfer_files(k,ordered_matches)

		


