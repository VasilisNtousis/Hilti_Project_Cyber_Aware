# Hilti_Project_Cyber_Aware
Repo for the Cyber Aware Project | University of Liechtenstein

## Installation 

A fast way to install ELK stack is via docker

- sudo apt-get install docker
- sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose # install docker compose
- sudo docker pull sebp/elk    https://elk-docker.readthedocs.io/
- sudo docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -it --name elk sebp/elk {Ports:Service, {9200:Elasticsearch,5601:Kibana, 5044:Logstash"Not used"}{

*Check the elastic search is up* http_auth -> elastic:changeme

- curl -XGET localhost:9200 -u elastic:changeme
- you should receive a response like this:
``` {
  "name" : "128434afe7df",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "Udr478jaSO-Ygb1fJVBlfg",
  "version" : {
    "number" : "7.10.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "51e9d6f22758d0374a0f3f5c6e8f3a7997850f96",
    "build_date" : "2020-11-09T21:30:33.964949Z",
    "build_snapshot" : false,
    "lucene_version" : "8.7.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
} ```






