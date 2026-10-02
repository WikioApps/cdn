#!/usr/bin/env python3
"""Build the editable eCourts artwork. Standard library only; no raster assets."""
from pathlib import Path
from html import escape
import math
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def num(v):
    return f'{v:.3f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)

def attrs(a):
    return ' '.join(f'{k.replace("_", "-")}="{escape(num(v), quote=True)}"' for k,v in a.items() if v is not None)

def tag(t, **a):
    return f'<{t} {attrs(a)}/>'

def path(d, fill='none', **a):
    return tag('path', d=d, fill=fill, **a)

def rect(x,y,w,h,fill,rx=0,**a):
    return tag('rect', x=x,y=y,width=w,height=h,rx=rx,fill=fill,**a)

def circle(x,y,r,fill,**a):
    return tag('circle',cx=x,cy=y,r=r,fill=fill,**a)

def ellipse(x,y,rx,ry,fill,**a):
    return tag('ellipse',cx=x,cy=y,rx=rx,ry=ry,fill=fill,**a)

def line(x1,y1,x2,y2,color,width=2,**a):
    return tag('path',d=f'M{num(x1)} {num(y1)}L{num(x2)} {num(y2)}',fill='none',stroke=color,stroke_width=width,stroke_linecap='round',**a)

def group(name, content, **a):
    return f'<g id="{name}" {attrs(a)}>\n'+('\n'.join(content) if isinstance(content,list) else content)+'\n</g>'

def paint(name):
    return f'url(#{name})'

class Art:
    def __init__(self, slug, name, dark, bg, accent):
        self.slug, self.name, self.dark = slug, name, dark
        self.defs, self.body = [], []
        self.serial=0
        self.ink='#040B18' if dark else '#293242'
        self.accent=accent
        self.gradient('background', bg, (0,0,1024,1024))
        self.gradient('gold', ['#FFF4CA','#E6BD6A','#9F692F','#F0DCA0','#BC8540'], (270,230,762,800))
        self.gradient('gold-cross', ['#775026','#D5A256','#FFF1C1','#CA9650','#825129'], (340,0,670,0))
        self.gradient('gold-edge', ['#FFFFDF','#E2B96F','#704721'], (250,220,750,800))
        self.gradient('silver', ['#F9FEFF','#B5C6CF','#F5FBFF','#738D9C','#CADCE7'], (250,230,780,800))
        self.gradient('silver-cross', ['#6C8497','#EAF6FF','#FFFFFF','#91AABB','#DBEAF5'], (370,0,670,0))
        self.gradient('porcelain', ['#FFFFFF','#F5EEDD','#D7CDB7','#FCF8EC'], (250,260,770,800))
        self.gradient('paper', ['#FFFFFB','#F4F2E9','#CBC9BB'], (260,230,810,860))
        self.gradient('edge-light', [('#FFFFFF',.96),('#FFFFFF',.36),(accent,.22),('#FFFFFF',.65)], (230,220,790,810))
        self.gradient('shine', [('#FFFFFF',.55),('#FFFFFF',.07),('#FFFFFF',0)], (260,200,750,620))
        self.gradient('wood', ['#AB673E','#733F27','#9C5430','#4A281D'], (270,290,730,690))
        self.gradient('wood-cross', ['#3B2019','#94542F','#BE8050','#7C462B','#3A211B'], (320,0,700,0))
        self.gradient('leather', ['#AD4C50','#783039','#561F2E','#3D1825'], (300,210,760,790))
        self.gradient('enamel', [accent,'#12697D','#082F49'], (240,230,760,820))
        self.gradient('crystal', [('#FFFFFF',.83),(accent,.78),('#3695B9',.61),('#14568E',.91)], (230,200,820,800))
        self.gradient('crystal-edge', ['#E6FFFF',accent,'#174870','#9AF1EE'], (250,230,770,850))
        self.gradient('frost', [('#FFFFFF',.93),('#E7FAFF',.79),(accent,.68)], (240,240,760,800))
        self.radial('ambient', [('#FFFFFF',.12 if dark else .9),('#FFFFFF',0)], .32,.15,.88)
        self.radial('halo', [(accent,.17 if dark else .13),(accent,0)], .5,.47,.48)
        self.radial('ground', [('#020916',.5 if dark else .28),('#020916',0)], .5,.5,.5)
        self.defs.append('<filter id="soft-shadow" x="-35%" y="-35%" width="170%" height="180%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="13"/></filter>')
        self.defs.append('<filter id="small-shadow" x="-25%" y="-25%" width="150%" height="160%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="4"/></filter>')
        self.body.append(group('backplate',[
            rect(0,0,1024,1024,paint('background')),
            rect(0,0,1024,1024,paint('ambient')),
            rect(0,0,1024,1024,paint('halo')),
        ]))

    def gradient(self, id, stops, coords=(0,0,1,1)):
        stop=[]
        for i,c in enumerate(stops):
            color, opacity = c if isinstance(c,tuple) else (c,1)
            stop.append(tag('stop',offset=i/(len(stops)-1),stop_color=color,stop_opacity=opacity))
        self.defs.append(f'<linearGradient id="{id}" gradientUnits="userSpaceOnUse" x1="{coords[0]}" y1="{coords[1]}" x2="{coords[2]}" y2="{coords[3]}">'+''.join(stop)+'</linearGradient>')

    def radial(self,id,stops,cx,cy,r):
        s=''.join(tag('stop',offset=i/(len(stops)-1),stop_color=c,stop_opacity=o) for i,(c,o) in enumerate(stops))
        self.defs.append(f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}">'+s+'</radialGradient>')

    def clip(self, shape):
        self.serial+=1
        id=f'clip-{self.serial}'
        self.defs.append(f'<clipPath id="{id}">{shape}</clipPath>')
        return paint(id)

    def add(self, content):
        self.body.extend(content if isinstance(content,list) else [content])

    def ground(self,cx=512,cy=798,rx=330,ry=86):
        self.add(ellipse(cx,cy,rx,ry,paint('ground')))

    def relief(self,d,material='gold',dx=0,dy=10,width=2):
        return [path(d,'#061C2C',opacity=.5,transform=f'translate({dx} {dy+5})',filter=paint('small-shadow')),
                path(d,paint(material+'-edge' if material in ['gold','crystal'] else material),transform=f'translate({dx} {dy})'),
                path(d,paint(material),stroke=paint('edge-light'),stroke_width=width,stroke_linejoin='round')]

    def write(self, folder, description):
        theme='dark' if self.dark else 'light'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" role="img" aria-labelledby="title description">\n<title id="title">eCourts — {escape(self.name)} — {theme}</title>\n<desc id="description">{escape(description)} Editable vector artwork. No raster images, fonts, scripts or external resources.</desc>\n<defs>\n'+ '\n'.join(self.defs)+'\n</defs>\n'+'\n'.join(self.body)+'\n</svg>\n'
        # Remove unused material definitions and namespace every identifier so
        # multiple icons can also be inlined together without gradient collisions.
        for _ in range(3):
            referenced=set(re.findall(r'url\(#([^)]+)\)',svg))
            svg=re.sub(r'<(linearGradient|radialGradient|filter|clipPath) id="([^"]+)"[^>]*>.*?</\1>',lambda m:m[0] if m[2] in referenced else '',svg,flags=re.S)
        prefix=self.slug+'-'+theme+'-'
        svg=re.sub(r'id="([^"]+)"',lambda m:f'id="{prefix}{m[1]}"',svg)
        svg=re.sub(r'url\(#([^)]+)\)',lambda m:f'url(#{prefix}{m[1]})',svg)
        svg=svg.replace('aria-labelledby="title description"',f'aria-labelledby="{prefix}title {prefix}description"')
        svg=re.sub(r'\n{3,}','\n\n',svg)
        dest=ROOT/folder/'icons'/self.slug/f'{theme}.svg'
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(svg)
        return {'path':str(dest.relative_to(ROOT)), 'bytes':dest.stat().st_size}

