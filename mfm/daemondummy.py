#!/usr/bin/env python  

import os
import json
import re
import MySQLdb
import ast
import operator
import shutil
import daemon
import time
import logging 
from daemon import runner
#handle same number of matches
#test cases
#create daemon
#import nose
#choose a root folder ie downloads
root_dir=os.path.join(os.path.abspath(os.sep),'/root/Development/REPOS/metaf-man/mfm/downloads')
db_results=None
	    


def transfer_files(key,matches_list):
#'''Copies the files to their new location key:string matches_list:list'''
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



class App():
   
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/testdaemon/testdaemon.pid'
        self.pidfile_timeout = 5
           
    def run(self):
	    #Main code goes here ...

	    #check available files on the folder  with extensions--> .doc, .pdf, .xcl, .ppt

	    files= os.listdir(root_dir)
	    doc_pat=re.compile(".pdf|.txt|.docx|.pptx$")
	    print "FILES: ",files,"\n\n\n"
	    while True :		
		

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

		#create wait time for the program
				time.sleep(10)

			logger.debug("Debug message")
			logger.info("Info message")
			logger.warn("Warning message")
			logger.error("Error message")
			time.sleep(10)

            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
        	
        	
        	
        	
        	

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/testdaemon/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()



	





		


