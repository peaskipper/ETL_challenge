######## imports

### open lib
import os
import pandas as pd
import gzip
import graphviz
import re
# import pythonplantuml

### self defined lib
if __name__ == "__main__":
    from ingest import ingest_src
    from analyse import parse_dataset
    from uml_writer import puml_script, tbl_name_reformat
else:
    from .ingest import ingest_src
    from .analyse import parse_dataset
    from .uml_writer import puml_script, tbl_name_reformat

######## Class, method Fn definitions


######## Source specific configs

src_location = '..\\source_data\\data\\'
extension = '.gz'
compression = 'gzip'
separator = '|'
classification  = ['hier.', 'fact.']


######## Main

##### Ingest from source into dict

# Specify configs
ingested_data = ingest_src(
                        src_location = src_location,\
                        extension = extension,\
                        compression = compression,\
                        separator = separator,\
                        classification  = ''
                    )
# Begin ingestion
dataframe_dict = ingested_data.ingest()


##### Parse datasets

# Parse tbl metadata
parsed_dataset = parse_dataset(dataframe_dict)
tbl_parsed_dict = parsed_dataset.tbl_parsed_dict

# Parse inter-tbl relationships
fct_list = [tbl for tbl in tbl_parsed_dict.keys() if tbl.startswith('fact.')]
relation_fct_dict = parsed_dataset.find_relation(fct_list)
dim_list = [tbl for tbl in tbl_parsed_dict.keys() if tbl.startswith('hier.')]
relation_dim_dict = parsed_dataset.find_relation(dim_list, one2many=False)


##### Write puml script

if __name__ == "__main__":
    # Initiate script
    script = puml_script(classification)  

    # Add entity
    for tbl,data in tbl_parsed_dict.items():
        typ = tbl.split('.',maxsplit=1)[0]
        tbl_name = tbl_name_reformat(tbl)
        col_type = zip(data['columns'],data['data_type'])
        entity = script.add_entity(tbl_name,col_type,typ)

    # Add relationships
    entity = script.add_relationship(relation_fct_dict)
    puml_file_path = 'ETL_challenge\\output_obj\\ER_diagram.puml'
    save = script.end_script(puml_file_path)

######## debug
# x = relation_dim_dict
# print(True)
# raise ValueError("debugging")