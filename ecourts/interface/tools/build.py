#!/usr/bin/env python3
"""Rebuild the authored SVG, VectorDrawable and AnimatedVectorDrawable library."""
from pathlib import Path
import json, html, hashlib, re, base64
from artwork import ICONS, ALIASES

ROOT=Path(__file__).resolve().parents[1]
THEMES={
 'light':dict(ink='#482F36',accent='#E9543E',end='#C93639',soft='#E9543E',surface='#FFF4ED'),
 'dark':dict(ink='#F7E9E2',accent='#FFD1A6',end='#FF9271',soft='#FFAC8A',surface='#352026'),
 'mono':dict(ink='currentColor',accent='currentColor',end='currentColor',soft='currentColor',surface='currentColor')
}

# One timeline drives the SVG and native Android exports. Values are measured
# in the 24-unit viewBox, degrees, or unitless scale / trim fractions.
def motion(name):
    if name=='trace':return {'trim':[(0,0),(.15,0),(.8,1),(1,1)]}
    curves={
      'seat':('ty',[-2.1,-.7,.18,0,0]),'seat-late':('ty',[-2.1,-2.1,-.4,.12,0]),'seat-later':('ty',[-2.1,-2.1,-1.2,.12,0]),
      'turn':('sx',[.55,.72,1.02,1,1]),'scan':('tx',[0,-1.1,1.1,-.15,0]),
      'balance':('r',[-7,-3,2,-.4,0]),'strike':('r',[-7,-3,.8,-.2,0]),
      'open':('sx',[.68,.75,1.02,1,1]),'press':('ty',[-1.4,-.7,.35,0,0]),
      'write':('tx',[-1.3,-.8,.7,.15,0]),'flap':('sy',[.76,.82,1.015,1,1]),
      'shelve':('r',[6,4,-.7,.1,0]),'join-right':('tx',[-1.4,-.8,.08,0,0]),'join-left':('tx',[1.4,.8,-.08,0,0]),
      'align':('ty',[-1.5,-.5,.1,0,0]),'extend':('sy',[.65,.8,1.02,1,1]),
      'step':('ty',[-1.5,-1.2,.2,0,0]),'expression':('sy',[.7,.8,1.08,1,1]),
      'incline':('r',[-5,-3,.8,0,0]),'select':('sx',[.7,.82,1.04,1,1]),
      'unfold':('sy',[.6,.85,1.02,1,1]),'grow':('sy',[.7,.85,1.02,1,1]),
      'bloom':('sx',[.78,.9,1.035,1,1]),'rays':('sy',[.8,.9,1.02,1,1]),
      'rise':('ty',[1.8,1,-.1,0,0]),'drift':('tx',[-.8,-.3,.8,.2,0]),
      'ear':('r',[-7,-3,1.5,0,0]),'wing':('r',[-10,-4,1.5,0,0]),'tail':('r',[-8,5,-2,.5,0]),
      'peek':('tx',[-1.2,-.6,.1,0,0]),'crawl':('tx',[-.8,-.4,.6,0,0]),
      'clock':('r',[-20,-10,2,.3,0]),'ring':('r',[-9,6,-2.5,.6,0]),'ring-late':('r',[0,-8,4,-1,0]),
      'sector':('tx',[1.2,.7,-.05,0,0]),'answer':('r',[-7,-3,1,0,0]),'unlock':('r',[-12,-6,2,0,0]),
      'fly':('ty',[1.5,.7,-.2,0,0]),'swell':('ty',[0,-.5,.5,.1,0]),
      'exhaust':('sy',[.5,.75,1.04,1,1]),'aperture':('sx',[1,.7,.85,1,1]),
      'snip':('r',[-12,-7,0,1,0]),'lift':('ty',[1.2,.2,-.4,0,0]),'goal':('ty',[-2,-.7,.1,0,0]),
      'tune':('tx',[-1.5,-.8,.1,0,0]),'back':('tx',[1,.5,-.5,0,0]),'forward':('tx',[-1,-.5,.5,0,0]),
      'download':('ty',[-2,-1,.2,0,0]),'upload':('ty',[2,1,-.2,0,0]),
      'lid':('r',[-10,-5,1,0,0]),'copy':('tx',[-1.6,-.7,.1,0,0]),'rewind':('r',[20,10,-2,0,0]),
      'paper':('ty',[-2,-.9,.1,0,0]),'switch-on':('tx',[-5,-2.5,.1,0,0]),'switch-off':('tx',[5,2.5,-.1,0,0]),
    }
    if name.startswith('work-'):
        phase={'work-a':0,'work-b':.16,'work-c':.32}[name]
        return {'sy':[(0,1),(phase,1),(phase+.17,.4),(phase+.36,1),(1,1)]}
    if name=='progress':return {'tx':[(0,0),(.4,7),(.7,7),(1,0)]}
    key,vals=curves[name]
    return {key:list(zip([0,.26,.58,.82,1],vals))}

