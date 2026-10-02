#!/usr/bin/env python3
"""Structural verification. Browser and Android checks are recorded separately."""
from pathlib import Path
import json,xml.etree.ElementTree as ET
from artwork import ICONS,ALIASES
from build import motion
ROOT=Path(__file__).resolve().parents[1]
NS={'a':'http://schemas.android.com/apk/res/android'}
A='{'+NS['a']+'}'
catalog=json.loads((ROOT/'catalog.json').read_text())
inventory=json.loads((ROOT/'inventory.json').read_text())
assert len(catalog['icons'])==len(ICONS)==197
assert inventory['unresolved']==[]
assert inventory['profileChoicesPerBranch']=={'main':140,'liquid-glass-ui':140}
assert {r for row in inventory['rows'] for r in row['replacements']}==set(ICONS)
for icon in catalog['icons']:
    for mode,variants in icon['paths'].items():
        assert set(variants)=={'light','dark','mono'}
        for theme,file in variants.items():
            raw=(ROOT/file).read_text();svg=ET.fromstring(raw)
            assert svg.attrib['viewBox']=='0 0 24 24'
            assert svg.attrib['width']==svg.attrib['height']=='24'
            assert all(e.tag.split('}')[-1] not in ['image','script','foreignObject','filter','text'] for e in svg.iter())
            assert all(not any(k.endswith('href') for k in e.attrib) for e in svg.iter())
            assert all('stroke-dasharray' not in e.attrib for e in svg.iter()),'Fallback must not rely on CSS or pathLength support'
            if mode=='animated':assert 'prefers-reduced-motion:no-preference' in raw
    id=icon['id'];native=icon['android']['static']
    v=ET.parse(ROOT/f'android/res/drawable/{native}.xml').getroot()
    names={e.attrib[A+'name'] for e in v.iter() if A+'name' in e.attrib}
    av=ET.parse(ROOT/f'android/res/drawable/{icon["android"]["animated"]}.xml').getroot()
    for target in av.findall('target'):assert target.attrib[A+'name'] in names
    for p in ICONS[id]['parts']:
        if p['motion']:
            for key,frames in motion(p['motion']).items():
                assert frames[-1][0]==1
                assert frames[-1][1]==(1 if key in ['trim','sx','sy'] else 0)
for f in (ROOT/'android/res').rglob('*.xml'):ET.parse(f)
assert all(v in ICONS for v in ALIASES.values())
print(f'PASS: {len(ICONS)} icons; 1,182 SVGs; 594 Android XML resources; {inventory["records"]} source records; 0 missing mappings.')
