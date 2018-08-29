import datetime
from elasticsearch import Elasticsearch as ES

# Elastic-search read configuration
es_read_node = "test.com"
es_read_port = "9200"
es_read_index = "myindex"
es_read_type = "mytype"

es_read_server = ES("http://"+es_read_node+":"+es_read_port)

startdate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
enddate = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
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

response = es_read_server.search(index=es_read_index, doc_type=es_read_type, body=es_query, size=1)
docs_created_today=response['hits']['total']
print('Found %s created records in %s/%s for today' %(docs_created_today, es_read_index, es_read_type))



