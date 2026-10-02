#!/usr/bin/env python3
"""Map two read-only source snapshots; source code is never copied to the CDN.

Usage: python3 tools/audit.py /path/to/icon-audit
The input contains main/, liquid-glass-ui/ and the two recursive tree JSONs.
"""
from pathlib import Path
import re,json,sys,csv,collections
from artwork import ICONS,ALIASES
ROOT=Path(__file__).resolve().parents[1]
SNAPSHOTS={'main':'6a1f600624981355b519fd83a1908637d25afc7c','liquid-glass-ui':'b89473c58878765ac7a139826d6589af104cb07c'}
FUNCTIONS={'MIcon':0,'NativeRow':2,'RoundAction':0,'ActionPill':1,'EmptyState':0,'DetailShortcut':3,'CompactDocumentAction':1,'NativeDestination':2,'CaseSelectionAction':1}
STATES={'Checkbox':['checkbox-off','checkbox-on'],'RadioButton':['radio-off','radio-on'],'EcourtsSwitch':['switch-off','switch-on'],'CircularProgressIndicator':['loading'],'LinearProgressIndicator':['progress'],'ProgressBar':['loading']}
RES={'ic_pdf_back':'arrow-left','ic_pdf_download':'download','ic_pdf_share':'share','ic_pdf_more':'more','ic_pdf_link':'link','ic_pdf_print':'print','ic_fetch_notification':'notification-fetch'}
def norm(s):return s.replace('_','-')
def resolve(s):return ALIASES.get(norm(s),norm(s))
def strings(s):return re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"',s)
def mask(s):
    # Keep positions / line breaks, hide comments and strings while balancing.
    return re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/',lambda m:''.join('\n' if c=='\n' else ' ' for c in m[0]),s)
def calls(s,names):
    m=mask(s)
    for hit in re.finditer(r'\b('+'|'.join(names)+r')\s*\(',m):
        if re.search(r'\b(fun|class)\s*$',m[max(0,hit.start()-20):hit.start()]):continue
        start=hit.end();depth=1;i=start;split=start;args=[]
        while i<len(m) and depth:
            c=m[i]
            if c in '([{':depth+=1
            elif c in ')]}':depth-=1
            if c==',' and depth==1:args.append(s[split:i]);split=i+1
            if depth==0:args.append(s[split:i])
            i+=1
        yield hit[1],hit.start(),args,s[hit.start():i]

