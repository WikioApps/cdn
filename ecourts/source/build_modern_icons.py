#!/usr/bin/env python3
"""Native SVG brand marks for eCourts. No raster artwork or dependencies."""
from pathlib import Path
from html import escape
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]

def f(n):
    return f'{n:.3f}'.rstrip('0').rstrip('.') if isinstance(n,float) else str(n)

def node(kind, **attributes):
    attrs=' '.join(f'{k.replace("_","-")}="{escape(f(v),quote=True)}"' for k,v in attributes.items())
    return f'<{kind} {attrs}/>'

def p(d,**kw):
    return node('path',d=d,**kw)

def box(x,y,w,h,r=0,**kw):
    return node('rect',x=x,y=y,width=w,height=h,rx=r,**kw)

def disc(cx,cy,r,**kw):
    return node('circle',cx=cx,cy=cy,r=r,**kw)

def g(content,**kw):
    attrs=' '.join(f'{k.replace("_","-")}="{escape(f(v),quote=True)}"' for k,v in kw.items())
    return f'<g {attrs}>\n'+('\n'.join(content) if isinstance(content,list) else content)+'\n</g>'

def polar(cx,cy,r,degrees):
    t=math.radians(degrees)
    return f'{cx+r*math.cos(t):.3f} {cy+r*math.sin(t):.3f}'

def arc_band(cx,cy,outer,inner,start,end):
    return f'M{polar(cx,cy,outer,start)}A{outer} {outer} 0 {int(end-start>180)} 1 {polar(cx,cy,outer,end)}L{polar(cx,cy,inner,end)}A{inner} {inner} 0 {int(end-start>180)} 0 {polar(cx,cy,inner,start)}Z'

def rounded_path(x,y,w,h,r):
    return f'M{x+r} {y}H{x+w-r}Q{x+w} {y} {x+w} {y+r}V{y+h-r}Q{x+w} {y+h} {x+w-r} {y+h}H{x+r}Q{x} {y+h} {x} {y+h-r}V{y+r}Q{x} {y} {x+r} {y}Z'

# Each concept is drawn independently. The mark is a geometric silhouette;
# colour and surface treatments are separate editable SVG layers.
def civic():
    return [
        ('body', [p(arc_band(507,512,278,151,39,321)),box(300,455,464,114,57)]),
    ]

def parity():
    top='M362 284H744Q771 284 758 308L698 418Q686 440 661 440H280Q253 440 266 416L326 306Q338 284 362 284Z'
    # Opposing diagonals balance the visual weight of two equal bars.
    return [('body',[p(top)]),('accent',[p(top,transform='rotate(180 512 512)')])]

def folio():
    left='M244 300Q244 267 273 280L489 373V758L274 663Q244 650 244 618Z'
    right='M531 373L747 280Q776 267 776 300V618Q776 650 746 663L531 758Z'
    return [
        ('body',[p(left)]),('accent',[p(right)]),
        ('fold',[p('M244 300Q244 267 273 280L489 373V502L273 407Q244 394 244 363Z')]),
    ]

def forum():
    back='M340 230H496Q602 230 602 336V356H476Q376 356 376 456V548H350L278 618Q258 638 258 610V540Q226 510 226 464V344Q226 230 340 230Z'
    front='M530 402H686Q798 402 798 514V626Q798 694 751 723L772 775Q784 804 755 790L648 738H530Q422 738 422 630V510Q422 402 530 402Z'
    return [('accent',[p(back)]),('body',[p(front)])]

def gateway():
    arch='M248 748V474C248 327 358 222 512 222S776 327 776 474V748H648V476C648 397 593 350 512 350S376 397 376 476V748Z'
    return [('body',[p(arch),box(456,500,112,248,56)])]

def docket():
    # A case-index grid with an unmistakable folded upper-right corner.
    return [
        ('body',[
            p('M310 260H486V486H260V310Q260 260 310 260Z'),
            p('M538 260H658L764 366V486H538Z'),
            p('M260 538H486V764H310Q260 764 260 714Z'),
            p('M538 538H764V690Q764 764 690 764H538Z'),
        ]),
        ('accent',[p('M658 260V333Q658 366 691 366H764Z')]),
    ]

