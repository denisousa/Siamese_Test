import os 
import pandas as pd
import shutil

def most_recent_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, file) for file in files]
    most_recent = max(paths, key=os.path.getctime)
    most_recent_name = os.path.basename(most_recent)
    return most_recent_name, open(f'{directory}/{most_recent_name}', 'r').read()

def delete_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file}")
            else:
                print(f"Skipped: {file} is not a file")
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

def get_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    file_times = [(os.path.join(folder_path, file), os.path.getctime(os.path.join(folder_path, file))) for file in files]
    sorted_files = sorted(file_times, key=lambda x: x[1])
    return [file_path.split('/')[-1] for file_path, _ in sorted_files]

def cut_so_project():
    df_clones = pd.read_csv('clones_only_QS_EX_UD.csv')

    so_path = '/home/denis/programming/siamese-optmization/Siamese/my_index/stackoverflow/stackoverflow_formatted'
    new_so_path = '/home/denis/programming/siamese-optmization/Siamese/my_index/cut_stackoverflow_filtered'

    if os.path.isdir(new_so_path):
        shutil.rmtree(new_so_path)
    
    os.makedirs(new_so_path)

    result = []

    for index, row in df_clones.iterrows():
        result.append(row.to_dict())

        new_start1 = row['start1'] - 1
        code_text = open(f'{so_path}/{row["file1"]}', 'r').read().split('\n')
        cut_code_text = '\n'.join(code_text[new_start1 :row['end1']])

        new_filename = f'{row["file1"].replace(".java", "")}_{row["start1"]}_{row["end1"]}.java'
        open(f'{new_so_path}/{new_filename}', 'w').write(cut_code_text)

        result[index]['file1'] = new_filename
        result[index]['start1'] = 1
        result[index]['end1'] = (row['end1']+1) - row['start1'] 

    new_oracle = pd.DataFrame(result)
    new_oracle.to_csv('NEW_clones_only_QS_EX_UD.csv', index=False)
    return new_oracle
    