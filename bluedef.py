#%%
import os
import re
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from unidecode import unidecode


current_directory = Path(__file__).parent
assigned_numbers_directory = current_directory / "yaml" / "assigned_numbers"
template_directory = current_directory / "template"
output_directory = current_directory / "output"

env = Environment(loader=FileSystemLoader(template_directory))

NESTED_BRACKET_MAX = 3

def keep_text_inside_parentheses(text):
    return re.sub(r'[\(\{](.*?)[\)\}]', r'_\1_', text.replace(' ', '_'))

def symbol_modifier(name:str):
    name = unidecode(name)
    
    for _ in range(NESTED_BRACKET_MAX):
        name = keep_text_inside_parentheses(name)
    
    name = name.upper()\
        .replace(" ", "_")\
        .replace(",", "")\
        .replace(".", "")\
        .replace("+", "_PLUS_")\
        .replace("&", "_AND_")\
        .replace("!", "_")\
        .replace("\"", "")\
        .replace("|", "")\
        .replace("\'", "")\
        .replace("-", "_")\
        .replace("/", "_")\
        .replace("__", "_")\
        .replace("\\TEXTSUBSCRIPT", "")
    
    if name[0] in "0123456789":
        name = "_" + name 
    
    name = name.replace("__", "_")
    name = name.replace("__", "_")
    if name[-1] == "_":
        name = name[:-1]
    
    return name
        
def process_company_identifier():
    entries = []
    with open(os.path.join(assigned_numbers_directory, "company_identifiers", "company_identifiers.yaml"), encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        
        for elem in data['company_identifiers']:
            entries.append(
                {
                    'symbol' : symbol_modifier(elem['name']),
                    'identifier' : f"{elem['value']:04X}"
                }
            )
        
        return entries
    
def process_uuids(category : str, uuid_tail:bool = True):
    entries = []
    with open(os.path.join(assigned_numbers_directory, "uuids", f"{category}" + ("_uuids" if uuid_tail else "" + "") + ".yaml"), encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        pass
        for elem in data['uuids']:
            entries.append(
                {
                    'symbol' : symbol_modifier(elem['name']),
                    'identifier' : f"{elem['uuid']:04X}"
                }
            )
        
        return entries
    
def render(language:str, extension:str):
    template = env.get_template(f'{language}/bluedef.{extension}.j2')
    output_directory = os.path.join("output", language)
    
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory, exist_ok=True)
    
    output   = os.path.join(output_directory, f'bluedef.{extension}')

    with open(output, 'w') as f:
        f.write(
            template.render(
                namespaces = {
                    'Company'           : process_company_identifier(),
                    'ServiceUUID'       : process_uuids("service"),
                    'CharacteristicUUID': process_uuids("characteristic"),
                    'DescriptorUUID'    : process_uuids("descriptors", uuid_tail=False),
                    'UnitUUID'          : process_uuids("units", uuid_tail=False),
                }
            )
        )

for language, extension in [("c", "h"), ("cpp", "h"), ("rust", "rs")]:
    render(language, extension)