def fine_hatch(a,shape,x0,y0,x1,y1,spacing=5,color='#FFFFFF',opacity=.13,slope=.35):
    clip=a.clip(shape)
    lines=[]
    for y in range(int(y0-(x1-x0)*abs(slope)),int(y1+(x1-x0)*abs(slope)),spacing):
        lines.append(line(x0,y,x1,y+(x1-x0)*slope,color,.8,opacity=opacity))
    return group(f'brushed-finish-{a.serial}',lines,clip_path=clip)

def chain(x,y1,y2, color='silver'):
    out=[]
    n=int((y2-y1)/10)
    for i in range(n):
        y=y1+i*(y2-y1)/max(n-1,1)
        out.append(ellipse(x,y,3.4 if i%2 else 2,6,'none',stroke='#263D42',stroke_width=3))
        out.append(ellipse(x-.7,y-.8,3 if i%2 else 1.5,5.3,'none',stroke=paint(color),stroke_width=1.7))
    return out

def small_scales(cx,cy,s=1,fill='gold'):
    items=[path('M498 336Q512 312 526 336L522 568H502Z',paint(fill)),
           path('M363 381Q438 372 496 348H528Q586 372 661 381L660 395Q586 389 512 369Q438 389 364 395Z',paint(fill)),
           path('M464 573Q512 555 560 573L576 591H448Z',paint(fill)),
           circle(512,351,15,paint(fill))]
    for x in [382,642]:
        items.extend([path(f'M{x-52} 494L{x} 388L{x+52} 494',stroke=paint(fill),stroke_width=5),
                      path(f'M{x-60} 493Q{x} 573 {x+60} 493Z',paint(fill)),
                      ellipse(x,493,60,8,paint(fill))])
    return group('balance-emblem',items,transform=f'translate({cx} {cy}) scale({s}) translate(-512 -460)')

def balance(a):
    a.ground(cy=814)
    # Turned base, fine lathe lines and an enamel insert.
    a.add(group('turned-pedestal',[
        path('M343 764Q512 688 681 764V789Q512 859 343 789Z',paint('gold-cross')),
        ellipse(512,763,169,54,paint('gold')),
        ellipse(512,757,143,41,'#183E43'),
        ellipse(512,753,139,39,paint('enamel')),
        ellipse(512,752,137,37,'none',stroke=paint('gold-edge'),stroke_width=3),
    ]+[path(f'M{350+i*2} {780+i*.85}Q512 {837+i*.1} {674-i*2} {780+i*.85}',stroke='#F6DFA3' if i%2 else '#69451E',stroke_width=.85,opacity=.55) for i in range(15)]))
    stem='M499 271Q512 255 525 271L539 674Q544 702 577 715L590 736Q512 758 434 736L447 715Q480 702 485 674Z'
    a.add(group('cast-bronze-upright',a.relief(stem)+[fine_hatch(a,path(stem),430,265,594,756,3,'#FFF7D7',.14,0),path('M507 292L503 657Q501 705 465 723',stroke='#FFF6C9',stroke_width=4,opacity=.68)]))
    beam='M282 339Q396 319 474 291Q491 286 505 296L512 308L519 296Q533 286 550 291Q628 319 742 339Q755 342 753 354Q751 366 738 364Q623 351 536 325L512 341L488 325Q401 351 286 364Q273 366 271 354Q269 342 282 339Z'
    a.add(group('balanced-crossbeam',a.relief(beam,dy=7)+[fine_hatch(a,path(beam),270,280,755,380,3,'#FFF9DB',.21,.06),path('M283 343Q399 324 478 298L510 319L544 298Q625 324 740 343',stroke='#FFF4CE',stroke_width=3)]))
    for x in [304,720]:
        a.add(group(f'chains-{x}',chain(x,357,564,'gold')+[
            path(f'M{x} 377L{x-91} 564M{x} 377L{x+91} 564',stroke='#A37736',stroke_width=4),
            path(f'M{x-1} 378L{x-91} 564M{x+1} 378L{x+91} 564',stroke='#FFF0BE',stroke_width=1.8),
            circle(x,353,9,paint('gold'),stroke='#FFF0C5',stroke_width=1.5)]))
        pan=f'M{x-106} 562Q{x-88} 637 {x} 643Q{x+88} 637 {x+106} 562Z'
        a.add(group(f'enamel-pan-{x}',a.relief(pan,'enamel',dy=6)+[
            ellipse(x,561,106,21,paint('gold')),
            ellipse(x,560,93,13,'#082F42'),
            ellipse(x,558,87,10,paint('enamel')),
            path(f'M{x-90} 586Q{x} 669 {x+90} 586',stroke=paint('gold'),stroke_width=6),
            path(f'M{x-75} 590Q{x} 645 {x+75} 590',stroke='#BDEDE7',stroke_width=2,opacity=.48),
        ]+[path(f'M{x-85+i*5} 578Q{x-60+i*3.5} 610 {x-44+i*2.6} 626',stroke='#8AEAE7',stroke_width=.85,opacity=.18) for i in range(35)]))
    a.add(group('pivot',[
        circle(512,314,31,paint('gold-edge')),circle(512,310,26,paint('gold')),
        circle(512,310,15,paint('enamel')),circle(506,303,4,'#DBFFEF',opacity=.7),
        path('M496 263L502 237Q512 221 522 237L528 263Z',paint('gold')),
        ellipse(512,261,16,6,paint('gold-edge'))]))

