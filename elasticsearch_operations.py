import re
import os
import subprocess
from time import sleep
from dotenv import load_dotenv
load_dotenv()
import requests

def put_template(ngram):
    port = 9000 + ngram
    elasticsearch_url = f"http://http://localhost:{port}"

    index_name = os.getenv('INDEX_NAME')
    index_name = f'{index_name}_n_gram_{ngram}'

    create_index_endpoint = f"{elasticsearch_url}/{index_name}"

    response = requests.put(create_index_endpoint)

    if response.status_code == 200:
        print(f"Index '{index_name}' created successfully.")
    elif response.status_code == 400:
        print(f"Index creation failed. Index '{index_name}' may already exist.")
    else:
        print(f"Failed to create index '{index_name}'. Status code: {response.status_code}, Response: {response.text}")


def get_ngram_by_port():
    ngram_by_port = {}
    for ngram_i, port in zip(range(4,25), range(9200,9221)):
        ngram_by_port[ngram_i] = port
    return ngram_by_port

def create_one_cluster_elasticserach(ngram):
    port = 9000 + ngram
    elasticsearch_path = os.getenv('ELASTICSEARCH_CLUSTERS')

    if not os.path.exists(elasticsearch_path):
        os.makedirs(elasticsearch_path)

    command_delete = f'trash-put {elasticsearch_path}/elasticsearch-ngram-{ngram}'
    command_unzip = f'tar -xvf elasticsearch-2.2.0.tar.gz -C {elasticsearch_path}'
    command_rename = f'mv {elasticsearch_path}/elasticsearch-2.2.0 {elasticsearch_path}/elasticsearch-ngram-{ngram}'
    elasticsearch_yml_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram}/config/elasticsearch.yml'

    #template_content = open('elasticsearch_template_config.txt', 'r').read()
    
    index_name = os.getenv('INDEX_NAME')
    #template_name = os.getenv('ELASTICSEARCH_TEMPLATE')
    #template_content = template_content.replace('TEMPLATE', template_name).replace('INDEX', index_name)
    # elasticsearch_yml_content = f'cluster.name: stackoverflow \nindex.query.bool.max_clause_count: 8192 \nhttp.port: {port} \nindices.cache.filter.size: 20%\n{template_content}'
    
    #elasticsearch_yml_content = f'cluster.name: stackoverflow \nindex.name: {index_name}-{ngram}\nindex.query.bool.max_clause_count: 8192 \nhttp.port: {port} \nindices.cache.filter.size: 20%'
    elasticsearch_yml_content = f'cluster.name: stackoverflow \nindex.name: {index_name}_n_gram_{ngram}\nhttp.port: {port}'

    os.system(command_delete)
    sleep(1)

    os.system(command_unzip)
    sleep(1)

    os.system(command_rename)
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)
    print(f'\nCREATE ELASTICSEARCH elasticsearch-ngram-{ngram}\n')

