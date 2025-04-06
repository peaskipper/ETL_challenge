class puml_script():

    def __init__(self, classification:list=None,format:str=None):
        self.script = "@startuml"
        default_format = """
hide circle
top to bottom direction
skinparam dpi 200
skinparam defaultTextAlignment left
skinparam linetype ortho
skinparam shadowing false
skinparam entity {
BackgroundColor<<Fact>> #FDF6E3
BackgroundColor<<Hier>> #E6F7FF
}
"""
        self.script += default_format if not format else format

    def add_entity(self, name:str, columns:list, typ:str='Fact'):
        
        line_break = '\n\t\t'
        column_struct = [f"{col} : {col_typ}" for col, col_typ in columns]
        if len(column_struct) > 1:
            column_struct = line_break.join([column_struct[0], '---'] + column_struct[1:])
        else:
            column_struct = column_struct[0] if column_struct else ''

        entity_txt = f'''
entity "{name}" <<{typ}>> {{
    pk: {column_struct}
}}'''
        self.script += entity_txt
        return self.script
    
    def add_relationship(self, relation_dict, arrow_text=False):
        """ WIP """
        line_break = '\n'
        self.script += line_break
        for trgt_tbl, rel_tuple in relation_dict.items():
            for keycol,src_tbl in rel_tuple:
                keycol = f'"{keycol}" ' if arrow_text else ''
                entity_txt = f'''{line_break}{tbl_name_reformat(trgt_tbl)} {keycol}}}|--o| {tbl_name_reformat(src_tbl)}'''
                self.script += entity_txt
            self.script += line_break
        return self.script

    def end_script(self, file_path:str):
        self.script += '\n\n@enduml'
        with open(file_path, "w") as f:
            f.write(self.script)
        
        file = file_path.rsplit('\\',1)[-1]
        print(f"ER diagram PlantUML file generated: {file}")

    def diagram_reformat(self):
        """WIP"""
        return None
    

def tbl_name_reformat(tbl, to_replace:str='.', replace_with:str='_'):
    """"
    Reformat table names by replacing special characters
    """
    return tbl.replace(to_replace,replace_with)