def links():
    # Two open obrounds interlock through an explicit gap; no hidden masks.
    a='M452 558V394C452 353 477 326 512 326S572 353 572 394V444H680V394C680 293 610 218 512 218S344 293 344 394V558Z'
    b='M572 466V630C572 671 547 698 512 698S452 671 452 630V580H344V630C344 731 414 806 512 806S680 731 680 630V466Z'
    return [('body',[p(a,transform='rotate(38 512 512)')]),('accent',[p(b,transform='rotate(38 512 512)')])]

def decide():
    return [
        ('accent',[p(arc_band(491,517,270,173,52,302))]),
        ('body',[p('M375 489L462 574L703 316Q722 296 742 314L790 361Q809 380 790 400L490 718Q469 740 448 718L292 563Q273 544 292 525L333 487Q354 468 375 489Z')]),
    ]

def bench():
    roof='M254 352L483 218Q512 201 541 218L770 352Q792 365 780 387L740 456L512 324L284 456L244 387Q232 365 254 352Z'
    return [
        ('body',[p(roof),box(282,500,116,256,26),box(454,426,116,330,26),box(626,500,116,256,26)]),
    ]

def juris():
    left='M485 229V367L382 427Q366 437 366 456V568Q366 587 382 597L485 657V795L263 667Q238 652 238 624V400Q238 372 263 357Z'
    right='M539 229L761 357Q786 372 786 400V624Q786 652 761 667L539 795V657L642 597Q658 587 658 568V456Q658 437 642 427L539 367Z'
    return [('body',[p(left)]),('accent',[p(right)])]

DESIGNS=[
    dict(id='01-civic',name='Civic',draw=civic,idea='A custom e with an open circular silhouette.',
         light=('#2855F5','#163CC9','#FFFFFF','#EBF3FF','#B8CCFF','#FCFFFF'),dark=('#10182D','#080E1B','#81ACFF','#3566FA','#BBD3FF','#C6DFFF')),
    dict(id='02-parity',name='Parity',draw=parity,idea='Two equal bars with opposing diagonal cuts.',
         light=('#FFF5EF','#F6E6E0','#EF533D','#D43438','#F39677','#F4775B'),dark=('#261717','#100F14','#FFAC8A','#F05A48','#FFA17B','#FFD1A6')),
    dict(id='03-folio',name='Folio',draw=folio,idea='An open record expressed as two folded planes.',
         light=('#7154F5','#4D36C8','#FFFFFF','#E7DFFF','#E5BAFF','#BEB0FF'),dark=('#1D1931','#0E101A','#C6B6FF','#8B71F1','#FFC5CF','#BEA5FF')),
    dict(id='04-forum',name='Forum',draw=forum,idea='Two voices with a clear space between them.',
         light=('#F2FAF7','#DAEAE3','#176B5C','#0F4D45','#62BCA1','#86D8B9'),dark=('#10241F','#09120F','#CDF5DE','#83CFAF','#288D77','#70CCA9')),
    dict(id='05-gateway',name='Gateway',draw=gateway,idea='A broad arch and a central column form one mark.',
         light=('#E3F88C','#C9E85F','#253B29','#15271D','#546E35','#344934'),dark=('#172018','#0B110D','#EBFFA3','#BFDD65','#EBFFA3','#F5FFCB')),
    dict(id='06-docket',name='Docket',draw=docket,idea='A four-part case index with a folded corner.',
         light=('#F8F4F0','#E9E5DD','#2A354A','#172233','#EAA277','#FBC390'),dark=('#18202B','#0B111A','#E5EBF4','#B1C0D8','#F4B286','#FFD4A9')),
    dict(id='07-case-link',name='Case Link',draw=links,idea='Two open links connect a case and its history.',
         light=('#256DDE','#104BAC','#FFFFFF','#D8EEFF','#92CFF4','#DCF9FF'),dark=('#122234','#0A101C','#A0E2FF','#469BD7','#6685FF','#B3C3FF')),
    dict(id='08-decide',name='Decide',draw=decide,idea='A decisive stroke breaks through an open circle.',
         light=('#FFF8F0','#F1E4D3','#E45D32','#B74423','#203F48','#466A70'),dark=('#291E16','#121311','#FFC083','#F1894C','#527D83','#8CC4BF')),
    dict(id='09-bench',name='Bench',draw=bench,idea='A roof and three pillars reduced to bold geometry.',
         light=('#B73558','#872640','#FFF3E9','#F1C8C3','#FFE7CB','#FFF8ED'),dark=('#2B1722','#140D17','#FFA6B4','#D95A7D','#FFE5DD','#FFD7C9')),
    dict(id='10-juris',name='Juris',draw=juris,idea='Two court brackets create a shared hexagonal space.',
         light=('#EFF4FA','#DCE5F0','#294E70','#102F4E','#4589AA','#6FB6C8'),dark=('#10242D','#081219','#A9EDE4','#50A7B6','#728EFF','#C3D1FF')),
]