def court(a):
    a.gradient('stone',['#FFF5E0','#DCC199','#B58E62','#E7D3AE'],(220,340,780,810))
    a.gradient('stone-cross',['#98794F','#EAD1A6','#FFF4D6','#BD9A6B'],(250,0,740,0))
    a.gradient('dome',['#F9D7A0','#C28D59','#805938'],(365,270,670,478))
    a.ground(cy=809,rx=360)
    a.add(group('stone-steps',[
        rect(211,773,602,36,paint('stone'),10),rect(237,746,550,35,paint('stone'),7),
        rect(259,724,506,30,paint('stone'),6),
        line(218,779,805,779,'#FFF3D5',3),line(246,752,779,752,'#FFF3D5',3),
    ]+[line(228,785+i*3,796,785+i*3,'#9E7E55',.85,opacity=.36) for i in range(6)]))
    wings=[]
    for x in [246,626]:
        wings.extend([rect(x,523,150,204,paint('stone'),3),rect(x-8,510,166,20,paint('gold'),3),rect(x-4,532,158,11,paint('stone-cross'),2)])
        for wy in [568,657]:
            for wx in [x+24,x+84]:
                d=f'M{wx} {wy+44}V{wy+3}A20 20 0 0 1 {wx+40} {wy+3}V{wy+44}Z'
                wings.extend([path(d,'#886B4B',stroke='#F3DBB5',stroke_width=6),path(f'M{wx+7} {wy+39}V{wy+5}A13 13 0 0 1 {wx+33} {wy+5}V{wy+39}Z','#27464C'),line(wx+20,wy-7,wx+20,wy+38,'#B6A17F',3),line(wx+6,wy+15,wx+34,wy+15,'#B6A17F',3),rect(wx-3,wy+43,46,7,paint('stone'))])
        for wy in range(548,716,14):
            wings.append(line(x+2,wy,x+148,wy,'#705B42',.7,opacity=.16))
    a.add(group('court-wings',wings))
    a.add(group('court-entrance',[
        rect(371,479,282,250,paint('stone-cross'),6),
        path('M443 723V624A69 69 0 0 1 581 624V723Z','#9F7C52'),
        path('M455 723V626A57 57 0 0 1 569 626V723Z','#173942'),
        path('M467 719V626A45 45 0 0 1 557 626V719Z',paint('enamel')),
        line(512,582,512,721,'#D9BD84',3),line(467,642,557,642,'#D9BD84',3),
        rect(482,661,20,40,'none',3,stroke='#C1AC83',stroke_width=2),
        rect(522,661,20,40,'none',3,stroke='#C1AC83',stroke_width=2),
    ]))
    columns=[]
    for x in [385,425,587,627]:
        columns.extend([rect(x-14,548,28,157,paint('stone-cross'),4),rect(x-22,539,44,12,paint('stone'),3),rect(x-19,551,38,10,paint('stone'),3),rect(x-21,706,42,13,paint('stone'),3),rect(x-24,719,48,12,paint('stone'),2)])
        for dx in range(-9,13,5):
            columns.extend([line(x+dx,566,x+dx,700,'#876B44',1.3,opacity=.5),line(x+dx+1.5,566,x+dx+1.5,700,'#FFF2CC',1.1,opacity=.6)])
    a.add(group('fluted-columns',columns))
    a.add(group('entablature',[
        path('M351 534L369 507H655L673 534Z',paint('stone')),
        rect(348,492,328,20,paint('gold'),4),rect(359,516,306,11,paint('stone-cross'),3),
    ]+[rect(371+i*17,528,8,10,paint('porcelain'),1) for i in range(17)]))
    dome='M371 462C371 382 411 334 460 317C477 307 487 291 491 277H533C537 291 547 307 564 317C613 334 653 382 653 462Z'
    a.add(group('ribbed-dome',[
        rect(390,464,244,26,paint('stone'),4),path(dome,paint('dome'),stroke='#FBE7BF',stroke_width=2),
    ]+[path(f'M{491+i*4.2} 280C{449+i*13} 331 {371+i*28.2} 372 {371+i*28.2} 459',stroke='#68462C',stroke_width=2,opacity=.35) for i in range(11)]+[
        path('M487 297C429 352 414 383 412 450',stroke='#FFF2C8',stroke_width=5,opacity=.52),
        rect(362,455,300,13,paint('gold'),4),rect(371,472,282,10,paint('stone-cross'),2),
        rect(483,265,58,18,paint('gold'),3),path('M490 265V247A22 22 0 0 1 534 247V265Z',paint('stone')),
        line(512,203,512,232,paint('gold'),8),circle(512,203,7,paint('gold')),
    ]))
    a.add(group('stone-masonry', [line(277,734+i*5,747,734+i*5,'#7A654D',.7,opacity=.24) for i in range(7)]))

def gavel(a):
    a.ground(cy=811,rx=320)
    a.add(group('sounding-block',[
        path('M326 760Q512 691 698 760V800Q512 875 326 800Z',paint('wood')),
        ellipse(512,759,186,55,paint('wood')),
        ellipse(512,750,173,44,paint('gold')),ellipse(512,746,160,38,paint('wood')),
        ellipse(512,741,148,33,paint('wood')),
    ]+[ellipse(512,740,148-i*6,33-i*1.25,'none',stroke='#D6965A',stroke_width=.8,opacity=.2) for i in range(21)]+[
        path('M336 790Q512 852 688 790',stroke=paint('gold'),stroke_width=6),
        path('M338 773Q512 835 686 773',stroke='#E7AF73',stroke_width=1.5,opacity=.5),
    ]))
    head='M322 283Q317 268 337 258H673Q693 268 688 283V390Q693 406 673 415H337Q317 406 322 390Z'
    grip='M480 387H530L547 643Q548 680 519 690H491Q462 680 463 643Z'
    a.gradient('handle',['#4F2B1E','#B87342','#CF9564','#754127','#442319'],(460,0,548,0))
    items=[path(grip,'#100E17',transform='translate(3 11)',opacity=.5,filter=paint('small-shadow')),path(grip,paint('handle'),stroke='#E2AD7E',stroke_width=1.5)]
    grain=[]
    for i in range(32):
        x=466+i*2.6
        grain.append(path(f'M{num(x)} 385C{num(x-7)} 445 {num(x+10)} 516 {num(x+1)} 572S{num(x-7)} 647 {num(x+2)} 696',stroke='#321C14' if i%3 else '#E9B57D',stroke_width=.75,opacity=.24))
    items.append(group('handle-grain',grain,clip_path=a.clip(path(grip))))
    items.extend([rect(470,398,70,27,paint('gold-cross'),8),rect(465,630,80,22,paint('gold-cross'),8),rect(465,667,79,13,paint('gold-cross'),6)])
    for y in [402,407,414,636,642,674]:
        items.append(line(472,y,538,y,'#FFF6CA',.9,opacity=.55))
    items.extend(a.relief(head,'wood',dx=4,dy=9))
    grain=[]
    for i in range(68):
        y=261+i*2.25
        grain.append(path(f'M319 {num(y)}C412 {num(y-9*math.sin(i*.21))} 463 {num(y+8)} 518 {num(y)}S614 {num(y-8)} 694 {num(y+4)}',stroke='#FFE0A3' if i%4==0 else '#2B160F',stroke_width=.75,opacity=.2))
    items.append(group('walnut-head-grain',grain,clip_path=a.clip(path(head))))
    for x in [331,636]:
        band=f'M{x} 257H{x+44}V416H{x}Q{x-9} 337 {x} 257Z'
        items.extend([path(band,paint('gold'),stroke='#FFF3CC',stroke_width=2),fine_hatch(a,path(band),x-8,256,x+47,418,3,'#5A391D',.23,.04),line(x+8,264,x+8,407,'#FFF7D9',2),line(x+36,264,x+36,407,'#63401D',2)])
    items.extend([ellipse(322,337,14,77,paint('wood')),ellipse(688,337,14,77,paint('wood')),path('M383 270H628',stroke='#F3C293',stroke_width=4,opacity=.36)])
    a.add(group('walnut-and-brass-gavel',items,transform='rotate(-35 512 495)'))

