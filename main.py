import csv
from os.path import abspath, join, dirname, exists
import tqdm
import urllib3
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk



def create_index(client):
    '''Creates an index in Elasticsearch if onse isn't already there.'''
    client.indices.create(
        index = 'hilti',
        body = {
            "settings" :{"number_of_shards":1,
                        "index.mapping.ignore_malformed": 'true'},
            "mappings" : {
                "properties" : { 
                    "index": {"type":"integer"},
                    "Content ID" : {"type": "integer"},
                    "User ID": {"type" :"integer"},
                    "Email":{"type": "text"},
                    "Last login":{"type":"date"},
                    "Last activity":{"type":"date","ignore_malformed": 'true'},
                    "Registration date": {"type":"date","ignore_malformed": 'true'},
                    "EmployeeGuid": {"type":"text"},
                    "SAPCentralPersonNumber":{"type":"integer"},
                    "HierarchyDescription" : {"type" : "text"},
                    "CountryISOCode" : {"type":"text"},
                    "CostCenterNumber":{"type":"integer"},
                    "LanguageKey": { "type": "text"},
                    "CompanyName": { "type": "text"},
                    "Created":{"type": "date","ignore_malformed": 'true'},
                    "NewHire":{"type":"text"},
                    "Company":{"type":"text"},
                    "Department":{"type":"text"},
                    "Position":{"type":"text"},
                    "Country":{"type":"text"},
                    "Date course started": {"type":"date", "ignore_malformed": 'true'},
                    "SCORM course status":{"type":"text"},
                    "Test score":{"type":"integer"},
                    "Session time": {"type": 'text'},
                    "Date course completed": {"type":"date", "ignore_malformed": 'true'},     
                    
                }
            },
        },
        ignore=400,
    )


def generate_action():

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

def main():
    print("Loading dataset")
    number_of_rows = 32313


    client = Elasticsearch(
        http_auth = ('elastic','changeme')      
    )
    print('Creating an index')
    create_index(client)
    print("Indexing documents")
    progress = tqdm.tqdm(unit='docs',total=number_of_rows)
    successes = 0 
    for ok , action in streaming_bulk(
        client=client,index='hilti',actions=generate_action(),
    ):
        progress.update(1)
        successes+=ok
    print("Indexed %d/%d documents" % (successes, number_of_rows))



if __name__ == "__main__":
    main()