def linear(id,stops,xy):
    x1,y1,x2,y2=xy
    out=f'<linearGradient id="{id}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
    for offset,color,opacity in stops:
        out+=node('stop',offset=offset,stop_color=color,stop_opacity=opacity)
    return out+'</linearGradient>'

def svg_art(design,theme):
    parts=design['draw']()
    id=design['id']+'-'+theme
    defs=[]
    prefix=lambda s:id+'-'+s
    paint=lambda s:'url(#'+prefix(s)+')'
    symbol=[]
    if theme=='mono':
        for name,shapes in parts:
            # A fold is material detail on an existing plane, not extra geometry.
            if name=='fold':continue
            symbol.append(g(shapes,id=prefix('shape-'+name),fill='#FFFFFF'))
        body=g(symbol,id=prefix('symbol'))
        desc='Single-colour white foreground on transparency for tinting and silhouette inspection.'
    else:
        bg1,bg2,main1,main2,accent1,accent2=design[theme]
        defs.extend([
            linear(prefix('tile'),[(0,bg1,1),(1,bg2,1)],(170,0,860,1024)),
            linear(prefix('body'),[(0,main1,1),(.5,main1,1),(1,main2,1)],(270,260,770,795)),
            linear(prefix('accent'),[(0,accent2,1),(.6,accent1,1),(1,accent1,1)],(290,240,730,800)),
            linear(prefix('fold'),[(0,accent2,1),(1,accent1,1)],(250,270,520,530)),
            linear(prefix('surface-light'),[(0,'#FFFFFF',.16),(.36,'#FFFFFF',.035),(.8,'#FFFFFF',0),(1,'#FFFFFF',.045)],(245,210,782,802)),
            linear(prefix('rim'),[(0,'#FFFFFF',.55),(.45,'#FFFFFF',.06),(1,'#FFFFFF',.18)],(264,224,774,810)),
            linear(prefix('reflection'),[(0,'#FFFFFF',0),(.47,'#FFFFFF',0),(.5,'#FFFFFF',.13),(.54,'#FFFFFF',.035),(1,'#FFFFFF',0)],(200,175,860,900)),
        ])
        silhouette=[]
        for name,shapes in parts:
            if name!='fold':silhouette.extend(shapes)
        defs.append('<clipPath id="'+prefix('mark-clip')+'">'+''.join(silhouette)+'</clipPath>')
        # A restrained, close contact shadow gives edge separation; it never
        # becomes a scene or floating 3D object under the mark.
        defs.append('<filter id="'+prefix('contact')+'" x="-15%" y="-15%" width="130%" height="140%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="3.5"/></filter>')
        shadow=g(silhouette,id=prefix('contact-shadow'),fill='#000714',opacity=.09 if theme=='light' else .2,filter=paint('contact'),transform='translate(0 5)')
        for name,shapes in parts:
            symbol.append(g(shapes,id=prefix('shape-'+name),fill=paint(name)))
        # Separate clipping preserves all original path geometry for editing.
        finish=g([
            box(190,190,644,644,fill=paint('surface-light')),
            box(190,190,644,644,fill=paint('reflection')),
        ],id=prefix('satin-finish'),clip_path=paint('mark-clip'))
        rim='' if design['id']=='01-civic' else g(silhouette,id=prefix('edge-definition'),fill='none',stroke=paint('rim'),stroke_width=1.25,stroke_linejoin='round',opacity=.46)
        body=g([box(0,0,1024,1024,fill=paint('tile'))],id=prefix('background'))+'\n'+shadow+'\n'+g(symbol,id=prefix('symbol'))+'\n'+finish+'\n'+rim
        desc='Full-bleed '+theme+' app icon. '+design['idea']+' Independently editable silhouette, colour and surface layers.'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" role="img" aria-labelledby="{prefix("title")} {prefix("description")}">\n<title id="{prefix("title")}">eCourts — {escape(design["name"])} — {theme}</title>\n<desc id="{prefix("description")}">{escape(desc)} Original native vector artwork without raster images, fonts or external resources.</desc>\n<defs>\n'+ '\n'.join(defs)+'\n</defs>\n'+body+'\n</svg>\n'

