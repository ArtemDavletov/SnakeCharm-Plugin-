import csv

# pip install GitPython
import git
import yaml

git.Git(".").clone("git@github.com:snakemake/snakemake-wrappers.git")

import os
import shutil

DIRS = []

# Add header to csv file
with open('./result.csv', 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['name', 'description', 'authors', 'input_args', 'input_named_args',
                                                  'output_args', 'output_named_args', 'param_args', 'param_named_args'])
    writer.writeheader()


# Переписал проверку по типу
def quantity_of_named_args(args):
    quantity = 0
    for arg in args:
        if type(arg) is dict:
            quantity += 1
    return quantity


def give_authors(authors_list):
    return ' '.join(authors_list)


def converter(yaml_file_path, csv_file_path):
    fnames = ['name', 'description', 'authors', 'input_args', 'input_named_args',
              'output_args', 'output_named_args', 'param_args', 'param_named_args']
    input_names = ['name', 'description', 'authors', 'input', 'output', 'param']
    with open(yaml_file_path) as yaml_file:
        yaml_dict = yaml.safe_load(yaml_file)
        for input_name in input_names:
            if input_name not in yaml_dict:
                yaml_dict[input_name] = ''
        with open(csv_file_path, 'a') as csv_file:
            # yaml.safe_load и в правду парсит словари
            # print(yaml_dict)
            # print(yaml_dict['input'])
            # print(type(yaml_dict['input'][1]) is dict)
            writer = csv.DictWriter(csv_file, fieldnames=fnames)
            writer.writerow({'name': yaml_dict['name'],
                             'description': yaml_dict['description'],
                             'authors': give_authors(yaml_dict['authors']),
                             'input_args': len(yaml_dict['input']),
                             'input_named_args': quantity_of_named_args(yaml_dict['input']),
                             'output_args': len(yaml_dict['output']),
                             'output_named_args': quantity_of_named_args(yaml_dict['output']),
                             'param_args': len(yaml_dict['param']),
                             'param_named_args': quantity_of_named_args(yaml_dict['param'])})


def walking(d):
    for current_dir, dirs, files in os.walk(d):
        for file in files:
            if file == 'meta.yaml':
                DIRS.append(current_dir)
                converter(current_dir + '/' + file, './result.csv')
                break
        if dirs:
            for dir in dirs:
                walking(dir)


walking('./snakemake-wrappers')

# Quantity of wrappers
print(len(DIRS))

shutil.rmtree('./snakemake-wrappers')