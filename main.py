import csv
from os.path import abspath, join, dirname, exists
import tqdm
import urllib3
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk




def create_index_it_awareness(client):
    '''Creates an index in Elasticsearch if onse isn't already there.'''
    client.indices.create(
        index = 'Awareness',
        body = {
            "settings" :{"number_of_shards":1,
                        "index.mapping.ignore_malformed": 'true'},
            "mappings" : {
                "properties" : { 
                    "index": {"type":"integer"},
                    "Content ID" : {"type": "integer"},
                    "User ID": {"type" :"integer","fields":{"keyword":{"type":"keyword"}}},
                    "Email":{"type": "text"},
                    "Last login":{"type":"date"},
                    "Last activity":{"type":"date","ignore_malformed": 'true'},
                    "Registration date": {"type":"date","ignore_malformed": 'true'},
                    "EmployeeGuid": {"type":"text"},
                    "SAPCentralPersonNumber":{"type":"integer"},
                    "HierarchyDescription" : {"type" : "text","fields":{"keyword":{"type":"keyword"}}},
                    "CountryISOCode" : {"type":"text","fields":{"keyword":{"type":"keyword"}}},
                    "CostCenterNumber":{"type":"integer"},
                    "LanguageKey": { "type": "text"},
                    "CompanyName": { "type": "text","fields":{"keyword":{"type":"keyword"}}},
                    "Created":{"type": "date","ignore_malformed": 'true'},
                    "NewHire":{"type":"text","fields":{"keyword":{"type":"keyword"}}},
                    "Company":{"type":"text"},
                    "Department":{"type":"text","fields":{"keyword":{"type":"keyword"}}},
                    "Position":{"type":"text","fields":{"keyword":{"type":"keyword"}}},
                    "Country":{"type":"text"},
                    "Date course started": {"type":"date", "ignore_malformed": 'true'},
                    "SCORM course status":{"type":"text"},
                    "Test score":{"type":"integer"},
                    "Session time": {"type": 'text',"fields":{"keyword":{"type":"keyword"}}},
                    "Date course completed": {"type":"date", "ignore_malformed": 'true'},     
                    
                }
            },
        },
        ignore=400,
    )

def create_index_phising(client):
    ''' Creates an index on Elastic search for the phising programm'''
    client.indices.create(
        index = 'Phising',
        body = {
            'settings': {"number_of_shards":1,
                        "index.mapping.ignore_malformed": 'true'},
            'mappings' : {
                'properties': {
                    'index': {'type':'integer'},
                    'Subject' : {'type': 'text','fields' : {"keyword":{'type':'keyword'}}},
                    'Received': {'type':'date', 'ignore_malformed': 'true'},
                    'Sender':{'type':'text','fields':{'keyword':{'type':'keyword'}}},
                    'Filename':{'type':'text','fileds':{'keyword':{'type':'keyword'}}}	,

                }

            }
        },
        ignore=400,
    )


def generate_action_phising():
    with open('dataPhising.csv') as g:
        reader = csv.DictReader(g)
        for row in reader:
            doc = {
                
                'Subject' : row['Subject'] ,
                'Received' : row['Received'],
                'Sender': row['Sender'],
                'Filename' :row['Filename']

            }
            yield doc
        

def generate_action_awareness():
    with open('hilti.csv',mode='r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            doc = {
            "Content ID": row["Content ID"],
            "User ID" : row["User ID"],
            "Email" :row["Email"],
            "Last login" : row["Last login"],
            "Last activity":row["Last activity"],
            "Registration date": row["Registration date"],
            "EmployeeGuid" : row["EmployeeGuid"],
            "SAPCentralPersonNumber": row["SAPCentralPersonNumber"],
            "HierarchyDescription" : row["HierarchyDescription"],
            "CountryISOCode": row["CountryISOCode"],
            "CostCenterNumber": row["CostCenterNumber"],
            "LanguageKey": row["LanguageKey"],
            "CompanyName": row["CompanyName"],
            "Created" : row["Created"],
            "NewHire": row["NewHire"],
            "Company": row["Company"],
            "Department": row["Department"],
            "Position": row["Position"],
            "Country": row["Country"],
            "Date course started":row["Date course started"],
            "SCORM course status": row["SCORM course status"],
            "Test score": row["Test score"],
            "Session time": row["Session time"],
            "Date course completed":row["Date course completed"]          
            }
            yield doc



def upload_awareness():
    print("Loading awareness dataset")
    number_of_rows = 32313

    client = Elasticsearch(
        http_auth = ('elastic','changeme')      
    )
    print('Creating an index')
    create_index_it_awareness(client)
    print("Indexing documents")
    progress = tqdm.tqdm(unit='docs',total=number_of_rows)
    successes = 0 
    for ok , action in streaming_bulk(
        client=client,index='Awareness',actions=generate_action_awareness(),
    ):
        progress.update(1)
        successes+=ok
    print("Indexed %d/%d documents" % (successes, number_of_rows))


def upload_phising():
    print("Loading phising dataset")
    number_of_rows = 1050
    client = Elasticsearch(
        http_auth = ('elastic','changeme')      
    )
    print('Creating an index')
    create_index_it_awareness(client)
    print("Indexing documents")
    progress = tqdm.tqdm(unit='docs',total=number_of_rows)
    successes = 0 
    for ok , action in streaming_bulk(
        client=client,index='phising',actions=generate_action_phising(),
    ):
        progress.update(1)
        successes+=ok
    print("Indexed %d/%d documents" % (successes, number_of_rows))


if __name__ == "__main__":
    #upload_awareness()
    upload_phising()