def book(a):
    a.ground(cy=820,rx=314)
    a.gradient('page-edge',['#AB9171','#F8EDD5','#D5BD93','#FFFFEC'],(390,690,767,767))
    a.gradient('ribbon',['#FEE6A4','#CF9B44','#F4D68D','#A36F2C'],(528,0,620,0))
    bottom='M313 282L699 236Q721 234 725 260L790 715Q794 739 770 745L388 824Q361 828 349 809Z'
    cover='M285 260Q282 232 309 228L694 185Q719 182 722 209L785 678Q789 706 761 713L378 791Q349 797 341 768Z'
    a.add(group('back-cover',a.relief(bottom,'leather',dy=9)+[
        path('M357 784L389 813L770 735',stroke='#CA716C',stroke_width=3,opacity=.6)]))
    pages='M356 711L739 641L772 727L391 805L361 784Z'
    a.add(group('gilt-page-block',[
        path(pages,paint('page-edge')),
    ]+[path(f'M{359+i*.6:.2f} {728+i*1.78:.2f}L{389+i*.035:.2f} {744+i*1.72:.2f}L{758+i*.28:.2f} {669+i*1.85:.2f}',stroke='#8E744B' if i%3 else '#FFFFE3',stroke_width=.95,opacity=.5) for i in range(35)]+[
        path('M390 744L391 798',stroke='#7B633F',stroke_width=2,opacity=.3)]))
    a.add(group('silk-bookmark',[
        path('M554 723L613 710L640 809L612 792L587 825Z',paint('ribbon'),stroke='#FFE5A1',stroke_width=1.5),
        path('M563 728L592 810M604 718L629 794',stroke='#916228',stroke_width=2,opacity=.35),
    ]+[path(f'M{566+i*2.7:.2f} 732L{590+i*2.7:.2f} 805',stroke='#FFF3C8',stroke_width=.6,opacity=.35) for i in range(15)]))
    a.add(group('leather-cover',a.relief(cover,'leather',dy=4)+[
        path('M309 239L694 197Q709 195 711 212L774 678Q776 694 759 698L381 776Q360 781 356 760L298 263Q296 241 309 239Z','none',stroke='#E7A36E',stroke_width=2,opacity=.75),
        path('M330 237L393 781',stroke='#341521',stroke_width=7,opacity=.6),
        path('M336 239L398 777',stroke='#C4756D',stroke_width=2,opacity=.5),
    ]))
    # Small leather pores follow the surface; they are visible at master size,
    # not a repeated generic texture pasted over the background.
    pores=[]
    for row in range(44):
        for col in range(27):
            x=348+col*13.6+(row%2)*6.3+row*1.35
            y=241+row*11.6-col*1.56
            if y>242-col*.13 and x<728:
                pores.append(path(f'M{num(x)} {num(y)}q2.1 -1.1 3.4 .7',stroke='#EAB897' if (row+col)%3==0 else '#240D19',stroke_width=.7,opacity=.16))
    a.add(group('leather-grain',pores,clip_path=a.clip(path(cover))))
    border='M365 264L673 228L729 655L419 719Z'
    inner='M378 276L661 244L715 643L430 701Z'
    a.add(group('foil-border',[
        path(border,stroke=paint('gold'),stroke_width=4,stroke_linejoin='round'),
        path(inner,stroke=paint('gold'),stroke_width=1.5,stroke_linejoin='round'),
    ]))
    corners=[path(d,stroke=paint('gold'),stroke_width=2.2,stroke_linecap='round') for d in [
        'M389 307Q386 283 409 279', 'M638 250Q660 247 664 270',
        'M427 674Q430 697 453 692', 'M690 646Q713 642 710 619']]
    a.add(group('foil-corner-work',corners))
    medallion=[ellipse(512,468,107,117,'none',stroke=paint('gold'),stroke_width=2),ellipse(512,468,99,109,'none',stroke=paint('gold'),stroke_width=1,opacity=.7)]
    for i in range(72):
        t=2*math.pi*i/72
        medallion.append(circle(512+102*math.cos(t),468+113*math.sin(t),1.3,paint('gold')))
    medallion.append(small_scales(512,464,.5))
    a.add(group('embossed-justice-mark',medallion,transform='matrix(.985 -.13 .13 1 -31 65)'))
    a.add(group('spine-bands',[
        path(f'M{300+i*11} {317+i*98}L{342+i*11} {312+i*98}',stroke=paint('gold'),stroke_width=9,opacity=.8) for i in range(4)
    ]))

def rosette(cx,cy,r,depth,petals,phase=0):
    p=[]
    for i in range(petals*16):
        t=i*2*math.pi/(petals*16)
        rr=r+depth*math.cos(t*petals+phase)
        p.append((cx+rr*math.cos(t),cy+rr*math.sin(t)))
    return 'M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in p)+'Z'

