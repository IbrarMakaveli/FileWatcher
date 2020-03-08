import os, yaml, shutil

print("[INFO] Install config with root path")
root_path_project = os.path.dirname(os.path.abspath(__file__))
yaml_file = os.path.join(root_path_project, "config.yaml")

list_doc = dict

with open(yaml_file) as f:
    list_doc = yaml.safe_load(f)

root_path_project = root_path_project.rsplit(os.path.sep, 1)[0] #retire le config de la fin
list_doc['appPath'] = root_path_project
list_doc['logs']['path'] = os.path.join(root_path_project, "logs")
list_doc['data']['path'] = os.path.join(root_path_project, "data")
list_doc['pid']['path'] = os.path.join(root_path_project, "pid")

if os.path.exists(list_doc['logs']['path'])==False:
    print("[INFO] Create logs folder")
    os.mkdir(list_doc['logs']['path'])

if os.path.exists(list_doc['data']['path'])==False:
    print("[INFO] Create data folder")
    os.mkdir(list_doc['data']['path'])

if os.path.exists(list_doc['pid']['path'])==False:
    print("[INFO] Create pid folder")
    os.mkdir(list_doc['pid']['path'])

with open(yaml_file, "w") as f:
    yaml.safe_dump(list_doc, f)