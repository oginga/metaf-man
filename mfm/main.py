#!/usr/bin/env python

import argparse
import os
import json	
import MySQLdb

current_dir=os.getcwd()
meta_file_name='.meta'

'''

def Creae_DB_If_None_exist():
	try:
		pass
	except Exception, e:
		raise e
'''


def DB_connection(sql):

	con=MySQLdb.connect('localhost','root','526419','Metar')
	cursor=con.cursor()

	try:
		cursor.execute(sql)
	except:
		db.rollback

	db.close()



def createMetaFile():
	with open(os.path.join(os.getcwd(),meta_file_name),'w') as metafile:
		#file_path=
		init_data='''
					{
					'path':%s,
					'metadata':[],
					}

				  '''%(os.path.abspath(os.path.join(os.getcwd(),meta_file_name)),)
		json.dump(init_data,metafile,indent=0)

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
					meta_data=json.load(_meta)
					#create an sql statement using the key-values in meta_data and execute




		else:pass
			#If init successfull,register path to that directory in the DBs lookup paths
			#Store a copy of the current dirs meta_info int the DB
			#
			#
			#
			#
		
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