def seal(a):
    a.gradient('wax',['#EA7861','#B03939','#73273C','#A63F45'],(260,220,810,840))
    a.gradient('wax-rim',['#FEB899','#9B2839','#5B1830'],(260,200,780,830))
    a.gradient('seal-gold',['#FFF2C6','#C78E43','#ECC576','#98612F'],(280,220,760,840))
    a.ground(cy=813,rx=304)
    outer=rosette(512,507,290,11,20)
    a.add(group('poured-wax',[
        path(outer,'#050A15',transform='translate(0 25)',opacity=.4,filter=paint('soft-shadow')),
        path(outer,paint('wax-rim'),transform='translate(0 13)'),path(outer,paint('wax'),stroke='#F4A189',stroke_width=2),
        path(rosette(512,507,280,9,20),stroke='#FAB393',stroke_width=2,opacity=.6),
        circle(512,507,266,paint('wax-rim')),circle(512,503,257,paint('wax')),
        circle(512,504,243,paint('seal-gold'),stroke='#FFE4A2',stroke_width=3),
        circle(512,504,217,'#6B4030'),circle(512,501,212,paint('seal-gold')),
    ]))
    knurl=[]
    for i in range(120):
        t=2*math.pi*i/120
        x1,y1=512+226*math.cos(t),504+226*math.sin(t)
        x2,y2=512+238*math.cos(t+.01),504+238*math.sin(t+.01)
        knurl.extend([line(x1,y1,x2,y2,'#6F4324',1.4,opacity=.6),line(x1+1,y1-1,x2+1,y2-1,'#FFF0B7',1.1,opacity=.75)])
    a.add(group('milled-bronze-rim',knurl))
    # Interlocking guilloche rings are genuine engraved curve geometry.
    curves=[]
    for j in range(12):
        d=rosette(512,502,193,6.8,18,j*2*math.pi/12)
        curves.append(path(d,stroke='#FFF0B5' if j%2 else '#744721',stroke_width=.65,opacity=.56))
    a.add(group('guilloche-engraving',curves))
    a.add(group('inner-medallion',[
        circle(512,502,177,paint('wax')),circle(512,502,168,'none',stroke=paint('gold'),stroke_width=2),
    ]))
    # A single embossed fountain nib, rather than an official seal or crest.
    nib='M512 369L571 487L530 574H494L453 487Z'
    a.add(group('counsel-nib',a.relief(nib,'gold',dy=4)+[
        path('M512 380L462 486L496 558L484 490Z','#FFF3B7',opacity=.28),
        path('M518 390L561 486L529 558L542 491Z','#714823',opacity=.2),
        path('M512 380L512 499',stroke='#713A2C',stroke_width=3),
        circle(512,501,12,'#74303A',stroke='#F2CF8E',stroke_width=2),
        path('M469 489L495 548M555 489L529 548',stroke='#865A31',stroke_width=2),
        rect(485,573,54,16,paint('gold'),4),rect(474,591,76,14,paint('gold'),4),
    ]))
    laurel=[]
    for side in [-1,1]:
        branch=[]
        for i in range(50):
            t=.08+i*1.44/49
            branch.append((512+side*137*math.sin(t),495+142*math.cos(t)))
        laurel.append(path('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in branch),stroke=paint('gold'),stroke_width=2.5))
        for i in range(7):
            t=.24+i*.178
            x,y=512+side*137*math.sin(t),495+142*math.cos(t)
            tx,ty=side*math.cos(t),-math.sin(t)
            nx,ny=side*math.sin(t),math.cos(t)
            for outward in [-1,1]:
                ex,ey=x+tx*18+nx*18*outward,y+ty*18+ny*18*outward
                vx,vy=ex-x,ey-y
                length=math.hypot(vx,vy)
                px,py=-vy/length*6,vx/length*6
                d=f'M{x:.2f} {y:.2f}C{x+vx*.15+px:.2f} {y+vy*.15+py:.2f} {x+vx*.72+px:.2f} {y+vy*.72+py:.2f} {ex:.2f} {ey:.2f}C{x+vx*.72-px:.2f} {y+vy*.72-py:.2f} {x+vx*.15-px:.2f} {y+vy*.15-py:.2f} {x:.2f} {y:.2f}Z'
                laurel.append(path(d,paint('gold'),stroke='#FFE9AC',stroke_width=.7))
                laurel.append(line(x+vx*.15,y+vy*.15,x+vx*.8,y+vy*.8,'#7A512C',.7,opacity=.55))
    a.add(group('engraved-laurel',laurel))

def shield(a):
    a.ground(cy=814,rx=300)
    silhouette='M512 204Q615 264 746 275L733 544Q722 696 512 810Q302 696 291 544L278 275Q409 264 512 204Z'
    a.add(group('shield-cast-shadow',[path(silhouette,'#020B20',transform='translate(0 18)',opacity=.38,filter=paint('soft-shadow'))]))
    a.add(group('optical-shield',a.relief(silhouette,'crystal',dy=11,width=3)+[
        path('M512 222Q411 277 297 289L310 541Q321 684 512 788Q703 684 714 541L727 289Q613 277 512 222Z','none',stroke=paint('edge-light'),stroke_width=4),
        path('M512 241Q415 290 318 302L331 538Q338 650 512 762Q686 650 693 538L706 302Q609 290 512 241Z',paint('frost'),opacity=.64),
        path('M512 241L512 760Q686 650 693 538L706 302Q609 290 512 241Z',paint('crystal'),opacity=.42),
        path('M308 299Q408 288 500 240V410Q402 447 317 538Z',paint('shine')),
        path('M512 760Q697 649 712 535L726 300L694 331L680 537Q667 659 512 744Z',fill=a.accent,opacity=.6),
    ]))
    etch=[]
    for i in range(38):
        y=358+i*8.8
        x=324+(max(0,y-518)/5)
        etch.extend([line(x,y,x+13,y+7,'#E9FFFF',.9,opacity=.55),line(1024-x,y,1011-x,y+7,'#072B59',.9,opacity=.25)])
    a.add(group('bevel-refraction-cuts',etch))
    # A raised silver courthouse pillar is the primary legal identifier.
    pillar=[path('M451 374L512 338L573 374Z',paint('silver')),rect(448,377,128,20,paint('silver'),5),rect(455,405,114,19,paint('silver'),4),rect(477,424,70,170,paint('silver-cross'),7),rect(461,594,102,18,paint('silver'),5),rect(449,617,126,24,paint('silver'),6)]
    for x in range(488,544,10):
        pillar.extend([line(x,438,x,582,'#456C86',2,opacity=.6),line(x+3,438,x+3,582,'#FFFFFF',2,opacity=.75)])
    a.add(group('silver-court-column',pillar))
    a.add(group('shield-specular-edges',[
        path('M303 374L298 297Q421 281 507 230',stroke='#FFFFFF',stroke_width=4,opacity=.82),
        path('M707 544Q690 663 518 768',stroke='#CBFFFF',stroke_width=3,opacity=.88),
        path('M362 628Q413 703 482 741',stroke='#FFFFFF',stroke_width=2,opacity=.37),
    ]))

def docket(a):
    a.gradient('rear-file',['#DCD9FF','#9480CF','#5C4C8B'],(260,200,780,750))
    a.gradient('front-file',[('#E8FFFF',.87),('#77E5E6',.77),('#23A3B6',.92),('#136587',.95)],(250,320,780,800))
    a.ground(cy=821,rx=343)
    back='M274 282Q274 259 297 259H414L448 292H719Q744 292 744 318V678Q744 706 716 706H299Q274 706 274 679Z'
    a.add(group('rear-case-folder',[
        path(back,'#030B1E',transform='translate(0 17)',opacity=.4,filter=paint('soft-shadow')),
        path(back,paint('rear-file'),stroke='#DFDBFF',stroke_width=2,transform='rotate(-9 510 500)'),
        path('M296 276H407L436 310H720',stroke='#F8F2FF',stroke_width=3,opacity=.75,transform='rotate(-9 510 500)'),
    ]))
    a.add(group('case-documents',[
        rect(312,250,342,411,paint('paper'),20,transform='rotate(4 485 455)',stroke='#FFFFFF',stroke_width=2),
        rect(334,262,342,411,paint('paper'),20,transform='rotate(-2 505 466)',stroke='#C9DAE2',stroke_width=2),
        path('M371 282H615L677 344V681H354V302Q354 282 371 282Z',paint('paper'),stroke='#E7F6F8',stroke_width=2),
        path('M615 282V331Q615 344 628 344H677Z','#B8CFD6'),
        path('M617 286L673 342H628Q617 342 617 330Z','#FBFFFF'),
        rect(390,327,151,13,'#3A6172',6),rect(390,352,111,6,'#83A0AC',3),
    ]+[rect(391,389+i*24,221-(i%3)*25,5,'#A6B8BC',2) for i in range(8)]))
    front='M237 438Q236 410 263 410H396L430 445H769Q795 445 789 473L746 743Q742 773 712 773H298Q268 773 264 743Z'
    a.add(group('glass-folder',a.relief(front,'crystal',dy=11)+[
        path(front,paint('front-file'),stroke=paint('edge-light'),stroke_width=3),
        path('M258 426H391L423 462H773L753 587Q535 481 278 585Z',paint('shine')),
        path('M282 493L304 744H703Q727 744 731 721L769 476',stroke='#C2FFFF',stroke_width=2.5,opacity=.66),
        path('M281 742Q283 759 305 759H711Q731 759 734 741',stroke='#125B7C',stroke_width=4,opacity=.52),
    ]))
    a.add(group('folder-lip-machining',[
        path(f'M{276+i*.18:.2f} {735+i*1.9:.2f}Q510 {758+i*1.6:.2f} {728-i*.18:.2f} {735+i*1.9:.2f}',stroke='#D4FFFF',stroke_width=.75,opacity=.24) for i in range(12)
    ]))
    # A recessed, opaque plaque keeps the foreground readable over both themes.
    a.add(group('case-index-plaque',[
        rect(397,541,227,121,'#105977',20,opacity=.35),
        rect(396,535,227,121,paint('frost'),20,stroke='#E5FFFF',stroke_width=2),
        rect(414,553,39,82,paint('crystal'),8),
        rect(473,561,125,9,'#23617D',4),rect(473,584,95,7,'#4C90A0',3),
        rect(473,605,120,7,'#4C90A0',3),circle(433,576,7,'#F0FFFF'),
        path('M425 609L432 616L442 602',stroke='#EEFFFF',stroke_width=4,stroke_linejoin='round'),
    ]))
    a.add(group('precision-label-rules',[
        line(476+i*4,628,476+i*4,638 if i%4 else 641,'#438798',1.3,opacity=.75) for i in range(28)
    ]))

def calendar(a):
    a.gradient('calendar-glass',[('#FEF7FF',.92),('#BAADFC',.86),('#7C72C2',.9)],(270,260,790,810))
    a.gradient('calendar-cap',['#AB8DF2','#7761B3','#4D3E83'],(260,260,760,431))
    a.gradient('selected',['#FFECC7','#E7BD7B','#B7804B'],(420,530,550,664))
    a.ground(cy=818,rx=332)
    card='M285 271H733Q776 271 776 314V731Q776 776 731 776H288Q244 776 244 732V314Q244 271 285 271Z'
    a.add(group('calendar-body',a.relief(card,'crystal',dy=14)+[
        path(card,paint('calendar-glass'),stroke=paint('edge-light'),stroke_width=3),
        path('M285 281H733Q765 281 765 314V424H255V314Q255 281 285 281Z',paint('calendar-cap')),
        path('M260 433H760V730Q760 759 730 759H290Q260 759 260 730Z',paint('frost'),opacity=.88),
        line(258,423,764,423,'#F6E9FF',3),line(264,431,758,431,'#514579',2,opacity=.45),
        path('M280 290H732Q757 290 757 316',stroke='#FFF4FF',stroke_width=3,opacity=.7),
    ]))
    rings=[]
    for x in [365,655]:
        rings.extend([ellipse(x,340,30,13,'#44385B'),ellipse(x,337,24,9,'#E9E3FF'),
                      path(f'M{x-18} 333V249Q{x-18} 224 {x+2} 224Q{x+22} 224 {x+22} 248V271',stroke='#0F1B36',stroke_width=25,opacity=.4,transform='translate(0 6)'),
                      path(f'M{x-18} 333V249Q{x-18} 224 {x+2} 224Q{x+22} 224 {x+22} 248V271',stroke=paint('silver'),stroke_width=23),
                      path(f'M{x-23} 329V249Q{x-23} 219 {x+2} 219',stroke='#FFFFFF',stroke_width=3,opacity=.85)])
    a.add(group('steel-binder-rings',rings))
    a.add(group('header-inlay',[
        rect(454,344,114,8,'#F2E6FF',4,opacity=.9),rect(477,365,68,4,'#E0D4FA',2,opacity=.65),
    ]))
    cells=[]
    for row in range(3):
        for col in range(4):
            x,y=303+col*111,480+row*80
            if row==1 and col==1:
                cells.extend([rect(x-11,y-9,88,67,'#5C4775',16,opacity=.2,transform='translate(0 5)'),rect(x-11,y-9,88,67,paint('selected'),16,stroke='#FFF6DC',stroke_width=2),path(f'M{x+8} {y+23}L{x+24} {y+38}L{x+50} {y+8}',stroke='#725032',stroke_width=7,stroke_linecap='round',stroke_linejoin='round')])
            else:
                cells.extend([rect(x,y,65,45,'#8270AD',11,opacity=.18),rect(x+3,y+2,59,39,paint('frost'),9,opacity=.66),rect(x+17,y+18,31,6,'#61577F',3,opacity=.68)])
    a.add(group('hearing-date-grid',cells))
    a.add(group('etched-calendar-rim',[line(266,714+i*2.7,754,714+i*2.7,'#FFFFFF',.75,opacity=.26) for i in range(9)]))
    # An inset analog clock identifies hearings without language-specific text.
    clock=[circle(729,718,101,'#1F153A',opacity=.25,transform='translate(0 11)',filter=paint('small-shadow')),circle(729,718,101,paint('silver')),circle(729,716,88,'#F6F2FD'),circle(729,716,81,'none',stroke='#B5A7C7',stroke_width=1.5)]
    for i in range(60):
        t=i*math.pi/30
        r=71 if i%5==0 else 76
        clock.append(line(729+r*math.sin(t),716-r*math.cos(t),729+80*math.sin(t),716-80*math.cos(t),'#716283',2.4 if i%5==0 else 1))
    clock.extend([path('M729 663V716L759 737',stroke='#59436F',stroke_width=7,stroke_linecap='round',stroke_linejoin='round'),circle(729,716,7,paint('gold'))])
    a.add(group('hearing-clock',clock))

def column(a):
    a.gradient('jade-glass',[('#E5FFF5',.96),('#78DCC6',.9),('#258F86',.9),('#8AEBCD',.9)],(305,260,700,785))
    a.gradient('jade-cross',['#236A68','#7EE4C6','#E5FFF2','#73D8C0','#2C8C84'],(389,0,645,0))
    a.gradient('base-glass',['#DEFFF5','#76D9C6','#27867B'],(285,711,734,827))
    a.ground(cy=825,rx=303)
    a.add(group('crystal-stylobate',[
        path('M302 748L512 696L722 748V796L512 838L302 796Z',paint('base-glass'),stroke='#ADF4DD',stroke_width=2),
        path('M302 748L512 792L722 748L512 704Z',paint('frost')),
        path('M512 792V837L722 796V748Z',paint('jade-glass')),
        path('M319 763L512 804L705 764M319 778L512 819L705 779',stroke='#C4FFEB',stroke_width=1.5,opacity=.7),
        path('M348 731L512 692L676 731V753L512 789L348 753Z',paint('jade-glass'),stroke='#BEFFE8',stroke_width=2),
        path('M348 731L512 765L676 731L512 695Z',paint('frost')),
    ]))
    shaft='M414 368H610L632 704Q512 768 392 704Z'
    a.add(group('fluted-crystal-shaft',a.relief(shaft,'crystal',dy=6)+[
        path(shaft,paint('jade-cross'),stroke='#E6FFF4',stroke_width=2),
        path('M421 378H442L425 703Q412 708 400 703Z',paint('shine')),
    ]))
    flutes=[]
    for i in range(11):
        x1=425+i*16.8; x2=408+i*20.7
        d=f'M{x1:.2f} 395Q{x1+7:.2f} 383 {x1+12:.2f} 395L{x2+16:.2f} 693Q{x2+8:.2f} 711 {x2:.2f} 693Z'
        flutes.extend([path(d,paint('jade-glass'),stroke='#176D69',stroke_width=1.2,stroke_opacity=.45),path(f'M{x1+2:.2f} 398L{x2+3:.2f} 690',stroke='#D9FFF1',stroke_width=1.8,opacity=.82)])
    a.add(group('hand-cut-column-flutes',flutes))
    a.add(group('column-foot-mouldings',[
        ellipse(512,712,126,29,paint('jade-glass'),stroke='#B7FFE9',stroke_width=2),
        ellipse(512,701,122,27,paint('frost')),ellipse(512,692,112,25,paint('jade-cross')),
        path('M404 694Q512 739 620 694',stroke='#E7FFF6',stroke_width=3),
    ]))
    cap='M337 317Q315 306 317 282Q319 261 340 260H684Q705 261 707 282Q709 306 687 317L654 372Q512 400 370 372Z'
    a.add(group('ionic-capital',a.relief(cap,'crystal',dy=9)+[
        path(cap,paint('jade-glass'),stroke='#CFFFF0',stroke_width=3),
        rect(317,251,390,28,paint('frost'),9,stroke='#D3FFF0',stroke_width=2),
        rect(339,280,346,17,paint('jade-cross'),5),
        path('M387 335Q512 384 637 335L617 374Q512 404 407 374Z',paint('jade-cross')),
    ]))
    ovals=[]
    for i in range(13):
        x=391+i*20
        ovals.extend([ellipse(x,337,6.7,14,'none',stroke='#247B71',stroke_width=2,opacity=.6),path(f'M{x-4} 333Q{x} 320 {x+4} 333',stroke='#D9FFED',stroke_width=1.5,opacity=.85)])
    a.add(group('capital-egg-and-dart',ovals))
    volutes=[]
    for cx in [365,659]:
        direction=1 if cx==365 else -1
        volutes.extend([circle(cx,324,55,paint('jade-cross'),stroke='#D6FFEE',stroke_width=2),circle(cx,324,46,paint('jade-glass'))])
        points=[]
        for i in range(161):
            t=i*4.5*math.pi/160
            r=43*(1-i/184)
            points.append((cx+direction*r*math.cos(t),324+r*math.sin(t)))
        d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points)
        volutes.extend([path(d,stroke='#1D6966',stroke_width=6,stroke_linecap='round',opacity=.6),path(d,stroke='#C7FFE8',stroke_width=2,stroke_linecap='round',transform='translate(-1 -2)')])
    a.add(group('carved-spiral-volutes',volutes))
    a.add(group('polished-capital-edges',[
        path('M328 262H694',stroke='#FFFFFF',stroke_width=3,opacity=.83),
        path('M412 374Q512 399 612 374',stroke='#CEFFED',stroke_width=3),
    ]+[line(330,255+i*1.9,694,255+i*1.9,'#3D917E',.6,opacity=.26) for i in range(10)]))

def search(a):
    a.gradient('lens',['#E4FFEF','#A5EEDD','#47BFAA','#116F79'],(270,260,660,662))
    a.gradient('lens-metal',['#E6FFEE','#8FE2CF','#286C75','#E2FFF3','#397B7F'],(235,217,701,706))
    a.gradient('lens-handle',['#216D70','#90DEBD','#D3FFE1','#338C7A','#134F59'],(639,635,770,778))
    a.ground(cx=518,cy=820,rx=348)
    handle='M618 592Q634 579 650 593L804 747Q828 773 804 800Q777 829 750 804L596 650Q582 634 597 618Z'
    a.add(group('magnifier-handle',a.relief(handle,'crystal',dy=12)+[
        path(handle,paint('lens-handle'),stroke='#BEF5D7',stroke_width=2),
        path('M655 627L790 765Q803 778 792 793',stroke='#E1FFE5',stroke_width=4,opacity=.7),
        path('M666 627L627 666M674 635L635 674',stroke=paint('gold'),stroke_width=12),
        path('M671 632L632 671',stroke='#FFF0BC',stroke_width=2),
    ]))
    a.add(fine_hatch(a,path(handle),595,590,823,826,3,'#104C4C',.13,-1))
    a.add(group('lens-mount',[
        circle(457,449,242,'#031D29',opacity=.38,transform='translate(0 18)',filter=paint('soft-shadow')),
        circle(457,459,243,'#205967'),circle(457,449,243,paint('lens-metal'),stroke='#C8FEEB',stroke_width=2),
        circle(457,449,220,'#1F6E76'),circle(457,446,213,paint('lens'),stroke='#BDFFEB',stroke_width=3),
    ]))
    rim=[]
    for i in range(144):
        t=i*math.pi/72
        rim.append(line(457+232*math.cos(t),449+232*math.sin(t),457+239*math.cos(t+.004),449+239*math.sin(t+.004),'#F0FFDF' if i%2 else '#285F61',.9,opacity=.46))
    a.add(group('precision-lens-rim',rim))
    inside=[circle(457,446,204,paint('frost'),opacity=.62)]
    # Magnified courthouse sits physically inside the lens, clipped to glass.
    inside.extend([
        path('M321 416L457 330L593 416Z',paint('silver'),stroke='#FFFFFF',stroke_width=2),
        path('M345 406L457 348L569 406Z',paint('enamel'),opacity=.85),
        rect(316,418,282,18,paint('silver'),4),rect(326,441,262,15,paint('silver'),3),
        rect(313,565,288,19,paint('silver'),4),rect(296,589,322,21,paint('silver'),5),
    ])
    for x in [345,414,483,552]:
        inside.extend([rect(x-14,459,28,103,paint('silver-cross'),4),rect(x-21,454,42,10,paint('silver'),2),rect(x-21,556,42,9,paint('silver'),2)])
        for dx in [-7,0,7]:
            inside.extend([line(x+dx,469,x+dx,548,'#4A858A',1.2,opacity=.7),line(x+dx+2,469,x+dx+2,548,'#FFFFFF',1,opacity=.85)])
    inside.extend([circle(457,386,17,paint('gold')),path('M450 387L455 392L466 379',stroke='#74602B',stroke_width=3,stroke_linecap='round',stroke_linejoin='round')])
    a.add(group('magnified-court',inside,clip_path=a.clip(circle(457,446,209,'#FFFFFF'))))
    a.add(group('optical-surface-reflections',[
        path('M277 405Q307 279 439 249Q528 250 586 288Q421 286 277 467Z',paint('shine'),opacity=.68),
        path('M294 549Q327 621 426 641',stroke='#F1FFE5',stroke_width=5,opacity=.77),
        path('M335 278Q461 204 584 278',stroke='#FFFFFF',stroke_width=4,opacity=.73),
        path('M628 552Q666 502 664 444',stroke='#ACFFDC',stroke_width=3,opacity=.86),
        circle(457,446,199,'none',stroke='#FFFFFF',stroke_width=1,opacity=.24),
    ]))

DESIGNS = [
    ('main','01-balance','Balance',balance,('#F8F4E9','#DADDD2'),('#15342F','#061C22'),'#58BDB2','Bronze balance with linked suspension chains, engraved metal, enamel pans and a turned pedestal.'),
    ('main','02-courthouse','Courthouse',court,('#F5F3E9','#D6DDD4'),('#29362F','#0B191C'),'#9DC5B0','A domed courthouse in carved sandstone, with ribbed roof, fluted columns, arched windows and layered steps.'),
    ('main','03-verdict','Verdict',gavel,('#F5F1EA','#DAD7CE'),('#30313A','#101520'),'#BFB4A1','Walnut gavel with curved wood grain, machined brass cuffs and a concentric sounding block.'),
    ('main','04-statute','Statute',book,('#FAF1E9','#DFD5C6'),('#39272F','#151722'),'#D7A06E','Burgundy leather law book with foil border, embossed scales, gilt page edges and a silk bookmark.'),
    ('main','05-counsel-seal','Counsel seal',seal,('#F8EFE6','#E4D3C3'),('#35272B','#101823'),'#D89976','Sculpted wax seal with milled bronze rim, guilloche engraving, fountain nib and laurel branches.'),
    ('liquid-glass','01-court-shield','Court shield',shield,('#EFF7FC','#CFDBEB'),('#142D4B','#071020'),'#72DDED','Faceted optical-glass shield with refracted edges, a divided glass face and a raised silver court column.'),
    ('liquid-glass','02-case-docket','Case docket',docket,('#F2F6FB','#D5DCEB'),('#152A45','#0B1121'),'#70E3E4','Layered glass case folders with folded documents, recessed index plaque and polished folder lip.'),
    ('liquid-glass','03-hearing-day','Hearing day',calendar,('#F5F1FC','#DCD8EC'),('#2D2444','#101323'),'#B8A0EE','Lavender glass hearing calendar with steel binder rings, selected date and an inset precision clock.'),
    ('liquid-glass','04-ionic-column','Ionic column',column,('#F1F9F2','#D0E2D8'),('#173B35','#081C25'),'#74DEC1','Carved jade-glass Ionic column with spiral volutes, egg-and-dart capital, eleven flutes and a stepped plinth.'),
    ('liquid-glass','05-court-search','Court search',search,('#F0F8F2','#D2E4D8'),('#173831','#071924'),'#88DFBB','Emerald optical magnifier with a silver courthouse inside the lens, a milled rim and metal-banded handle.'),
]

def build():
    manifest={'format':'SVG','viewBox':'0 0 1024 1024','version':2,'icons':[]}
    for folder,slug,name,draw,light,dark,accent,desc in DESIGNS:
        variants={}
        for is_dark in [False,True]:
            a=Art(slug,name,is_dark,dark if is_dark else light,accent)
            draw(a)
            variant=a.write(folder,desc)
            variants['dark' if is_dark else 'light']=variant
        manifest['icons'].append({'id':slug,'name':name,'collection':folder,'description':desc,'variants':variants})
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    rows=['# eCourts app icons','',
          'Ten distinct designs. Each has its own light and dark SVG. Click any preview to open the editable artwork.','',
          'All icons use a 1024 × 1024 canvas with a full background for launcher masking. Paths, gradients and named layers stay editable; there are no embedded images, external fonts or scripts.','']
    for section,label in [('main','Metal, stone and leather'),('liquid-glass','Glass')]:
        rows.extend([f'## {label}','','| Design | Light | Dark |','| --- | --- | --- |'])
        for item in manifest['icons']:
            if item['collection']!=section: continue
            ls,ds=item['variants']['light'],item['variants']['dark']
            rows.append(f'| **{item["name"]}**<br>{item["description"]} | [<img src="{ls["path"]}" width="180" alt="{item["name"]}, light">]({ls["path"]})<br>{ls["bytes"]/1024:.1f} KiB | [<img src="{ds["path"]}" width="180" alt="{item["name"]}, dark">]({ds["path"]})<br>{ds["bytes"]/1024:.1f} KiB |')
        rows.append('')
    rows.extend(['## Direct SVG links','',
        'Use the paths in [manifest.json](manifest.json). For example:','',
        '- [Balance, light SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/main/icons/01-balance/light.svg)',
        '- [Balance, dark SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/main/icons/01-balance/dark.svg)',
        '- [Court shield, light SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/liquid-glass/icons/01-court-shield/light.svg)',
        '- [Court shield, dark SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/liquid-glass/icons/01-court-shield/dark.svg)','',
        'For a pinned CDN URL, replace `main` in a raw URL with the desired commit SHA.','',
        'These are SVG source assets, not Android VectorDrawable XML. For a native launcher resource, export the chosen source to the required Android bitmap densities; keep the full square background so the launcher can apply its mask.','',
        'Regenerate with `python3 ecourts/source/build_icons.py` from the repository root. The generator uses only the Python standard library.',''])
    (ROOT/'README.md').write_text('\n'.join(rows))
    print(json.dumps({'icons':len(manifest['icons']),'svgs':len(manifest['icons'])*2,'min_bytes':min(v['bytes'] for i in manifest['icons'] for v in i['variants'].values()),'max_bytes':max(v['bytes'] for i in manifest['icons'] for v in i['variants'].values())}))

if __name__=='__main__':
    build()
