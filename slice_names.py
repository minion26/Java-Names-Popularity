import os

with open('java_files_from_repo2.txt', 'r', encoding='utf-8') as f:
    java_files = f.readlines()

with open('sliced_names_from_repo2.txt', 'w', encoding='utf-8') as file:
    for java_file in java_files:
        java_file = java_file.strip()
        name = os.path.basename(java_file)
        name = name.split('/')[-1]
        name = name.split('.')[0]
        file.write(f"{name}\n")