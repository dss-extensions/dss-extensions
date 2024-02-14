"""
A quick script to extract most of the DSS data from the internal DSS C-API schema; mixes some AltDSS-Schema to complement it.
"""
from dss import lib, ffi, dss
import json
import html
from mako.template import Template
import textwrap
from pathlib import Path

out_path = Path('./dss-format')
out_path.mkdir(exist_ok=True)

escape = html.escape

numeric_enums = ['InvControl: Control Model', 'Generator: Model', 'Load: Model', 'PVSystem: Model', 'UPFC: Mode'] # TODO: extract from JSON Schema
mo = Path('../messages/messages/properties-alt-en-US.mo')
assert mo.exists()
print(lib.DSS_SetPropertiesMO(bytes(mo.absolute())))
schema = json.loads(ffi.string(lib.DSS_ExtractSchema(ffi.NULL, False)))
json_schema = json.loads(ffi.string(lib.DSS_ExtractSchema(ffi.NULL, True)))['$defs']
# with open('legacy-schema.json', 'w') as f:
#     json.dump(schema, f)

global_enums = schema['globalEnums']
id_to_enum = {e['id']: e for e in global_enums}

def get_slug(s):
    return s.replace(': ', '').replace(' - ', ' ').replace(' ', '-').lower()

found = set()
def fix_parent(par):
    par = par.replace('Element', ' Element').replace('Class', ' Element').replace('Data', ' Data').replace('  ', ' ').replace('Ckt', 'Circuit')
    if par not in found:
        found.add(par)
    
    return par

for cls in schema['classes']:
    cls['parents'] = [fix_parent(par) for par in cls['parents']]
    
# print(found)
#schema['classes'] = sorted(schema['classes'], key=lambda x: (len(x['parents']), x['name']))

commands = [(dss.Executive.Command(i), dss.Executive.CommandHelp(i)) for i in range(1, dss.Executive.NumCommands + 1)]
#commands

options = [(dss.Executive.Option(i), dss.Executive.OptionHelp(i)) for i in range(1, dss.Executive.NumOptions + 1)]

commands = dict(sorted(commands, key=lambda x: x[0].lower()))
options = dict(sorted(options, key=lambda x: x[0].lower()))

def notes(p, cls):
    res = ''
    if 'Redundant' in p['flags']:
        other = cls['properties'][p["redundantWith"] - 1]['name']
        res += f'<br>***Redundant with {other}***'

    if 'Unused' in p['flags']:
        res += f'<br>***Not used***'

    return res

#TODO: legend explaining how each is codified in the DSS text format
# preamble = open('/home/meira/projects/dss/dss_gen/properties_preamble.md', 'r').read()
# show_export = open('/home/meira/projects/dss/dss_gen/properties_show_export.md', 'r').read()

files = []

types = {
    'Integer': 'integer',
    'IntegerArray': 'array of integers',
    'Double': 'real',
    'ComplexPartSymMatrix': 'array of reals<br>*(symmetric matrix)*',
    'DoubleSymMatrix': 'array of reals<br>*(symmetric matrix)*',
    'MappedIntEnum': 'integer<br>*(from enum.)*',
    'MappedStringEnum': 'string<br>*(from enum.)*',
    'StringEnumAction': 'string<br>*(from enum., action)*',
    'MappedStringEnumOnStructArray': 'string<br>*(from enum., on array)*',
    'MappedStringEnumArray': 'array of strings<br>*(from enum.)*',
    'MappedStringEnumArrayOnStructArray': 'array of strings<br>*(from enum.)*',
    'BooleanAction': 'boolean<br>*(action)*',
    'MakeLike': 'string<br>*([{classname}](#{classname}) name)*<br>[deprecated]{{.fg-warning}}',
    'DSSObjectReference': 'string<br>*(object name)*',
    'DSSObjectReferenceArray': 'array of strings<br>*(object names)*',
    'DoubleDArray': 'array of reals',
    'DoubleArray': 'array of reals',
    'DoubleVArray': 'array of reals',
    'DoubleFArray': 'array of reals',
    'DoubleArrayOnStructArray': 'array of reals',
    'DoubleOnArray': 'real<br>*(on array)*',
    'DoubleOnStructArray': 'real<br>*(on array)*',
    'String': 'string',
    'Boolean': 'boolean',
    'Enabled': 'boolean',
    'IntegerOnStructArray': 'integer<br><br>*(on array)*',
    'Bus': 'string<br>*(bus def.)*',
    'BusOnStructArray': 'string<br>*(bus def., on array)*',
    'BusesOnStructArray': 'array of strings<br>*(bus defs., on array)*',
    'StringList': 'array of strings',
    'ComplexParts': 'complex',
    'Complex': 'complex',
    'StringSilentROFunction': 'string<br>**(read-only)**',
    'DeprecatedAn': '[deprecated/removed]{{.fg-warning}}',
}

