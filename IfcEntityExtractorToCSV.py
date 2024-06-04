import ifcopenshell
from ifcopenshell.util.element import get_pset
from ifcopenshell.util.selector import Selector
from easygui import fileopenbox, filesavebox, enterbox
import pandas as pd
from pathlib import Path
import sys

Selector.get_class_selector()

files = fileopenbox(msg="Selecteer een of meerdere Ifc files", filetypes=["*.ifc", "*.ifczip"], multiple=True)
if files is None:
    sys.exit(0)
if type(files) != list:
    files = [files]

list_of_types = enterbox(msg="Geef de IfcEntitie(s) op die gechecked moeten worden. Gebruik een komma voor meerdere types", default='IfcElement', strip=True)

if ',' in list_of_types:
    list_of_types = list_of_types.split(',')
else:
    list_of_types = [list_of_types]

list_of_psets = enterbox(msg='Geef de naam van de pset(s) die opgehaald moeten worden. Gebruik een komma voor meerdere Psets', strip=False)
if ',' in list_of_psets:
    list_of_psets = list_of_psets.split(',')
else:
    list_of_psets = [list_of_psets]

list_of_elements = []
for file_name in files:
    ifc_file = ifcopenshell.open(file_name)
    for ifc_type in list_of_types:
        elements = ifc_file.by_type(ifc_type)
        print('file:', file_name, 'elements:', len(elements))
        for element in elements:
            properties = {'NO_PSET': []}
            for pset in list_of_psets:
                pset_properties = get_pset(element=element, name=pset)
                if type(pset_properties) != dict:
                    properties['NO_PSET'].append(pset)
                else:
                    properties.update(pset_properties)
            properties['IfcFile_Name'] = Path(file_name).stem
            properties['GUID'] = element.GlobalId
            properties['Element_name'] = element.Name
            properties['Element_badID'] = element.Tag
            list_of_elements.append(properties)

csvfile = filesavebox(msg="CSV filenaam", filetypes=[".csv"], default='parameters.csv')

df = pd.DataFrame.from_dict(list_of_elements)
df.to_csv(csvfile)
print(df)