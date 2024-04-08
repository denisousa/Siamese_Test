"""
Indexing
r1, r2, and r3 starting from 4 to 24 (step of 4) - Siamese Research
r1, r2, and r3 starting from 4 to 24 (step of 1 or 2) - Denis Research

Search
The query reduction thresholds should be somewhere around 1-15%

"""
import datetime
import os
import gc
import subprocess
from elasticsearch_operations import (
    new_execute_cluster_elasticserach,
    stop_cluster_elasticserach,
    create_one_cluster_elasticserach
)
from dotenv import load_dotenv

load_dotenv()


def execute_siamese_index_properties(ngram):
    gc.collect()
    os.system("sync")

    project_index_path = os.getenv("PROJECT_TO_INDEX")
    elasticsearch_path = os.getenv("ELASTICSEARCH_CLUSTERS")
    n_gram_properties_path = "./n-gram-properties"

    index_name = os.getenv("INDEX_NAME")
    index_name = f"{index_name}_n_gram_{ngram}"

    config = open("config-index.properties", "r").read()
    config = config.replace(
        "elasticsearchLoc=", f"elasticsearchLoc=./ngram_all"
    )
    config = config.replace("cluster=", f"cluster=stackoverflow")
    config = config.replace("index=", f"index={index_name}")
    config = config.replace("t1NgramSize=", f"t1NgramSize={ngram}")
    config = config.replace("t2NgramSize=", f"t2NgramSize={ngram}")
    config = config.replace("ngramSize=", f"ngramSize={ngram}")
    config = config.replace("inputFolder=", f"inputFolder={project_index_path}")
    print(f"CONFIG NAME: {index_name} \n\n")
    new_config = f"{n_gram_properties_path}/n_gram_{ngram}.properties"
    open(new_config, "w").write(config)
    command = f"java -jar siamese-0.0.6-SNAPSHOT.jar -cf {new_config}"
    process = subprocess.Popen(
        command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True
    )
    process.wait()


initial_quantity = int(os.getenv("INITIAL_CLUSTER_QUANTITY"))
final_quantity = int(os.getenv("FINAL_CLUSTER_QUANTITY")) + 1
clusters_range = range(initial_quantity, final_quantity)

start_time = datetime.datetime.now()

new_execute_cluster_elasticserach()

for i in range(4,9,2):
    execute_siamese_index_properties(i)

end_time = datetime.datetime.now()
exec_time = end_time - start_time
print("Execution time:", exec_time)