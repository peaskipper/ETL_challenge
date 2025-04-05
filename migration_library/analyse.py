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
            tbl_parsed_dict[tbl] = {
                'filename':tbl,
                'df':df,
                'columns':columns,
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

    def find_relation(self, tbl_list, one2many=True):
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
        # if key in columns:
        #     columns.remove(key)
        #     return [key].extend(columns)
        return columns