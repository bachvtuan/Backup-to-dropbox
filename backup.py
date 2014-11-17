# Include the Dropbox SDK
import dropbox, sys, os, json, operator
from dropbox import rest


from datetime import datetime

def end_wrong_syntax():
  print "wrong argv python backup.py config_file_path upload_file_path"
  sys.exit()  

try:
  if __name__ != '__main__':
    print "not allow"
    sys.exit()


  current_file = os.path.realpath(__file__)
  current_path = os.path.dirname(current_file)
  
  os.chdir(current_path)

  print sys.argv
  if len(sys.argv) != 3:
    end_wrong_syntax()

  config_file_path = sys.argv[1]
  upload_file_path = sys.argv[2]


  if  os.path.isfile(config_file_path) is False:
    print "not found config file: "+config_file_path
    sys.exit()

  if  os.path.isfile(upload_file_path) is False:
    print "not found upload file: " + upload_file_path
    sys.exit()

  config_file = open(config_file_path, 'r')

  config = json.loads(config_file.read())
  file_name_backup = os.path.basename(upload_file_path)
  print "File name to backup is " + file_name_backup


  # Get your app key and secret from the Dropbox developer website

  backup_folder       = config['backup_folder']

  access_token        = config['access_token']

  max_file_in_folder  = config['max_file_in_folder']

  dest_backup_path = os.path.join( backup_folder, file_name_backup )
  print "This process will backup file {0} to  {1} on your dropbox account".format( upload_file_path, dest_backup_path  )
  

  client = dropbox.client.DropboxClient(access_token)
  print 'linked account: ', client.account_info()

  
  file_instance = open( upload_file_path , 'rb')

  print file_instance

  file_size =  os.path.getsize( upload_file_path )
  print "file_size is " + str(file_size) 

  uploader = client.get_chunked_uploader(file_instance, file_size)
  
  while uploader.offset < file_size:
    try:
      upload = uploader.upload_chunked()
      print uploader.offset
    except rest.ErrorResponse, e:
      # perform error handling and retry logic
      print "happended error while  backup for file"
      print e
      sys.exit()

  uploader.finish( dest_backup_path )
  print "your file is backuped to dropbox successfully"


  #Get all files on this backup folder
  folder_metadata = client.metadata( backup_folder  )
  
  file_list = []

  #maybe we should sort by modified date for sure and don't action to folder item
  for _file in folder_metadata['contents']:
    #not a folder
    if _file['icon'] != 'folder':
      item = {
        'date':datetime.strptime( _file['modified'][:-6],'%a, %d %b %Y %H:%M:%S'),
        'path': _file['path']
      }

      file_list.append( item )

  print "file_list"
  print file_list
  sorted(file_list, key=operator.itemgetter('date'), reverse=True)

  print file_list

  #remove old backup files
  if len( file_list ) > max_file_in_folder:
    delete_number = len(file_list)  - max_file_in_folder

    for i in range(delete_number):
      _file = file_list[i]
      print "removing " +  _file['path']
      client.file_delete(_file['path'])

    print "Removed all old files"

  # f, metadata = client.get_file_and_metadata('/Backup/backup2.jpg')
  # out = open('hey.jpg', 'wb')
  # out.write(f.read())
  # out.close()
  # print metadata

except Exception, e:
  print "error"
  print e
finally:
  pass
