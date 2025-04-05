from os import listdir
from pandas import read_table

class ingest_src():
    def __init__(self,src_location:str,extension:str,compression:str,separator:str,classification:list=[]):
        self.src_location = src_location
        self.extension = extension
        self.compression = compression
        self.separator = separator
        self.classification = classification
        return None

    def ingest(self):
        self.src_file_list = self.get_src_files(self.src_location,self.extension)
        self.df_dict = self.create_df(self.src_file_list,self.compression,self.separator)
        return self.df_dict

    def get_src_files(self, loc:str, ext:str, prefix:str=None) -> list:
        if not loc.endswith('\\'):
            loc += '\\'
        file_list = [loc+i for i in listdir(loc) if i.endswith(ext) and (not prefix or i.startswith(prefix))]
        return file_list

    def create_df(self, file_list:list,compression:str, sep:str) -> dict:
        df_dict = {}
        for file in file_list:

            df_name = file.rsplit('\\',1)[-1]
            df = read_table(file,compression=compression,sep=sep)
            df_dict[df_name] = df

            state = f'Loaded {df_name}'
            print(state)
            # log += state + '\n'
        return df_dict