import json
from elasticsearch import Elasticsearch
import config

class UrlBatch(object):
  es = Elasticsearch(config.ES_HOSTS,verify_certs=config.ES_VERIFY_CERTS)

  def __init__(self):
    self.batch_name = None
    self.total_urls = 0
    self.successes = 0
    self.failures = 0
    self.urls = []


  @staticmethod
  def query_all(token):
    body = {
      "aggs": {
        "batches": {
          "terms": {
            "field": "body.batch_name.raw",
            "size" : 1000
          },
          "aggs": {
            "working_url": {
              "terms": {
                "field": "working_url"
              }
            }
          }
        }
      },
      "query": {
        "match": {
          "body.token_id": "%s"%token
        }
      }
    }
    results = UrlBatch.es.transport.perform_request(
      method='POST',
      url='/'+config.ES_INDEX+'/_search?search_type=count',
      body=json.dumps(body)
    )
    retVal = { 'total': 0, 'data' : [] }
    if results[0] == 200:
      buckets = results[1]['aggregations']['batches']['buckets']
      retVal['total'] = len(buckets)
      for b in buckets:
        to_append = {
          "batch_name" : b['key'],
          "total_urls" : b['doc_count'],
          'success_cnt' : 0,
          'fail_cnt' : 0
        }
        for url_bucket in b['working_url']['buckets']:
          if url_bucket['key'] == 'T':
            to_append['success_cnt'] = url_bucket['doc_count']
          else:
            to_append['fail_cnt'] = url_bucket['doc_count']
        retVal['data'].append(to_append)
    retVal['data'] = sorted(retVal['data'], key=lambda b: b['batch_name'], reverse=True)
    return retVal

  @staticmethod
  def get_batch_details(token_id,batch_name):
    body = {
      "query": {
        "bool": {
          "must": [{
            "match": {
              "body.token_id": "%s"%token_id
            }
          },
          {
            "match": {
              "body.batch_name.raw": "%s"%batch_name
            }
          },
          {
            "match": {
              "working_url": False
            }
          }]
        }
      },
      "size":100
    }
    results = UrlBatch.es.transport.perform_request(
      method='POST',
      url='/'+config.ES_INDEX+'/_search',
      body=json.dumps(body)
    )
    retVal = { 'total': 0, 'data' : [] }
    if results[0] == 200 and results[1]['hits']['total'] > 0 :
      retVal['total'] = results[1]['hits']['total']
      hits = results[1]['hits']['hits']
      for hit in hits:
        retVal['data'].append({
          "id" : hit['_id'],
          "url" : hit['_source']['checked_url'],
          "status_code" : hit['_source']['status_code'],
          "resp_body" : hit['_source']['resp_body'],
          "last_checked_time" : hit['_source']['last_checked_time']
        })
    return retVal
