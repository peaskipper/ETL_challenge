class parse_dataset():

    def __init__(self, dataframe_dict):
        self.dataframe_dict = dataframe_dict
        self.tbl_parsed_dict = self.create_metadata_dict(dataframe_dict)
        pass

    def create_metadata_dict(self,dataframe_dict) -> dict:
        tbl_parsed_dict = {}
        for tbl, df in dataframe_dict.items():
            tbl_parsed_dict[tbl] = {
                'filename':tbl,
                'df':df,
                'columns':df.columns,
                'pk':self.get_pk(df)
            }
        return tbl_parsed_dict

    def get_pk(self, df, suffix='', filter=''):
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

        relationship = {}
        for tbl in tbl_list:
            relationship[tbl] = []
            if one2many:
                for col in self.tbl_parsed_dict[tbl]['columns']:
                    for nxt_tbl, nxt_data in self.tbl_parsed_dict.items():
                        if nxt_tbl not in tbl_list and col in nxt_data['columns']:
                            relationship[tbl].append((col, nxt_tbl))
            else:
                key = self.tbl_parsed_dict[tbl]['pk']
                for nxt_tbl, nxt_data in self.tbl_parsed_dict.items():
                    if nxt_tbl != tbl and key in nxt_data['columns']:
                        relationship[tbl].append((key, nxt_tbl))
        return relationship