def write(path,data):
    target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(data,encoding='utf-8')
def num(v):return f'{v:.4f}'.rstrip('0').rstrip('.') if v else '0'

def svg(item,theme,animated=False):
    id=item['id'];pfx=f'ecui-{id}-{theme}'+('-motion' if animated else '')
    t=THEMES[theme];mono=theme=='mono'
    root=f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" role="img" aria-label="{html.escape(item["label"])}" class="{pfx}">'
    lines=[root,f'<title>{html.escape(item["label"])}</title>',f'<desc>{html.escape(item["motion"] if animated else item["label"]+". Original eCourts interface icon.")}</desc>']
    if not mono:
        lines.append(f'<defs><linearGradient id="{pfx}-accent" gradientUnits="userSpaceOnUse" x1="4" y1="3" x2="20" y2="22"><stop stop-color="{t["accent"]}" style="stop-color:var(--ec-icon-accent,{t["accent"]})"/><stop offset="1" stop-color="{t["end"]}" style="stop-color:var(--ec-icon-accent-end,{t["end"]})"/></linearGradient></defs>')
    css=[]
    for i,p in enumerate(item['parts']):
        if animated and p['motion']:
            curves=motion(p['motion']);key=next(iter(curves));frames=curves[key]
            cssprop={'tx':'translateX','ty':'translateY','r':'rotate','sx':'scaleX','sy':'scaleY'}.get(key)
            unit='px' if key in ['tx','ty'] else 'deg' if key=='r' else ''
            data=''.join(f'{num(f*100)}%{{'+(f'stroke-dashoffset:{num(1-v)}' if key=='trim' else f'transform:{cssprop}({num(v)}{unit})')+'}' for f,v in frames)
            selector=f'.{pfx} .p{i}'
            css.append(f'{selector}{{'+('stroke-dasharray:1;stroke-dashoffset:0;' if key=='trim' else '')+f'transform-box:view-box;transform-origin:{p["pivot"][0]}px {p["pivot"][1]}px;animation:{pfx}-p{i} {item["duration"]}ms cubic-bezier(.3,0,.2,1) '+('infinite' if item['loop'] else '1')+' backwards}'+f'@keyframes {pfx}-p{i}{{{data}}}')
    if css:lines.append('<style>@media(prefers-reduced-motion:no-preference){'+''.join(css)+'}</style>')
    for i,p in enumerate(item['parts']):
        role=p['role'];color=t[role];style=''
        if role=='accent' and not mono:color=f'url(#{pfx}-accent)'
        elif not mono:style=f' style="'+('fill' if p['fill'] else 'stroke')+f':var(--ec-icon-{role},{color})"'
        attr=f'fill="{color}"' if p['fill'] else f'fill="none" stroke="{color}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round"'
        if role=='soft':attr+=' opacity="0.12"'
        if mono and role=='surface':attr+=' opacity="0.5"'
        if animated and p['motion']=='trace':attr+=' pathLength="1"'
        lines.append(f'<path class="p{i}" d="{p["d"]}" {attr}{style}/>')
    return '\n'.join(lines+['</svg>',''])

def vector(item,mono=False):
    prefix='ecui_'+item['id'].replace('-','_')
    lines=['<vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">']
    for i,p in enumerate(item['parts']):
        color='@color/ecui_mono' if mono else '@color/ecui_'+p['role']
        attr=f'android:fillColor="{color}"' if p['fill'] else f'android:fillColor="@android:color/transparent" android:strokeColor="{color}" android:strokeWidth="1.65" android:strokeLineCap="round" android:strokeLineJoin="round"'
        if p['role']=='soft':attr+=' android:fillAlpha="0.12"'
        if mono and p['role']=='surface':attr+=f' android:{"fill" if p["fill"] else "stroke"}Alpha="0.5"'
        lines.append(f'<group android:name="g{i}" android:pivotX="{p["pivot"][0]}" android:pivotY="{p["pivot"][1]}">')
        if p['role']=='accent' and not mono:
            prop='fillColor' if p['fill'] else 'strokeColor'
            attr=re.sub(f'android:{prop}="[^"]+"','',attr)
            lines.append(f'<path android:name="p{i}" android:pathData="{p["d"]}" {attr}><aapt:attr name="android:{prop}"><gradient android:startX="4" android:startY="3" android:endX="20" android:endY="22" android:type="linear"><item android:offset="0" android:color="@color/ecui_accent"/><item android:offset="1" android:color="@color/ecui_accent_end"/></gradient></aapt:attr></path>')
        else:lines.append(f'<path android:name="p{i}" android:pathData="{p["d"]}" {attr}/>')
        lines.append('</group>')
    return '\n'.join(lines+['</vector>',''])

