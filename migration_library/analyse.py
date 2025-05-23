class parse_dataset():
    """
    Parses and analyzes a dictionary of dataFrames to extract metadata
    Includes primary keys and tbl relationships
    """
    def __init__(self, dataframe_dict):
        """
        Initialize a dictionary of dataFrames and generate metadata

        Arg:
            dataframe_dict (dict): Dictionary of DataFrames keyed by filename or tbl name
        """
        self.dataframe_dict = dataframe_dict
        self.tbl_parsed_dict = self._create_metadata_dict(dataframe_dict)

    def _create_metadata_dict(self,dataframe_dict) -> dict:
        tbl_parsed_dict = {}
        for tbl, df in dataframe_dict.items():
            key = self._get_pk(df)
            columns = self._key_as_first_col(df.columns.tolist(), key)
            data_type = self._infer_column_type(df,columns)
            tbl_parsed_dict[tbl] = {
                'filename':tbl,
                'df':df,
                'columns':columns,
                'data_type':data_type,
                'pk':key
            }
        return tbl_parsed_dict

    def _get_pk(self, df, suffix='', filter=''):
        """
        Infer primary key column in a dataFrame

        Arg:
            df (pd dataFrame): Input dataframe
            suffix (str): Suffix to filter potential ID columns like '_id', '_key' etc.
            filter (str): Optional pandas filter expression to filter clean up df (for edge cases)
        Returns:
            str: Primary key coluumn name
        """
        if filter:
            df = df[eval(filter)]
        
        id_col = [col for col in df.columns if col.endswith(suffix)]

        for col in id_col:
            if df[col].is_unique and not df[col].isnull().any():
                return col

        # Return first column if no suitable column is found
        return df.columns[0]

    def find_relation(self, tbl_list, one2many:bool=True):
        """
        Identify potential relationships between tables based on shared columns

        Arg:
            tbl_list (list): List of tbl names to check for relationships
            one2many (bool): True- looks for one-to-many by shared column names 
                             False- checks if a tbl's primary key appears in others
                             Purpose is to handle dim and fct relationships separately

        Returns:
            dict: Mapping each table to a list of inferred relationships
                  Structure- column_name:related_table
        """
        relationship = {}
        for tbl in tbl_list:
            relationship[tbl] = []
            if one2many:
                # Check each column in current tbl against all columns in other tbl
                for col in self.tbl_parsed_dict[tbl]['columns']:
                    for nxt_tbl, nxt_data in self.tbl_parsed_dict.items():
                        if nxt_tbl not in tbl_list and col in nxt_data['columns']:
                            relationship[tbl].append((col, nxt_tbl))
            else:
                # Check if this tbl's primary key against all columns in other tbl
                key = self.tbl_parsed_dict[tbl]['pk']
                for nxt_tbl, nxt_data in self.tbl_parsed_dict.items():
                    if nxt_tbl != tbl and key in nxt_data['columns']:
                        relationship[tbl].append((key, nxt_tbl))
        return relationship

    def _key_as_first_col(self, columns:list, key:str):
        """Moves the key column to the start of the list
        Arg:
            columns (list): Unordered column list
            key (string): Key column
        Returns:
            list: List of columns with key column as first item
        """
        return_list = []
        if key in columns:
            columns.remove(key)
            return_list.append(key)
            return_list.extend(columns)
            return return_list
        return columns
    
    def _infer_column_type(self, df, columns:list=None, map_type:bool=True):
        """Returns a list of inferred column data type, in the same order as columns list
        Arg:
            df (dataFrame): Input dataFrame
            columns (list): prederived and ordered column list
            map_type (bool): Default mapping for pandas dtype to universal type
        Returns:
            list: List of data type as strings
        """
        # Default mapping
        type_mapping = {
            'object': 'string',
            'int64': 'int',
            'int32': 'int',
            'float64': 'float',
            'float32': 'float',
            'bool': 'bool',
            'datetime64[ns]': 'datetime',
            'timedelta[ns]': 'timedelta',
            'category': 'string'
        }

        columns = df.columns if not columns else columns
        result = []
        for col in columns:
            dtype_str = str(df[col].dtype)
            if map_type:
                dtype_str = type_mapping.get(dtype_str, dtype_str)       #TODO: build fallback to original if not mapped
            else:
                dtype_str = dtype_str
            result.append(dtype_str)
        return result