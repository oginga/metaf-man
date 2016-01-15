#!/usr/bin/env python

import argparse
import os
import json	
import MySQLdb

current_dir=os.getcwd()
meta_file_name='init.json'

'''

def Creae_DB_If_None_exist():
	try:
		pass
	except Exception, e:
		raise e
'''


def store_into_DB(**kwargs):

	db=MySQLdb.connect('localhost','root','526419','mfm')
	cursor=db.cursor()
	sql="INSERT INTO meta(path,metadata) VALUES ('%s','%s')"%(str(kwargs['path']),str(kwargs['metadata']))
	
	
	try:
		cursor.execute(sql)
		db.commit()
		print 'database updated'

	except:
		db.rollback
		print "UNABLE"
	db.close()

def createMetaFile():   
	with open(os.path.join(os.getcwd(),meta_file_name),'w') as metafile:
		#file_path=
		init_data={'path':str(os.path.abspath(os.path.join(os.getcwd(),meta_file_name)),),'metadata':[]}
		
		json.dump(init_data,metafile,indent=0)
		return True
def initDir(dir_name):
	if not os.path.isdir(dir_name):
		print "Creating directory..."
		try:
			os.mkdir(dir_name)
			print 'DIR creation successful'
		except:print 'ERROR OCCURED'
			#chdir to the created directory
		os.chdir(dir_name)
			#Create an init file--specifies the meta-info for that directory
		if createMetaFile():
				print "successfully created .meta file"
				with open(meta_file_name) as _meta:
					meta_data=json.loads(_meta.read())
					print type(meta_data)
					print meta_data 
				#try:
					store_into_DB(path=meta_data['path'],metadata=meta_data['metadata'])
				#except:
				#	print "Error occured in the storage of path and meta-data"


		else:
			print "Metafile creation unsuccessfull"
			#If init successfull,register path to that directory in the DBs lookup paths
			#Store a copy of the current dirs meta_info int the DB
			#Update the database and manipulate the json with the new oibje
			
	else:
		print 'DIR exists.Changing to that directory'
		os.chdir(dir_name)
		print os.getcwd()
		if os.path.isfile(meta_file_name):
			print True


	

if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument(dest='folder_name',help='Provide folder name',type=str,metavar='fname',nargs=1)
	args=parser.parse_args()

	print type(args.folder_name[0])
	print args.folder_name[0]

	initDir(args.folder_name[0])