def main(source):
    rows=[];renderers=[];exceptions=[];files=[];profile_counts={};defined={};unresolved=[]
    def row(branch,file,line,kind,original,ids,context):
        missing=[x for x in ids if x not in ICONS]
        if missing:unresolved.append([branch,file,line,original,missing])
        rows.append(dict(branch=branch,commit=SNAPSHOTS[branch],file=file,line=line,kind=kind,original=original,replacements=ids,context=context,sourceUrl=f'https://github.com/vigarepo2/eCourts/blob/{SNAPSHOTS[branch]}/{file}#L{line}'))
    for branch,commit in SNAPSHOTS.items():
        root=source/branch
        index=0 if branch=='main' else 1
        tree=json.loads((source/f'tree-{index}.json').read_text())
        assert not tree['truncated']
        for t in tree['tree']:
            p=t['path']
            if t['type']!='blob' or not p.startswith('app/src/main/'):continue
            if not p.endswith(('.kt','.java','.xml')):continue
            f=root/p;assert f.exists(),p
            files.append(dict(branch=branch,path=p,blob=t['sha']))
            s=f.read_text();lines=s.splitlines()
            def ln(pos):return s[:pos].count('\n')+1
            def context(pos):
                fs=list(re.finditer(r'\b(?:fun|void|class)\s+(\w+)',s[:pos]))
                if f.suffix=='.java':
                    fs=list(re.finditer(r'^\s*(?:(?:private|public|protected|static|final|synchronized)\s+)+(?:[\w<>\[\].]+\s+)?(\w+)\s*\(',s[:pos],re.M))
                return fs[-1][1] if fs else f.stem
            if f.name=='NativeProfiles.kt':
                catalog=list(re.finditer(r'ProfileVector\("([^"]+)", "([^"]+)", "([^"]+)"',s))
                profile_counts[branch]=len(catalog)
                for hit in catalog:row(branch,p,ln(hit.start()),'profile-choice',hit[1],[resolve(hit[1])],hit[2]+' / '+hit[3])
                exceptions.append(dict(branch=branch,file=p,line=53,kind='profile-treatment',reason='Five saved paint patterns (solid, split, gradient, diagonal, stripes) are renderer treatments, not five different silhouettes. Preserve the saved preference and apply it to the new mono geometry.'))
            if f.name=='NativeDesign.kt':
                tail=s[s.index('private fun iconPaths'):];offset=s.index('private fun iconPaths');names=[]
                for hit in re.finditer(r'^\s*((?:"[^"]+"\s*,?\s*)+)\s*->',tail,re.M):
                    for name in strings(hit[1]):
                        names.append(name);row(branch,p,ln(offset+hit.start()),'declared-symbol',name,[resolve(name)],'MIcon compatibility name; use records distinguish active use from an available renderer definition.')
                defined[branch]=names
            for fn,pos,args,call in calls(s,list(FUNCTIONS)+list(STATES)+['ProfileGlyph','ProfileBadge']):
                line=ln(pos)
                if fn in STATES:
                    row(branch,p,line,'control-state',fn,STATES[fn],context(pos));continue
                if fn in ['ProfileGlyph','ProfileBadge']:
                    renderers.append(dict(branch=branch,file=p,line=line,renderer=fn,resolution='ProfileVector choices; aliases retain all 140 persisted IDs, with briefcase for a missing preference and scales for an unknown legacy ID.'));continue
                idx=FUNCTIONS[fn];arg=next((a.split('=',1)[1] for a in args if re.match(r'\s*icon\s*=',a)),args[idx] if len(args)>idx and not re.match(r'\s*\w+\s*=',args[idx]) else '')
                if not arg.strip() or arg.strip()=='null':continue
                names=[x for x in strings(arg) if resolve(x) in ICONS]
                if names:
                    ids=list(dict.fromkeys(resolve(x) for x in names))
                    # Semantic context avoids reusing a plain file for distinct
                    # legal concepts and preserves useful empty-state meanings.
                    if fn=='EmptyState':
                        mapping={'briefcase':'empty-cases','search':'empty-search','calendar':'empty-calendar','file':'empty-orders','history':'empty-history','note':'empty-notes'}
                        ids=list(dict.fromkeys(mapping.get(x,resolve(x)) for x in names))
                    if f.name=='NativeFir.kt' and 'file' in names:ids=['fir-document']
                    if fn=='ActionPill' and 'FIR' in call:ids=['fir-document']
                    if fn=='DetailShortcut' and 'Latest order' in call:ids=['court-order']
                    if f.name=='NativeCaseDetails.kt' and fn=='MIcon' and arg.strip()=='"file"':ids=['court-order']
                    row(branch,p,line,'interface-use',', '.join(names),ids,context(pos)+' / '+fn)
                else:
                    renderers.append(dict(branch=branch,file=p,line=line,renderer=fn,expression=arg.strip()[:100],resolution='Resolved by data-source records, wrapper callers or semantic aliases in this inventory.'))
            # Data-driven icons passed through otherwise opaque variables.
            for fn,pos,args,call in calls(s,['Triple']):
                if len(args)>1:
                    names=[x for x in strings(args[1]) if resolve(x) in ICONS]
                    if names:row(branch,p,ln(pos),'action-data',', '.join(names),[resolve(x) for x in names],(strings(args[0]) or ['Case action'])[0])
            if f.name in ['NativeSearch.kt','NativeSettings.kt']:
                for hit in re.finditer(r'val icon = when\s*\([^)]*\)\s*\{([\s\S]*?)\}',s):
                    for pair in re.finditer(r'(?:("[^"]+")|else)\s*->\s*"([^"]+)"',hit[1]):
                        id=resolve(pair[2]);label=(pair[1] or 'else').strip('"')
                        if f.name=='NativeSearch.kt':id={'cause':'clipboard','else':'fir-document'}.get(label,id)
                        row(branch,p,ln(hit.start()+hit[0].index(hit[1])+pair.start()),'icon-data',pair[2],[id],f.stem+' / '+label)
            for hit in re.finditer(r'R\.drawable\.(\w+)',s):
                name=hit[1]
                if name in RES:row(branch,p,ln(hit.start()),'drawable-use',name,[RES[name]],context(hit.start()))
                elif name.startswith('ic_launcher'):exceptions.append(dict(branch=branch,file=p,line=ln(hit.start()),kind='branding',reason='Existing launcher / about-screen brand artwork is explicitly excluded; preserve it.'))
                else:unresolved.append([branch,p,ln(hit.start()),name])
            if '/res/drawable/' in p:
                if f.stem in RES:row(branch,p,1,'drawable-definition',f.stem,[RES[f.stem]],'Bundled resource; ic_pdf_link is available but has no current call site.')
                else:exceptions.append(dict(branch=branch,file=p,line=1,kind='branding',reason='Launcher branding resource: excluded from replacement.'))
            for hit in re.finditer('→',s):row(branch,p,ln(hit.start()),'unicode-symbol','→',['transfer'],'From-court to to-court separator. Keep accessible text; icon is an optional visual replacement.')
            for token in ['StatusPill','nativeStatusColor']:
                for fn,pos,args,call in calls(s,[token]):
                    row(branch,p,ln(pos),'text-status',token,['status-pending','status-disposed','status-undated','status-error','warning'],context(pos)+' / currently text + colour; companion icons are optional, preserve status labels and logic.')
            # Explicit graphic exclusions prevent silent gaps in the audit.
            for i,line in enumerate(lines,1):
                if re.search(r'drawPath\(|drawCircle\(|drawRoundRect\(|drawBitmap\(|drawOutline\(|drawRect\(',line) and f.name not in ['NativeDesign.kt','NativeProfiles.kt']:
                    exceptions.append(dict(branch=branch,file=p,line=i,kind='non-icon-drawing',reason='Surface / backdrop rendering, document page painting or report layout, not an interface symbol; keep in the app renderer.'))
        # Text-only theme/data rows still have a meaningful integration route.
        extra={'NativeSettings.kt':{'Import':'import','Export':'export','Private display':'lock','Animation speed':'settings','Glass finish':'settings'},'NativeCaseDetails.kt':{'Parties & advocates':'people','Processes':'document'},'NativeCalendar.kt':{}}
        for name,mapping in extra.items():
            f=root/'app/src/main/java/in/wikio/ecourts'/name;s=f.read_text()
            for label,id in mapping.items():
                hit=re.search('"'+re.escape(label)+'"',s)
                if hit:row(branch,str(f.relative_to(root)),s[:hit.start()].count('\n')+1,'text-feature',label,[id],'Currently text-only; optional icon for a future app implementation, not an existing icon-bearing control.')
    assert profile_counts=={'main':140,'liquid-glass-ui':140},profile_counts
    assert not unresolved,unresolved
    used={id for r in rows for id in r['replacements']}
    counts=dict(collections.Counter(r['kind'] for r in rows))
    report=dict(sourceRepository='vigarepo2/eCourts',destinationRepository='WikioApps/cdn',snapshots=SNAPSHOTS,profileChoicesPerBranch=profile_counts,uniqueReplacementIcons=len(ICONS),mappedIcons=len(used),records=len(rows),counts=counts,unresolved=unresolved,rows=rows,renderers=renderers,exclusions=exceptions,auditedFiles=files,notes=[
      'All main-source Kotlin, Java and XML files in both recursive Git trees were inspected; no Material Icons imports, web UI, inline SVG UI, or bitmap UI icon pack was found.',
      'The current profile picker embeds Lucide-derived paths. Only the concepts and persisted IDs are mapped; none of those paths are used in the new artwork.',
      'Chevron-bearing text settings rows share the NativeRow trailing renderer. A source occurrence of that renderer covers all such rows; text-only rows are not mislabeled as icon uses.',
      'Unicode arrows denote transfers. Bullets, ellipses, dashes and curly quotes are punctuation or placeholders and remain text.',
      'Compose calendar date cells, radio/check/switch state surfaces, colour/shape preview tiles, PDF page counters and native date pickers retain their semantics and hit targets. Icons are not replacements for complete widgets.',
      'No source from the app repository is published here. Records contain only identifiers, function names, file locations and source links.',
      'Defined-but-unused renderer symbols remain mapped for compatibility; current use is represented separately.'])
    (ROOT/'inventory.json').write_text(json.dumps(report,indent=2)+'\n')
    with (ROOT/'inventory.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,lineterminator='\n',fieldnames=['branch','commit','file','line','kind','original','replacement','context','sourceUrl']);writer.writeheader()
        for r in rows:writer.writerow({k:v for k,v in r.items() if k!='replacements'}|dict(replacement=';'.join(r['replacements'])))
    print(json.dumps(dict(records=len(rows),counts=counts,auditedFiles=len(files),mappedIcons=len(used),catalogIcons=len(ICONS),unmappedCatalog=sorted(set(ICONS)-used),renderers=len(renderers),unresolved=unresolved),indent=2))

if __name__=='__main__':main(Path(sys.argv[1]).resolve())
