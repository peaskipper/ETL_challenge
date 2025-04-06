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
from uml_writer import puml_script, tbl_name_reformat

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

script = puml_script(classification)
for tbl,data in tbl_parsed_dict.items():
    typ = tbl.split('.',maxsplit=1)[0]
    tbl_name = tbl_name_reformat(tbl)
    entity = script.add_entity(tbl_name,data['columns'],typ)

entity = script.add_relationship(relation_fct_dict)
puml_file_path = 'ETL_challenge\\output_obj\\ER_diagram.puml'
save = script.end_script(puml_file_path)

######## debug
# x = relation_dim_dict
print(True)