def fix_ref(param):
    if param == 'PDElement':
        return '#pd-elements'
    
    if param == 'CktElement':
        return '#circuit-elements'

    return '#' + param

def ptypes(p, cls):
    t = p['type'] 
    if t == 'DSSObjectReference':
        param = p['params'][1]
        # print(param)
        if '|' not in param:
            return f'string<br>*([{param}]({fix_ref(param)}) name)*'
        else:
            options = ' or '.join(f'[{p}]({fix_ref(p)})' for p in param[1:-1].split('|'))
            return f'string<br>*({options} name)*'

    if t == 'DSSObjectReferenceArray':
        param = p['params'][1]
        print(param)
        return f'array of strings<br>*([{param}]({fix_ref(param)}) names)*'
    
    res = types.get(t, t).format(classname=cls['name'])
    if 'from enum.' not in res:
        return res
    
    enum = id_to_enum[p['params'][1]]
    enum_slug = get_slug('enum-' + enum['name'])
    short_name = ''
    if enum['name'].startswith(cls['name'] + ':') or enum['name'].startswith(cls['name'] + ' '):
        short_name = enum['name'][len(cls['name']) + 1:].lstrip()

    return res.replace('from enum.', f'from enum. [{short_name}](#{enum_slug})')


commands_template = r'''---
html_theme.sidebar_secondary.remove: true
---
# Commands

DSS commands as implemented in AltDSS/DSS C-API implementation of the OpenDSS engine. All are available in OpenDSS, but there are some omissions like OpenDSS-GIS commands (either closed-source or not publicly available).

:::{list-table}
:header-rows: 1
:align: center
*   - Name
    - Description
% for opt, desc in items.items():
*   - `${opt}`
    - ${desc.replace('\n', '<br>')}
% endfor
:::
'''

commands_txt = Template(commands_template).render(items=commands)

options_template = r'''---
html_theme.sidebar_secondary.remove: true
---
# General Options

General DSS options as implemented in AltDSS/DSS C-API implementation of the OpenDSS engine. All are available in OpenDSS.

:::{list-table}
:header-rows: 1
:align: center
*   - Name
    - Description
% for opt, desc in items.items():
*   - `${opt}`
    - ${desc.replace('\n', '<br>')}
% endfor
:::
'''
options_txt = Template(options_template).render(items=options)

general = []
controls = []
pdelements = []
pcelements = []
cktelements = []
meterelements = []

fn_classes = {
    'General Objects': general,
    'Control Elements': controls,
    'PD Elements': pdelements,
    'PC Elements': pcelements,
    'Meter Elements': meterelements,
    # 'Circuit Elements': cktelements,
}

def get_default(jcls, p, cls):
    if 'on array' in ptypes(p, cls):
        return '' #TODO?

    if p['name'] in jcls['properties']:
        p2 = jcls['properties'][p['name']]
        # print(p2)
        res = p2.get('default', '')
        if res is not None:
            if isinstance(res, float):
                return round(res, 3)

            if isinstance(res, list) and len(res) and isinstance(res[0], str):
                return '[{}]'.format(', '.join(res))

            return res

    return ''


