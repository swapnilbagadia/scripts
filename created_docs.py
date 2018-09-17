import datetime

from elasticsearch import Elasticsearch as ES

import mysql.connector

import requests

import sys


#First Argument is the name of the script, second - indexname, third - doctype, fourth - timeformat
print "Running script: ", sys.argv[0]
print "Arguments given are:", len(sys.argv)


# Elastic-search read configuration
es_read_node = "mynode"
es_read_port = "9200"
es_read_index = sys.argv[1]
es_read_type = sys.argv[2]

time_format = sys.argv[3]

print "Index:'{0}' & Doc_Type:'{1}' & Time_Format:{2}".format(es_read_index,es_read_type,time_format)

mydb = mysql.connector.connect(
  host="my_host",
  user="myuser",
  passwd="mypwd",
  database="mydb"

)
mycursor = mydb.cursor()

es_read_server = ES("http://"+es_read_node+":"+es_read_port)

now = datetime.datetime.now()

if time_format.lower() == 'day':
  startdate = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
  enddate = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
elif time_format.lower() == 'hour':
  hour = now.hour
  startdate = now.replace(hour=hour, minute=0, second=0, microsecond=0).isoformat()
  enddate = now.replace(hour=hour, minute=59, second=59, microsecond=0).isoformat()
else:
  print('Invalid Entry')
  sys.exit()

es_query = {
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "createddate": {
              "from": startdate,
              "to": enddate
            }
          }
        }
      ]
    }
  }
}


if es_read_index == 'my_index1':
  mysql_query = "SELECT COUNT(*) FROM MY_TABLE WHERE CREATED_DATE BETWEEN '{0}' AND '{1}'".format(startdate,enddate)
elif es_read_index == 'my_index2':
  mysql_query = "SELECT COUNT(*) FROM MY_TABLE WHERE CREATED_DATE BETWEEN '{0}' AND '{1}'".format(startdate,enddate)
  print('TODO')
else:
  print('Unknown Index')
  sys.exit()

mycursor.execute(mysql_query)
(rows_created,) = mycursor.fetchone()

response = es_read_server.search(index=es_read_index, doc_type=es_read_type, body=es_query, size=1)
docs_created_today=response['hits']['total']

if rows_created == docs_created_today:
	print('Found %s created records in %s/%s for %s' %(docs_created_today, es_read_index, es_read_type,time_format))
else:
	headers = {'Authorization': '<YOUR_TOKEN>'}
	payload = {'channel':'test','text':'test'}
	r = requests.post("https://slack.com/api/chat.postMessage", data=payload, headers=headers)