def preview(manifest):
    # One review board, built from the actual delivered vectors.
    width,height=1600,2110
    parts=[box(0,0,width,height,fill='#F1F2F4')]
    parts.append('<text x="52" y="65" font-family="Arial,sans-serif" font-size="32" font-weight="700" fill="#152131">eCourts / new identities</text>')
    parts.append('<text x="52" y="102" font-family="Arial,sans-serif" font-size="19" fill="#586373">Ten geometric marks · light and dark</text>')
    for i,item in enumerate(manifest['icons']):
        col=i%2; row=i//2; x=52+col*775; y=151+row*390
        parts.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="23" font-weight="600" fill="#182431">{i+1:02d} / {escape(item["name"])}</text>')
        for ti,theme in enumerate(['light','dark']):
            raw=(ROOT/item['variants'][theme]['path']).read_text()
            inner=raw[raw.index('>')+1:raw.rindex('</svg>')]
            clip=f'board-clip-{i}-{theme}'
            px=x+ti*351;py=y+26
            parts.append(f'<defs><clipPath id="{clip}">{box(px,py,320,320,74)}</clipPath></defs>')
            parts.append(f'<g clip-path="url(#{clip})"><svg x="{px}" y="{py}" width="320" height="320" viewBox="0 0 1024 1024">{inner}</svg></g>')
    (ROOT/'preview.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Ten new eCourts app icon designs in light and dark">\n'+'\n'.join(parts)+'\n</svg>\n')

def build():
    manifest={'version':3,'format':'SVG','canvas':[1024,1024],'icons':[]}
    for design in DESIGNS:
        item={'id':design['id'],'name':design['name'],'description':design['idea'],'variants':{}}
        for theme in ['light','dark','mono']:
            svg=svg_art(design,theme)
            dest=ROOT/'icons'/design['id']/(theme+'.svg')
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(svg)
            item['variants'][theme]={'path':str(dest.relative_to(ROOT)),'bytes':dest.stat().st_size}
        manifest['icons'].append(item)
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    preview(manifest)
    readme=['# eCourts app icons','',
        'Ten new geometric identities. Every design includes a light icon, a dark icon and a white foreground SVG on transparency.','',
        '[![Preview all ten designs](preview.svg)](preview.svg)','',
        '| Design | Light SVG | Dark SVG | Monochrome SVG |',
        '| --- | --- | --- | --- |']
    for item in manifest['icons']:
        v=item['variants'];base=item['id']
        readme.append(f'| **{item["name"]}** — {item["description"]} | [Light]({v["light"]["path"]}) | [Dark]({v["dark"]["path"]}) | [Foreground]({v["mono"]["path"]}) |')
    readme.extend(['','## Use','',
        '- All source icons have a 1024 × 1024 viewBox and editable vector paths.',
        '- Light and dark files have a full square background. Rounded corners appear only in the preview; the launcher applies its own mask.',
        '- The monochrome file contains the foreground only, with transparent surroundings and open negative spaces.',
        '- There are no embedded PNGs, external images, external fonts, scripts or linked assets in the icons.',
        '- SVG is the source format. Native Android launcher bitmap resources or VectorDrawable XML need a separate export.',
        '',
        '[Machine-readable paths](manifest.json) · [Source generator](source/build_modern_icons.py)','',
        'Example raw SVG: [Civic, dark](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/icons/01-civic/dark.svg). Replace `main` with a commit SHA to pin a CDN URL.','',
        'Regenerate from the repository root with `python3 ecourts/source/build_modern_icons.py`. Python standard library only.',''])
    (ROOT/'README.md').write_text('\n'.join(readme))
    print(json.dumps({'designs':len(manifest['icons']),'svg_variants':30,'preview':'ecourts/preview.svg'}))

if __name__=='__main__':
    build()
