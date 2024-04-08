from elasticsearch_operations import execute_cluster_elasticserach, new_execute_cluster_elasticserach, stop_cluster_elasticserach, delete_indices_incorrect
from siamese_search import execute_siamese_search
from datetime import datetime
from itertools import product
import os

def format_dimension(parms):
    return {'ngramSize' : parms[0],
            'minCloneSize' : parms[1],
            'QRPercentileNorm' : parms[2],
            'QRPercentileT2' : parms[3],
            'QRPercentileT1' : parms[4],
            'QRPercentileOrig' : parms[5], 
            'normBoost': parms[6],
            't2Boost': parms[7],
            't1Boost': parms[8],
            'origBoost': parms[9],
            'simThreshold': parms[10]}

def evaluate_tool(parms):
    parms = format_dimension(parms)
    parms['algorithm'] = 'grid_search'
    parms['output_folder'] = f'./output_{parms["algorithm"]}/{current_datetime}'
    
    if not os.path.exists(parms['output_folder']):
        os.makedirs(parms['output_folder'])
    
    execute_siamese_search(**parms)

def execute_grid_search(combinations):
    algorithm = 'grid_search'

    start_total_time = datetime.now()
    for i, combination in enumerate(combinations):
        i += 1

        print(f"\n\nCount {i}")
        print(f"Combination {combination}")

        start_time = datetime.now()
        evaluate_tool(combination)
        end_time = datetime.now()
        exec_time = end_time - start_time

        print(f"Runtime: {exec_time}")
        result_time_path = f'time_record/{algorithm}/{current_datetime}.txt'
        open(result_time_path, 'a').write(f'Success execution ')
        open(result_time_path, 'a').write( f'{combination} \nRuntime: {exec_time}\n\n')

    total_execution_time = end_time - start_total_time
    print(f"Total execution time: {total_execution_time}")
    open(result_time_path, 'a').write(f"\nTotal execution time: {total_execution_time}\n")

param = [
    [4, 6, 8], # ngram
    [6, 10], # minCloneSize
    [8, 10], # QRPercentileNorm
    [8, 10], # QRPercentileT2
    [8, 10], # QRPercentileT1
    [8, 10], # QRPercentileOrig
    [-1, 10], # normBoost
    [-1, 10], # t2Boost
    [-1, 10], # t1Boost
    [-1, 10], # origBoost
    ['20%,40%,60%,80%', '30%,50%,70%,90%'], # simThreshold 
]

#for i in range(4,9,2):
#    stop_cluster_elasticserach(i)
#    new_execute_cluster_elasticserach(i)


stop_cluster_elasticserach(200)
#execute_cluster_elasticserach(8)
new_execute_cluster_elasticserach()
combinations = list(product(*param))
print(len(combinations))
current_datetime = datetime.now()

execute_grid_search(combinations)