# Include the Dropbox SDK
import dropbox, sys, os, json, operator
from dropbox import rest


from datetime import datetime

def end_wrong_syntax():
  print "wrong argv python restore.py config_file_path backup_file_name dest_folder"
  sys.exit()  

try:
  if __name__ != '__main__':
    print "not allow"
    sys.exit()


  current_file = os.path.realpath(__file__)
  current_path = os.path.dirname(current_file)
  
  os.chdir(current_path)

  print sys.argv
  if len(sys.argv) != 4:
    end_wrong_syntax()

  config_file_path = sys.argv[1]
  backup_file_name = sys.argv[2]
  dest_folder = sys.argv[3]


  if  os.path.isdir(dest_folder) is False:
    print "Destination folder doesn't found , please check again: "+ dest_folder
    sys.exit()

  if  os.path.isfile(config_file_path) is False:
    print "not found config file: " + config_file_path
    sys.exit()

  config_file = open(config_file_path, 'r')

  config = json.loads(config_file.read())
  
  # Get your app key and secret from the Dropbox developer website

  backup_folder       = config['backup_folder']

  access_token        = config['access_token']

  max_file_in_folder  = config['max_file_in_folder']

  restore_path = os.path.join( backup_folder, backup_file_name )
  print "restore path is " + restore_path

  restore_path_computer = os.path.join( dest_folder, backup_file_name )

  print "This process will retore file {0}  from dropbox to  {1} on your computer".format( restore_path, restore_path_computer  )
  
  client = dropbox.client.DropboxClient(access_token)
  print 'linked account: ', client.account_info()


  f, metadata = client.get_file_and_metadata( restore_path )
  # print f
  # print metadata
  print "Restoring, please wait"
  out = open( restore_path_computer , 'wb')
  out.write(f.read())
  out.close()
  print metadata

except Exception, e:
  print "error"
  print e
finally:
  pass