for cls in schema['classes']:
    cls_name = cls['name']
    class_enums = cls.get('classEnums', [])
    id_to_enum.update({e['id']: e for e in class_enums})
    for e in class_enums:
        names, vals = e['names'], e['values']
        if e['name'] in ('Relay: Action', 'Relay: State', 'Recloser: Action', 'Recloser: State', 'AutoTrans: Connection', 'Monitor: Action', ):
            continue

        val_to_name = {}
        for v, n in zip(vals, names):
            if v not in val_to_name:
                val_to_name[v] = n
                continue
            prev = val_to_name[v]
            if len(prev) < len(n) and n.lower().startswith(prev.lower()):
                val_to_name[v] = n
                continue
            
            assert len(prev) > len(n) and prev.lower().startswith(n.lower()), (e['name'], prev, n)

        e['values'], e['names'] = zip(*list(val_to_name.items()))


    json_schema_cls = json_schema[cls_name]

    out_file_name = cls_name + '.md'
    out_file: Path = out_path / out_file_name

    parents = cls['parents']
    # if 'Circuit Element' in parents and not ('PC Element' in parents or 'PD Element' in parents or 'Control Element' in parents):
    #     cktelements.append(out_file_name)
        
    if len(parents):
        if 'PC Element' in parents:
            pcelements.append(out_file_name)
        elif 'PD Element' in parents:
            pdelements.append(out_file_name)
        elif 'Control Element' in parents:
            controls.append(out_file_name)
        elif 'Meter Element' in parents:
            meterelements.append(out_file_name)
        else:
            general.append(out_file_name)
    else:
        general.append(out_file_name)

    output = (Template((r'''---
html_theme.sidebar_secondary.remove: true
---

# ${cls['name']}

(
% if len(cls['parents']) > 1:        
% for par in cls['parents'][1:]:
    ${par}${'' if loop.last else ','}
% endfor
% else:
        General
% endif        
)

:::{list-table}
:header-rows: 1
:align: center
*   - Index
    - Name
    - Type
    - Default
    - Units
    - Description
% for p in cls['properties']:
*   - ${p['index']}
    - `${(p['name'])}`
    - ${types(p, cls)}
    - ${get_default(json_schema_cls, p, cls)}
    - ${p.get('units') or ''}
    - ${(p['description'] + notes(p, cls)).replace("\n", "<br>")}
% endfor
:::
% if enums:

${'##'} Enumerations

% for e in sorted(enums, key=lambda e: e['name']):
(${get_slug('enum-' + e['name'])})=
${"###"} ${e['name']}

:::{list-table}
:header-rows: 1
:align: center
% if e['name'] not in numeric_enums:
*   - Value
%   for opt, desc in zip(e['names'], e['values']):
*   - `${opt}`
%   endfor
% else:
*   - Value
    - Description
%   for opt, desc in zip(e['names'], e['values']):
*   - `${desc}`
    - ${opt}
%   endfor
% endif
:::

%  if e['hybrid']:
**This is a "hybrid" enumeration.** The related input properties accepts the values listed in this table and integer numbers greater than 1.
%  endif

% endfor
% endif
''')).render(
        types=ptypes,
        cls=cls,
        notes=notes,
        get_default=get_default,
        json_schema_cls=json_schema_cls,
        enums=class_enums,
        get_slug=get_slug,
        numeric_enums=numeric_enums,
        # preamble=markdown(preamble, extensions=['tables', 'md_in_html']), 
        # show_export=markdown(show_export, extensions=['tables', 'md_in_html'])
    ))

    out_file.write_text(output)
    files.append(out_file_name)


short_types = {
    'General Objects': 'general',
    'Control Elements': 'control',
    'PD Elements': 'pde',
    'PC Elements': 'pce',
    'Circuit Elements': 'ce',
    'Meter Elements': 'me',
}

for element_type, fns in fn_classes.items():
    short_type = short_types.get(element_type)
    if not short_type:
        continue
    toc_template = r'''

(${element_type_slug})=
# ${element_type}
```{toctree}
:maxdepth: 2
% for fn in sorted(fns):
${fn}
% endfor
```
'''
    out_file: Path = out_path / f'toc_{short_type}.md'
    out_file.write_text(Template(toc_template).render(element_type=element_type, fns=fns, element_type_slug=element_type.replace(' ', '-').lower()))


out_file: Path = out_path / f'Options.md'
out_file.write_text(options_txt)

out_file: Path = out_path / f'Commands.md'
out_file.write_text(commands_txt)


global_enums_template = r'''
# General Enumerations

These are general enumerations, lists of acceptable values, that can be used in more than one of the data elements. Specific classes may also specify additional enumerations.

% for e in sorted(enums, key=lambda e: e['name']):
(${get_slug('enum-' + e['name'])})=
${"##"} ${e['name']}

:::{list-table}
:header-rows: 1
:align: center
*   - Value
% for opt, desc in zip(e['names'], e['values']):
*   - `${opt}`
% endfor
:::

%  if e['hybrid']:
**This is a "hybrid" enumeration.** The related input properties accepts the values listed in this table and integer numbers greater than 1.
%  endif

% endfor


'''


for e in global_enums:
    names, vals = e['names'], e['values']
    if e['name'] in ('Connection', 'Phase Sequence'):
        continue

    val_to_name = {}
    for v, n in zip(vals, names):
        if v not in val_to_name:
            val_to_name[v] = n
            continue
        prev = val_to_name[v]
        if len(prev) < len(n) and n.lower().startswith(prev.lower()):
            val_to_name[v] = n
            continue
        
        assert len(prev) > len(n) and prev.lower().startswith(n.lower()), (e['name'], prev, n)

    e['values'], e['names'] = zip(*list(val_to_name.items()))


out_file: Path = out_path / f'Enumerations.md'
out_file.write_text(Template(global_enums_template).render(enums=global_enums, get_slug=get_slug))