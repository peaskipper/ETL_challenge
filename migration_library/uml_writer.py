class puml_script():

    def __init__(self, classification:list=None):
        self.script = """
@startuml
hide circle
skinparam linetype ortho
skinparam shadowing false
skinparam entity {
BackgroundColor<<Fact>> #FDF6E3
BackgroundColor<<Dimension>> #E6F7FF
}
"""

    def add_entity(self, name:str, columns:list, typ:str='Fact'):
        
        line_break = '\n\t\t'
        entity_txt = f'''
entity "{name}" <<{typ}>> {{
    * {line_break.join(columns)}
}}'''
        self.script += entity_txt
        return self.script
    
    def add_relationship(self, relation_dict):
        """ WIP """
        line_break = '\n\t\t'
        trgt_tbl = ''
        src_tbl = ''
        entity_txt = f'''\n{trgt_tbl} }}|--0| {src_tbl}'''
        self.script += entity_txt
        return self.script

    def end_script(self, file_path:str):
        self.script += '@enduml'
        with open(file_path, "w") as f:
            f.write(self.script)
        
        file = file_path.rsplit('\\',1)[-1]
        print(f"ER diagram PlantUML file generated: {file}")

    def formatting(self):
        """"
        lines.append("left to right direction") #("top to bottom direction")
        lines.append("skinparam defaultTextAlignment center")
        lines.append("skinparam dpi 150")
        """
        return None