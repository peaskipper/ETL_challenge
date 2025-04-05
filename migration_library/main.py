######## imports

import os
import pandas as pd
import gzip
import re
from ingest import ingest_src


######## Class and method definitions

######## Fn definitions

######## Configs

src_location = 'ETL_challenge\\source_data\\data\\'
extension = '.gz'
compression = 'gzip'
separator = '|'
classification  = ['hier.', 'fact.']


######## Main

##### Ingest from source into dict

create_dataframes = ingest_src(
                        src_location = 'ETL_challenge\\source_data\\data\\',\
                        extension = '.gz',\
                        compression = 'gzip',\
                        separator = '|',\
                        classification  = ['hier.', 'fact.']
                    ).ingest()

# debug
print(create_dataframes.keys())