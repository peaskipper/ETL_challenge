######## imports

### open lib
import os
import pandas as pd
import gzip
import graphviz
import re
# import pythonplantuml

### self defined lib
from ingest import ingest_src
from analyse import parse_dataset


######## Class, method Fn definitions


######## Configs

src_location = 'ETL_challenge\\source_data\\data\\'
extension = '.gz'
compression = 'gzip'
separator = '|'
classification  = ['hier.', 'fact.']


######## Main

##### Ingest from source into dict

ingested_data = ingest_src(
                        src_location = 'ETL_challenge\\source_data\\data\\',\
                        extension = '.gz',\
                        compression = 'gzip',\
                        separator = '|',\
                        classification  = ''
                    )

dataframe_dict = ingested_data.ingest()

##### Parse datasets

parsed_dataset = parse_dataset(dataframe_dict)
tbl_parsed_dict = parsed_dataset.tbl_parsed_dict

fct_list = [tbl for tbl in tbl_parsed_dict.keys() if tbl.startswith('fact.')]
relation_fct_dict = parsed_dataset.find_relation(fct_list)
dim_list = [tbl for tbl in tbl_parsed_dict.keys() if tbl.startswith('hier.')]
relation_dim_dict = parsed_dataset.find_relation(dim_list, one2many=False)

##### Write puml script


######## debug
# x = relation_fct_dict
# print(x)
