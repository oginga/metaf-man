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

def update_DB_meta(**kwargs):
	db=MySQLdb.connect('localhost','root','526419','mfm')
	cursor=db.cursor()
	print str(kwargs['metadata'])

	#sql="UPDATE meta SET metadata ='%s' WHERE path='%s'"%(str(kwargs['metadata']),str(kwargs['path']))
	sql='''UPDATE meta SET metadata ="%s" WHERE path="%s" '''%(str(kwargs['metadata']),str(kwargs['path']))
	try:
		cursor.execute(sql)
		db.commit()
		print 'database METADATA updated'

	except:
		db.rollback
		print "UNABLE TO UPDATE METADATA"
	db.close()



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
		init_data={'path':str(os.path.abspath(os.getcwd())),'metadata':[]}
		
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
					store_into_DB(path=meta_data['path'],metadata=meta_data['metadata'])
				print "FILE INIT SUCCESSFULL"


		else:
			print "Metafile creation unsuccessfull"
			#If init successfull,register path to that directory in the DBs lookup paths
			#Store a copy of the current dirs meta_info int the DB
			#Update the database and manipulate the json with the new oibje
			
	else:
		print 'DIR exists.Changing to that directory'
		#check if dir already initialised
		os.chdir(dir_name)
		print os.getcwd()
		if os.path.isfile(meta_file_name):
			print 'Dir already initialised'
		else:
			if createMetaFile():
				print "successfully created .meta file"
				with open(meta_file_name) as _meta:
					meta_data=json.loads(_meta.read())
					store_into_DB(path=meta_data['path'],metadata=meta_data['metadata'])
				print "FILE INIT SUCCESSFULL"



def edit_metadata():
	print os.getcwd()

	#get .meta,open as json dictionary 
	meta_data={}
	with open('init.json','r') as _meta:
		meta_data=json.loads(_meta.read())
		meta_string=raw_input("Enter individual metadata separated by commas:: ")
		meta_list=meta_string.split(',')
		for word in meta_list:
			meta_data['metadata'].append(word)

			#insert new data
	with open('init.json','w') as upd_meta:
		json.dump(meta_data,upd_meta,indent=0)
		
		#update db
		update_DB_meta(path=meta_data['path'],metadata=meta_data['metadata'])


if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument(dest='folder_name',help='Provide folder name',type=str,metavar='fname',nargs=1)
	args=parser.parse_args()

	print type(args.folder_name[0])
	print args.folder_name[0]

	initDir(args.folder_name[0])
	edit_metadata()

#init successful,manipulate the list in the DB metadata field by manipulating the .meta file first
#create daemon for searching a dummy folder with real files
