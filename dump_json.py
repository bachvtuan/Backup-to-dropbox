"""
this's an extra part, not relative to backup and restore 
Dump all files in a public folder to json format .
USING:
python dump_json.py config_file public_folder
EXAMPLE:
python dump_json.py configs/dethoima.com Public/BritishCouncil
"""


import dropbox, sys, os, json, operator
from dropbox import rest
import re

from datetime import datetime

def end_wrong_syntax():
  #Public/BritishCouncil
  print "wrong argv python restore.py config_file_path public_path"
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
  public_path = sys.argv[2]

  print "Public path is " + public_path

  if  os.path.isfile(config_file_path) is False:
    print "not found config file: " + config_file_path
    sys.exit()

  config_file = open(config_file_path, 'r')

  config = json.loads(config_file.read())
  
  # Get your app key and secret from the Dropbox developer website

  backup_folder       = config['backup_folder']
  access_token        = config['access_token']
  max_file_in_folder  = config['max_file_in_folder']
  
  client = dropbox.client.DropboxClient(access_token)
  account_info =  client.account_info()

  user_id = account_info['uid']

  print "user id is " + str(user_id)

  folder_metadata = client.metadata( public_path )

  return_arr = []

  for file_item in folder_metadata['contents']:

    path = file_item['path']

    if path[-3:] == "pdf":
      continue

    path = path.replace("/Public/","")
    arr_temp = path.split("/")

    file_name = arr_temp[ len( arr_temp ) -1 ]

    #replace - and _ to space  and uppercase on each letter
    file_name = re.sub("[\-\_]", ' ', file_name).title()

    dot_position = file_name.find(".")

    if dot_position != -1:
      file_name = file_name[:dot_position]

    audio_link = 'https://dl.dropboxusercontent.com/u/%s/%s' % ( user_id, path )
    pdf_dropbox_link = audio_link.replace(".mp3",'.pdf')
    pdf_link = "<a href='%s' target='_blank' >here</a>" %( pdf_dropbox_link  )

    emotion = "You can click %s to show to the transcript" % ( pdf_link )

    return_arr.append({
      'title'  : file_name,
      'link'   : audio_link,
      'emotion': emotion
    })
  print "Please copy below json string"
  print json.dumps( return_arr )

  #https://dl.dropboxusercontent.com/u/15633987/BritishCouncil/ylteachers.mp3

except Exception, e:
  print "error"
  print e
finally:
  pass