def create_clusters_elasticserach():
    elasticsearch_path = '../../siamese-optmization/elasticsearch-siamese'
    clusters = [5,7,9,11,13,15,17,19,21,23]
    for ngram_i in clusters:
        port = 9000 + ngram_i
        shards = 4
        replicas = 1
        shards_per_node = 2
        mem = 2

        command_unzip = f'tar -xvf elasticsearch-2.2.0.tar.gz -C {elasticsearch_path}'
        command_rename = f'mv {elasticsearch_path}/elasticsearch-2.2.0 {elasticsearch_path}/elasticsearch-ngram-{ngram_i}'
        elasticsearch_yml_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/config/elasticsearch.yml'
        elasticsearch_yml_content = f'cluster.name: stackoverflow \nindex.query.bool.max_clause_count: 8192 \nhttp.port: {port}'
        #elasticsearch_yml_content = f'{elasticsearch_yml_content}\nindex.number_of_shards: {shards}\nindex.number_of_replicas: {replicas}'
        #elasticsearch_yml_content = f'{elasticsearch_yml_content}\ncluster.routing.allocation.total_shards_per_node: {shards_per_node}'
        elasticsearch_yml_content = f'{elasticsearch_yml_content}\nindices.cache.filter.size: 20%'
        os.system(command_unzip)
        sleep(1)

        os.system(command_rename)
        open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_content)

        elasticsearch_in_bat_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/bin/elasticsearch.in.bat'
        elasticsearch_in_bat_text = open(elasticsearch_in_bat_path, 'r').read()
        elasticsearch_in_bat_text = elasticsearch_in_bat_text.replace('ES_MIN_MEM=256m', f'ES_MIN_MEM={mem}g')
        elasticsearch_in_bat_text = elasticsearch_in_bat_text.replace('ES_MAX_MEM=1g', f'ES_MAX_MEM={mem}g')

        elasticsearch_in_sh_path = f'{elasticsearch_path}/elasticsearch-ngram-{ngram_i}/bin/elasticsearch.in.sh'
        elasticsearch_in_sh_text = open(elasticsearch_in_sh_path, 'r').read()
        elasticsearch_in_sh_text = elasticsearch_in_sh_text.replace('ES_MIN_MEM=256m', f'ES_MIN_MEM={mem}g')
        elasticsearch_in_sh_text = elasticsearch_in_sh_text.replace('ES_MAX_MEM=1g', f'ES_MAX_MEM={mem}g')


        open(elasticsearch_in_bat_path, 'w').write(elasticsearch_in_bat_text)
        open(elasticsearch_in_sh_path, 'w').write(elasticsearch_in_sh_text)
        print(f'\nCREATE ELASTICSEARCH elasticsearch-ngram-{ngram_i}\n')

def delete_indices_incorrect(ngram):
    port = 9000 + ngram
    index_name = os.getenv('INDEX_NAME')

    for i in range(4,25):
        if i == ngram:
            continue

        complete_index_name = f'{index_name}_n_gram_{i}'
        os.system(f'curl -sS -X DELETE "http://localhost:{port}/{complete_index_name}" > /dev/null 2>&1')

def new_execute_cluster_elasticserach():
    command_execute = f'./ngram_all/bin/elasticsearch -d'
    print(f'EXECUTING elasticsearch-ngram-all')
    process = subprocess.Popen(command_execute, shell=True, stdout=subprocess.PIPE)
    process.wait()
    sleep(7)

def execute_cluster_elasticserach(ngram):
    command_execute = f'ngram_{ngram}/bin/elasticsearch -d'
    print(f'EXECUTING elasticsearch-ngram-{ngram}')
    process = subprocess.Popen(command_execute, shell=True, stdout=subprocess.PIPE)
    process.wait()
    sleep(7)

def stop_cluster_elasticserach(ngram):
    port = 9000 + ngram
    command_stop = f'sudo fuser -k -n tcp {port}'
    print(f'STOP elasticsearch-ngram-{ngram}')
    process = subprocess.Popen(command_stop, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    process.wait()

def change_cluster_name(ngram_size):
    command = f'sudo -S kill $(sudo lsof -t -i :9200)'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=None, stderr=None, close_fds=True)
    process.wait()

    elasticsearch_yml_path = '../../siamese-optmization/elasticsearch-2.2.0/config/elasticsearch.yml'
    pattern = r"cluster\.name:\s*(.*?)\s*\n"
    elasticsearch_yml_text = open(elasticsearch_yml_path, 'r').read()
    cluster_name = re.search(pattern, elasticsearch_yml_text).group(1)
    elasticsearch_yml_text = elasticsearch_yml_text.replace(cluster_name, f'n_gram_{ngram_size}')
    elasticsearch_yml_text = elasticsearch_yml_text
    open(elasticsearch_yml_path, 'w').write(elasticsearch_yml_text)


    command = f'../../siamese-optmization/elasticsearch-2.2.0/bin/elasticsearch'
    process = subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    process.wait()