def avd(item):
    name='ecui_'+item['id'].replace('-','_')
    lines=[f'<animated-vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt" android:drawable="@drawable/{name}">']
    for i,p in enumerate(item['parts']):
        if not p['motion']:continue
        for key,frames in motion(p['motion']).items():
            target=f'p{i}' if key=='trim' else f'g{i}'
            prop=dict(trim='trimPathEnd',tx='translateX',ty='translateY',sx='scaleX',sy='scaleY',r='rotation')[key]
            lines.append(f'<target android:name="{target}"><aapt:attr name="android:animation"><objectAnimator android:duration="{item["duration"]}" android:repeatCount="'+('-1' if item['loop'] else '0')+'" android:interpolator="@android:interpolator/linear"><propertyValuesHolder android:propertyName="'+prop+'" android:valueType="floatType">')
            # AVD keyframes have linear segment interpolation; an explicit
            # shared easing curve resource matches each CSS interval.
            for f,v in frames:lines.append(f'<keyframe android:fraction="{num(f)}" android:value="{num(v)}" android:interpolator="@interpolator/ecui_settle"/>')
            lines.append('</propertyValuesHolder></objectAnimator></aapt:attr></target>')
    return '\n'.join(lines+['</animated-vector>',''])

def build():
    catalog=[]
    for item in ICONS.values():
        id=item['id'];paths={}
        for mode in ['static','animated']:
            paths[mode]={}
            for theme in THEMES:
                p=f'{mode}/{theme}/{id}.svg';write(p,svg(item,theme,mode=='animated'));paths[mode][theme]=p
        native='ecui_'+id.replace('-','_')
        write(f'android/res/drawable/{native}.xml',vector(item))
        write(f'android/res/drawable/{native}_mono.xml',vector(item,True))
        write(f'android/res/drawable/{native}_animated.xml',avd(item))
        catalog.append({k:v for k,v in item.items() if k!='parts'}|dict(paths=paths,android=dict(static=native,animated=native+'_animated',mono=native+'_mono'),aliases=[k for k,v in ALIASES.items() if v==id]))
    for theme,qual in [('light','values'),('dark','values-night')]:
        values=THEMES[theme]|dict(accent_end=THEMES[theme]['end'],mono=THEMES[theme]['ink'])
        write(f'android/res/{qual}/ecui_colors.xml','<resources>\n'+''.join(f'<color name="ecui_{k}">{v}</color>\n' for k,v in values.items() if k!='end')+'</resources>\n')
    write('android/res/interpolator/ecui_settle.xml','<pathInterpolator xmlns:android="http://schemas.android.com/apk/res/android" android:controlX1="0.3" android:controlY1="0" android:controlX2="0.2" android:controlY2="1"/>\n')
    write('catalog.json',json.dumps(dict(version='1.0.0',viewBox=[0,0,24,24],strokeWidth=1.65,themes=list(THEMES),icons=catalog,aliases=ALIASES),indent=2)+'\n')
    if (ROOT/'inventory.json').exists():
        template=(ROOT/'tools/gallery.html').read_text()
        embedded={str(f.relative_to(ROOT)):'data:image/svg+xml;base64,'+base64.b64encode(f.read_bytes()).decode() for folder in ['static','animated'] for f in (ROOT/folder).rglob('*.svg')}
        def inline_image(match):
            src=match[1]
            if src.startswith(('../icons/','static/','animated/')):
                return 'src="data:image/svg+xml;base64,'+base64.b64encode((ROOT/src).read_bytes()).decode()+'"'
            return match[0]
        template=re.sub(r'src="([^"]+)"',inline_image,template)
        gallery=template.replace('__CATALOG__',json.dumps(dict(version='1.0.0',icons=catalog),separators=(',',':')).replace('</','<\\/')).replace('__AUDIT__',json.dumps(json.loads((ROOT/'inventory.json').read_text()),separators=(',',':')).replace('</','<\\/')).replace('__ASSETS__',json.dumps(embedded,separators=(',',':')))
        write('index.html',gallery)
    print(f'Built {len(catalog)} icons / {len(catalog)*6} SVGs / {len(catalog)*3} Android drawables.')

if __name__=='__main__':build()
