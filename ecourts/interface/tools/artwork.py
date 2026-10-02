"""Original eCourts interface geometry. No imported icon-library paths.

24-unit optical grid, rounded joins, open backgrounds. Parts are kept separate
for meaningful component motion and identical SVG / Android construction.
"""
import math

ICONS = {}
def path(d, role='ink', fill=False, motion=None, pivot=(12,12)):
    return dict(d=d, role=role, fill=fill, motion=motion, pivot=list(pivot))
def line(d, motion=None, role='ink', pivot=(12,12)):
    return path(d,role,False,motion,pivot)
def accent(d, motion=None, pivot=(12,12)):
    return path(d,'accent',True,motion,pivot)
def soft(d): return path(d,'soft',True)
def circle(x,y,r):
    return f'M{x-r:g} {y:g}a{r:g} {r:g} 0 1 0 {2*r:g} 0a{r:g} {r:g} 0 1 0 {-2*r:g} 0Z'
def box(x,y,w,h,r=2):
    return f'M{x+r:g} {y:g}H{x+w-r:g}Q{x+w:g} {y:g} {x+w:g} {y+r:g}V{y+h-r:g}Q{x+w:g} {y+h:g} {x+w-r:g} {y+h:g}H{x+r:g}Q{x:g} {y+h:g} {x:g} {y+h-r:g}V{y+r:g}Q{x:g} {y:g} {x+r:g} {y:g}Z'
def polygon(n,r=8.5,cy=12,rot=-90):
    pts=[(12+r*math.cos(math.radians(rot+360*i/n)),cy+r*math.sin(math.radians(rot+360*i/n))) for i in range(n)]
    return 'M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in pts)+'Z'
def icon(id, label, category, meaning, *parts, duration=800, loop=False):
    assert id not in ICONS,id
    assert any(p['motion'] for p in parts),id
    ICONS[id]=dict(id=id,label=label,category=category,motion=meaning,duration=duration,loop=loop,parts=list(parts))

# Legal work and the primary interface.
icon('briefcase','Cases','Court','The clasp seats as the case folio closes.',
    soft(box(3.5,7,17,13,2.5)),line('M8.5 6.5V5Q8.5 3.5 10 3.5H14Q15.5 3.5 15.5 5V6.5'),line(box(3.5,7,17,13,2.5)),line('M4 11.5Q12 15 20 11.5'),accent(box(10.5,11.5,3,4,1),'seat'))
icon('calendar','Calendar','Court','The date tile turns into its selected position.',
    soft(box(3.5,5,17,15,2.5)),line(box(3.5,5,17,15,2.5)),line('M4 9H20M8 3.5V6.5M16 3.5V6.5M7 16.5H8M11.5 16.5H12.5'),accent(box(14.5,11.5,3,3,0.7),'turn',(16,13)))
icon('search','Search','Navigation','The lens inspects a short horizontal range, then returns to centre.',
    line('M15.7 15.7L20.5 20.5'),soft(circle(10.2,10.2,6.4)),line(circle(10.2,10.2,6.4),'scan'),line('M7.3 9.3Q7.8 7.1 10.2 7.1','scan','accent'))
icon('courthouse','Court','Court','Two structural piers seat beneath a fixed roof.',
    accent('M3.5 7.5L12 3.8L20.5 7.5L19.7 9H4.3Z'),line('M3.5 20.2H20.5M5 17.7H19'),line('M7.2 11.7V15.5','seat'),line('M12 11.7V15.5','seat-late'),line('M16.8 11.7V15.5','seat-later'))
icon('scales','Scales','Court','The beam balances once about its central pin.',
    line('M12 4V20M8.5 20H15.5'),line('M5 7H19M6 7L3.5 13H8.5ZM18 7L15.5 13H20.5Z','balance',pivot=(12,7)),accent(circle(12,6.8,1.6)))
icon('gavel','Gavel','Court','The hammer makes one controlled strike above the fixed block.',
    accent(box(12,18.5,8,2,0.8)),line('M5 18L13.5 9.5M9 5.5L12 2.8L19.2 10L16.5 13Z','strike',pivot=(7,16)))
icon('book','Law book','Court','A page opens around the spine.',
    soft('M3.5 5Q8 3.8 12 6Q16 3.8 20.5 5V19Q16 17.8 12 20Q8 17.8 3.5 19Z'),line('M12 6V20M12 6Q8 3.8 3.5 5V19Q8 17.8 12 20'),line('M12 6Q16 3.8 20.5 5V19Q16 17.8 12 20','open',pivot=(12,12)),line('M15 9H18M15 12H18',None,'accent'))
icon('scroll','Legal scroll','Court','The written rule is revealed down the parchment.',
    soft('M6 4H17Q19 4 19 6V18H8V6Q8 4 6 4Z'),line('M6 8H3.5V6A2.5 2.5 0 0 1 8.5 6V18A2.5 2.5 0 0 0 13.5 18H21V19Q21 21 19 21H11M6 3.5H17Q19 3.5 19 6V15'),line('M11.5 8H16M11.5 11.5H16','trace','accent'))
icon('stamp','Court seal','Court','The seal presses onto the signature baseline.',
    line('M5 20.5H19'),accent('M5 16L7 12.8H10V8Q8.5 7 8.5 5.5A3.5 3.5 0 0 1 15.5 5.5Q15.5 7 14 8V12.8H17L19 16V17.5H5Z','press'))
icon('notebook-pen','Case notebook','Court','The pen completes a short note.',
    soft(box(4,3.5,12,17,2)),line('M13 3.5H6Q4 3.5 4 5.5V18.5Q4 20.5 6 20.5H16M2.5 7H5.5M2.5 12H5.5M2.5 17H5.5'),accent('M11 15L12 11L19 4L21 6L14 13Z','write'))
icon('clipboard','Cause list','Court','The listing marks are written beneath the fixed clip.',
    soft(box(4.5,5,15,15.5,2)),line('M8 5H6Q4.5 5 4.5 6.5V19Q4.5 20.5 6 20.5H18Q19.5 20.5 19.5 19V6.5Q19.5 5 18 5H16'),accent(box(8,3.5,8,4,1.5)),line('M8 11H8.1M11 11H16M8 15.5H8.1M11 15.5H16','trace'))
DOCUMENT='M6 3.5H14.5L19.5 8.5V18.5Q19.5 20.5 17.5 20.5H6Q4.5 20.5 4.5 19V5Q4.5 3.5 6 3.5Z'
icon('document','Document','Court','The text is drawn into a folded court document.',soft(DOCUMENT),line(DOCUMENT),accent('M14.5 3.5V8.5H19.5Z'),line('M8 12H16M8 16H13.5','trace'))
icon('folder','Folder','Court','The front flap opens slightly, exposing the filing edge.',
    line('M3.5 9V6Q3.5 4 5.5 4H9L11 6.5H18.5Q20.5 6.5 20.5 8.5'),accent('M3.5 9H20.5L19.3 18.3Q19.1 20 17.5 20H6.5Q4.9 20 4.7 18.3Z','flap',pivot=(12,20)),line('M8 13H16',None,'surface'))
icon('archive','Archive','Court','The archive lid lowers onto the stored records.',line('M5 9V19Q5 20.5 6.5 20.5H17.5Q19 20.5 19 19V9'),accent(box(3.5,4,17,5,1.2),'seat'),line('M9.5 12.5H14.5'))
icon('library','Library','Court','The last volume leans into its shelf position.',line('M3.5 20.5H21M4.5 4H9V18H4.5ZM11 4H14V18H11Z'),accent('M16 5L19 4.5L21 17.5L18 18Z','shelve',pivot=(18,18)))
icon('building','Office','Court','The entrance lifts into an otherwise anchored building.',soft(box(6,3.5,12,17,1.5)),line('M6 20.5V3.5H18V20.5M3.5 20.5H20.5M9 7H10M14 7H15M9 11H10M14 11H15'),accent(box(10,15,4,5.5,0.8),'seat'))
icon('presentation','Presentation','Work','The chart is plotted on the fixed screen.',line('M4 4H20V16H4ZM12 16V20M8 21L12 18L16 21'),line('M7 12L10 9L13 11L17 7','trace','accent'))
icon('handshake','Agreement','Work','The meeting hands join with a small inward movement.',line('M3 7L6 5L10 8M21 7L18 5L13 7L9 11Q10 13 12 11L13 10L18 15L15 18L11 20L5 14L3 15'),accent('M3 8L5.5 7L8.5 13L6 15Z','join-right'),accent('M18.5 7L21 8L18 15L15.5 13Z','join-left'))
icon('graduation','Learning','Work','The mortarboard seats above the curved academic band.',line('M6.5 12V16Q12 20 17.5 16V12M21 10V16'),accent('M2.8 9L12 4.5L21.2 9L12 13.5Z','seat'))
icon('medal','Medal','Work','The medallion settles below its two ribbons.',line('M6 3.5L10 10M18 3.5L14 10M3.5 3.5H8M16 3.5H20.5'),soft(circle(12,15,5.5)),line(circle(12,15,5.5)),accent('M12 11.5L13 13.7L15.5 14L13.7 15.8L14 18.2L12 17L10 18.2L10.3 15.8L8.5 14L11 13.7Z','seat'))

# People. The shared head / shoulder dimensions match profile and party use.
icon('person','Person','People','The identity silhouette resolves above its shoulder line.',line('M4.5 20Q5 14.5 12 14.5Q19 14.5 19.5 20'),accent(circle(12,7.5,3.5),'seat'))
icon('people','Parties','People','The second party joins the primary person.',line('M3 20Q3.5 14.5 9.5 14.5Q15.5 14.5 16 20'),accent(circle(9.5,7.5,3.5)),line('M16 5Q20 5.5 20 8.5Q20 11.5 17 12M18 15Q21 16 21 20','join-left'))
icon('contact','Contact','People','The identity mark seats inside the contact card.',line(box(4,5,16,15.5,2)),line('M8 3V6M16 3V6M8 17Q12 13.5 16 17'),accent(circle(12,10.5,2.5),'seat'))
icon('glasses','Glasses','People','The second lens aligns with the bridge.',line('M3.5 13L5 6H8M20.5 13L19 6H16M10 14Q12 12 14 14'),line(box(3.5,12,6.5,6,2.5)),line(box(14,12,6.5,6,2.5),'align','accent'))
icon('ear','Hearing','People','The inner hearing contour is revealed.',line('M5.5 9A6.5 6.5 0 0 1 18.5 9Q18.5 12 15.5 14L13 18Q12 20.5 9.5 20.5Q6.5 20.5 6.5 17'),line('M9 9Q9 6 12 6Q15 6 15 9Q15 11 12 12L10.5 15','trace','accent'))
icon('accessibility','Accessibility','People','The open arms extend around a stable centre.',accent(circle(12,4.5,2)),line('M12 9V14M8.5 20L12 14L15.5 20'),line('M5 8L12 10L19 8','extend','accent',pivot=(12,10)))
icon('baby','Baby','People','The small curl uncurls above the face.',line('M5 8Q4 11 4.5 14Q6 20 12 20Q18 20 19.5 14Q20 11 19 8M8 12H8.1M16 12H16.1M9.5 16Q12 17.5 14.5 16'),line('M6 6Q11 1.5 16 5Q18 8 14 8Q11.5 8 12 5.5','trace','accent'))
icon('standing','Standing person','People','The torso rises into a composed standing position.',accent(circle(12,4.5,2)),line('M7 10L12 8.5L17 10M12 9V14M8.5 21L12 14L15.5 21','seat'))
icon('footprints','Footprints','People','One footprint follows the other by a small step.',accent('M5 3.5Q8 2.5 8 6V12H4.5V8Q3 6 5 3.5Z'),line('M4.5 15H8V18Q6 20 4.5 18Z'),accent('M16 7.5Q19 6.5 19 10V16H15.5V12Q14 10 16 7.5Z','step'),line('M15.5 19H19V20Q17 22 15.5 20Z','step'))
icon('hand','Hand','People','The fingers open gently at the wrist.',line('M8 12V5.5Q8 4 9.5 4Q11 4 11 5.5V10M11 6V3.8Q11 2.5 12.5 2.5Q14 2.5 14 4V10M14 6Q14 4.5 15.5 4.5Q17 4.5 17 6V11M17 8Q20 7 20 10V14Q20 20.5 13 20.5Q9 20.5 7 18L3.5 13.5Q2.5 12 4 11.5Q5 11 8 14','open',pivot=(13,20)),accent('M11 17H16V18.5H11Z'))
icon('care','Care','People','A heart seats above the supporting palm.',line('M3 17L7 14H12Q14 14 14 16H10M14 16L19 12Q21 12 20.5 14L16 19H8L5 21'),accent('M12 11L7.5 7Q5 3.5 8.5 3.5Q10.5 3.5 12 5.5Q13.5 3.5 15.5 3.5Q19 3.5 16.5 7Z','seat'))
icon('brain','Thinking','People','The central connection is traced between two hemispheres.',line('M11.5 5Q7 1.5 5.5 6Q2.5 7 4 11Q1.5 15 5 17Q5 22 11.5 19V5ZM12.5 5Q17 1.5 18.5 6Q21.5 7 20 11Q22.5 15 19 17Q19 22 12.5 19V5Z'),line('M6.5 9L9 11V15M17.5 9L15 11V15','trace','accent'))
icon('eye','Visible','People','The pupil checks left and right while the eyelid remains still.',line('M3 12Q7 5.5 12 5.5Q17 5.5 21 12Q17 18.5 12 18.5Q7 18.5 3 12Z'),accent(circle(12,12,3),'scan'))
for id,label,mouth in [('smile','Smile','M8 14Q12 18 16 14'),('laugh','Laugh','M7.5 13.5H16.5Q16 18 12 18Q8 18 7.5 13.5Z')]:
    icon(id,label,'People','The expression opens briefly within a steady face.',line(circle(12,12,8.5)),line('M8 9H8.1M16 9H16.1'),line(mouth,'expression','accent',pivot=(12,14)))
icon('theatre','Theatre','People','The theatrical mask inclines from its top edge.',line('M3.5 6Q12 10 20.5 6V12Q20.5 18 12 21Q3.5 18 3.5 12Z','incline',pivot=(12,6)),line('M7 11L9 12M15 12L17 11M8.5 15Q12 18 15.5 15',None,'accent'))
icon('crown','Crown','People','The central jewel seats in the crown.',line('M4 8L8 11L12 4L16 11L20 8L18 18H6ZM7 21H17'),accent('M12 12L14 14L12 16L10 14Z','seat'))
icon('shield','Verified','People','The verification mark completes inside an anchored shield.',soft('M12 3L20 6V11Q20 17 12 21Q4 17 4 11V6Z'),line('M12 3L20 6V11Q20 17 12 21Q4 17 4 11V6Z'),line('M8 12L11 15L16.5 9','trace','accent'))

# Shape identities. Accent segments are integral to the silhouettes.
STAR='M12 3.5L14.5 8.8L20.5 9.5L16.2 13.6L17.3 19.7L12 16.8L6.7 19.7L7.8 13.6L3.5 9.5L9.5 8.8Z'
icon('star','Star','Shapes','The upper point resolves while the star outline remains recognizable.',line(STAR),accent('M12 3.5L14.5 8.8L12 11L9.5 8.8Z','seat'))
icon('star-filled','Starred','States','The selected star fills from its central axis.',accent(STAR,'select'),line(STAR))
HEART='M12 20Q3.5 14 3.5 8.5Q3.5 4 7.5 4Q10.5 4 12 7Q13.5 4 16.5 4Q20.5 4 20.5 8.5Q20.5 14 12 20Z'
icon('heart','Heart','Shapes','The heart completes its contour once.',soft(HEART),line(HEART,'trace','accent'))
for id,label,n,rot in [('diamond','Diamond',4,-90),('hexagon','Hexagon',6,-30),('triangle','Triangle',3,-90),('pentagon','Pentagon',5,-90),('octagon','Octagon',8,-22.5)]:
    d=polygon(n,8.3,12,rot);icon(id,label,'Shapes','The perimeter is drawn once around the identity shape.',soft(d),line(d,'trace'),accent(circle(12,12,1.6)))
for id,label,d in [('circle','Circle',circle(12,12,8)),('square','Square',box(4,4,16,16,3))]:
    icon(id,label,'Shapes','The perimeter closes around its central accent.',soft(d),line(d,'trace'),accent(circle(12,12,1.6)))
icon('infinity','Infinity','Shapes','One continuous stroke resolves the two connected loops.',line('M12 12C8 5 3.5 6 3.5 11C3.5 17 8 18 12 12C16 6 20.5 6 20.5 12C20.5 18 16 18 12 12Z','trace','accent'))
icon('orbit','Orbit','Shapes','The orbital arc is established around the fixed centre.',accent(circle(12,12,2.5)),line('M7 5Q17 0 20 10Q24 19 13 21Q3 22 3.5 12','trace'),accent(circle(5,6.5,1.8)))
icon('atom','Atom','Shapes','The intersecting orbital paths are traced without spinning the symbol.',accent(circle(12,12,1.8)),line('M4 5C8 1 24 17 20 20C16 24 0 9 4 5ZM20 5C16 1 0 17 4 20C8 24 24 9 20 5Z','trace'))
icon('asterisk','Asterisk','Shapes','The vertical stroke extends from the intersection.',line('M5.5 8L18.5 16M5.5 16L18.5 8'),line('M12 4V20','extend','accent'))
icon('sparkle','Sparkle','Shapes','The four-point facet is drawn into place.',soft('M12 3.5L14.5 9.5L20.5 12L14.5 14.5L12 20.5L9.5 14.5L3.5 12L9.5 9.5Z'),line('M12 3.5L14.5 9.5L20.5 12L14.5 14.5L12 20.5L9.5 14.5L3.5 12L9.5 9.5Z','trace','accent'))
icon('gem','Gem','Shapes','The cut facets resolve inside the gemstone.',line('M3 9L7 4H17L21 9L12 21Z'),line('M3 9H21M8 9L12 21L16 9M8 9L10 4M16 9L14 4','trace','accent'))
icon('ribbon','Ribbon','Shapes','The award tails unfold beneath the seal.',line(circle(12,8,4.5)),accent('M8 12L5.5 20L10 18L12 21L13 14Z','unfold',pivot=(12,12)),line('M16 12L18.5 20L14 18'))
icon('flag','Flag','Shapes','The attached flag opens from the pole.',line('M5 3.5V21'),accent('M5 4H19L16 8L19 12H5Z','open',pivot=(5,8)))
icon('trophy','Trophy','Shapes','The cup seats above the fixed stem.',line('M12 15V20M8 21H16M5.5 5H3.5V8Q3.5 11 7 11M18.5 5H20.5V8Q20.5 11 17 11'),accent('M6 3.5H18V8Q18 15 12 15Q6 15 6 8Z','seat'))

# Nature identities.
icon('leaf','Leaf','Nature','The midrib is traced from stem to tip.',soft('M4 17Q2 4 20 3.5Q22 21 7 19Z'),line('M4 17Q2 4 20 3.5Q22 21 7 19Z'),line('M3.5 21L15.5 8M9 15H15','trace','accent'))
icon('pine','Pine','Nature','The upper branch tier grows along the trunk.',line('M12 16V21M4 18L8 12H5.5L10 6'),accent('M12 3L18.5 12H16L20 18H12Z','grow',pivot=(12,18)))
icon('tree','Tree','Nature','The canopy opens above the rooted trunk.',line('M12 13V21M8.5 21H15.5M12 17L8 14'),accent('M7 16Q2 15 4 10Q3.5 6 8 6Q10 1 14 4Q19 2.5 20 8Q23 13 18 16Z','grow',pivot=(12,16)))
icon('flower','Flower','Nature','Four petals open around a fixed centre.',line('M12 14V21M12 18L17 15'),line('M12 8C4-1 1 10 8 12C-1 17 11 23 12 16C17 25 24 14 16 12C24 7 15-1 12 8Z','bloom',pivot=(12,12)),accent(circle(12,12,2.5)))
icon('sprout','Sprout','Nature','The paired leaves unfold around their stem.',line('M12 11V21'),accent('M12 13Q3 14 3.5 6Q11 5.5 12 13Z','open',pivot=(12,13)),line('M12 11Q12 3 20.5 3.5Q21 11 12 11Z','open',pivot=(12,11)))
icon('mountain','Mountain','Nature','The peak ridge is traced above the foothills.',soft('M3 20L10 5L16 16L19 11L22 20Z'),line('M3 20L10 5L16 16L19 11L22 20Z'),line('M7 11L10 12.5L12.5 10','trace','accent'))
icon('sun','Light theme','Nature','The rays extend around a stable warm disc.',accent(circle(12,12,4)),line('M12 2.8V5M12 19V21.2M2.8 12H5M19 12H21.2M5.5 5.5L7 7M17 17L18.5 18.5M5.5 18.5L7 17M17 7L18.5 5.5','rays'))
icon('moon','Dark theme','Nature','The crescent contour is revealed without rotating the moon.',accent('M18.5 15.5Q11 16 8.5 10Q7 6.5 9.5 3.5Q2.5 5.5 3.5 13Q4.5 21 12.5 20.5Q17 20 18.5 15.5Z'),line('M18.5 15.5Q11 16 8.5 10Q7 6.5 9.5 3.5','trace'))
icon('cloud','Cloud','Nature','The cloud contour grows from its flat horizon.',soft('M6.5 18Q2.5 18 2.5 14Q2.5 10 7 10Q7 3 13 4Q18 4 18.5 10Q22 10.5 21.5 14.5Q21 18 17.5 18Z'),line('M6.5 18Q2.5 18 2.5 14Q2.5 10 7 10Q7 3 13 4Q18 4 18.5 10Q22 10.5 21.5 14.5Q21 18 17.5 18Z','trace'))
icon('rainbow','Rainbow','Nature','The inner rainbow band follows the outer arch.',line('M3.5 19V13A8.5 8.5 0 0 1 20.5 13V19M7 19V13A5 5 0 0 1 17 13V19'),line('M10.5 19V13A1.5 1.5 0 0 1 13.5 13V19','trace','accent'))
icon('snowflake','Snowflake','Nature','The crystalline branches are traced from the centre.',line('M12 3V21M4.2 7.5L19.8 16.5M4.2 16.5L19.8 7.5'),line('M9 4L12 7L15 4M9 20L12 17L15 20M4 10L7 10V7M20 14H17V17','trace','accent'))
icon('flame','Flame','Nature','The inner flame rises within the stable outer silhouette.',line('M11 3Q10 9 6 12Q2 17 7 20Q12 23 17 19Q22 14 16 8Q16 12 13 12Q15 7 11 3Z'),accent('M11 13Q6 19 12 20Q17 19 13 15L12 17Z','rise'))
icon('droplet','Water drop','Nature','A short reflection travels down the water drop.',soft('M12 3.5Q4.5 11.5 4.5 15A7.5 6 0 0 0 19.5 15Q19.5 11.5 12 3.5Z'),line('M12 3.5Q4.5 11.5 4.5 15A7.5 6 0 0 0 19.5 15Q19.5 11.5 12 3.5Z'),line('M8 13Q6.5 17 10 18','trace','accent'))
icon('waves','Waves','Nature','The centre wave crosses a small horizontal interval.',line('M3 6Q6 9 9 6T15 6T21 6M3 18Q6 21 9 18T15 18T21 18'),line('M3 12Q6 15 9 12T15 12T21 12','drift','accent'))
icon('wind','Wind','Nature','The wind stroke resolves into its curled end.',line('M3 8H13Q18 8 17 4Q16 1.5 13.5 4M3 16H11Q16 16 15 20Q14 22 12 20'),line('M3 12H18Q23 12 21 8','trace','accent'))
icon('earth','Earth','Nature','The land contour is traced across a still planet.',line(circle(12,12,8.5)),line('M5 6.5L9 8L9.5 12L13 13L11 18L13 20M17 5.5L15 9L18 11L20 10','trace','accent'))
icon('sunrise','Sunrise','Nature','The sun rises behind the horizon.',line('M3 17H21M5 20.5H19M4.5 10L6.5 12M12 3V6M19.5 10L17.5 12'),accent('M7 17A5 5 0 0 1 17 17Z','rise'))
icon('eclipse','Eclipse','Nature','The obscured disc reveals its remaining crescent.',line(circle(12,12,8.5)),accent('M12 3.5A8.5 8.5 0 0 0 12 20.5Q4.5 12 12 3.5Z','open',pivot=(12,12)))

# Animal profile identities. Limited facial detail keeps 24px silhouettes legible.
icon('cat','Cat','Animals','One ear inclines as the face remains steady.',line('M5 10L4 4L9 7Q12 5.5 15 7L20 4L19 10Q23 20 12 21Q1 20 5 10Z'),line('M8 13H8.1M16 13H16.1M10 17L12 18L14 17'),accent('M4.5 5L8 7.5L5.5 9Z','ear',pivot=(5.5,9)))
icon('dog','Dog','Animals','The floppy ear settles beside the muzzle.',line('M7 6Q12 3 17 6L19 15Q19 21 12 21Q5 21 5 15Z'),line('M7 6L4 4L2.5 11Q2.5 14 6 13'),accent('M17 6L20 4L21.5 11Q21.5 14 18 13Z','ear',pivot=(17,6)),line('M8.5 12H8.6M15.5 12H15.6M10 16L12 18L14 16Z'))
icon('bird','Bird','Animals','The wing folds once against the resting bird.',line('M3 18L8 8Q10 4 13 7Q14 2.5 18 4Q21 5 20 10Q20 18 12 18ZM10 18V21M15 18V21M20 7L22 8L20 9'),accent('M8 10Q15 8 14 13Q12 16 6 16Z','wing',pivot=(9,11)),line('M17 7H17.1'))
icon('fish','Fish','Animals','The tail propels one short, restrained stroke.',line('M7 12Q13 2 21 12Q13 22 7 12ZM15.5 7Q13.5 12 15.5 17M18 11.5H18.1'),accent('M7 12L3 7V17Z','tail',pivot=(7,12)))
icon('rabbit','Rabbit','Animals','One long ear inclines at its base.',line('M8 11Q4 3 7 3Q10 3 11 10M10 10Q19 7 20 14Q22 16 19 17Q18 21 12 21Q5 21 5 16Q5 12 8 11Z'),accent('M13 10Q12 2 15 2Q18 2 16 10Z','ear',pivot=(14,10)),line('M16.5 13.5H16.6M9 18H13'))
icon('squirrel','Squirrel','Animals','The curled tail tightens once beside the body.',line('M11 13Q9 7 14 7L17 4V9Q22 12 18 15Q15 16 17 20H10Q7 20 8 16M17 11H17.1'),line('M8 17Q2 18 3 9Q4 2 8 4Q12 6 7 9Q4 11 7 13','trace','accent'))
icon('turtle','Turtle','Animals','The head extends beyond a fixed shell.',line('M4 15Q3 6 11 6Q19 6 18 15ZM6 15V19M15 15V19M8 7L10 11L7 15M10 11H15'),accent('M18 11H20Q23 13 20 15H18Z','peek'))
icon('snail','Snail','Animals','The feeler extends as the spiral remains still.',line('M3 20H16Q21 20 21 15V9M19 6L21 9L23 6'),soft(circle(10,13,7)),line('M10 13Q7 11 7 14Q8 18 12 16Q17 14 13 9Q7 4 4 10Q0 19 10 20','trace','accent'))
icon('ladybird','Ladybird','Animals','The wing seam opens slightly about the head.',line('M7 9L4 7M17 9L20 7M6 14H3M18 14H21M7 18L4 21M17 18L20 21M9 6Q9 2.5 12 2.5Q15 2.5 15 6'),accent('M12 7Q6 7 6 13Q6 21 12 21Z','open',pivot=(12,7)),line('M12 7Q18 7 18 13Q18 21 12 21V7M15 12H15.1M15 17H15.1'))
icon('paw','Paw','Animals','The central paw pad lands beneath the four toe pads.',line(circle(5.5,10,2)+circle(10,5.5,2)+circle(15,5.5,2)+circle(19,10,2)),accent('M7 16Q12 8 17 16Q21 22 12 20Q3 22 7 16Z','press'))
icon('mouse','Mouse','Animals','The thin tail uncurls from the resting body.',line('M7 12Q5 5 10 5Q13 5 12 10Q15 6 18 10L21 15L17 17H7Q3 15 7 12ZM17 12H17.1'),line('M7 17Q2 18 4 21H14','trace','accent'))
icon('worm','Worm','Animals','The last segment follows a short crawling movement.',line('M4 6Q7 2 10 6Q12 9 10 12Q8 16 12 18Q16 20 19 16'),accent(circle(18.5,16,2.5),'crawl'),line('M6 8L8 9M6 13L9 14M10 20L11 18'))
icon('feather','Feather','Animals','The quill is traced through the tapered vane.',soft('M6 17Q3 9 12 4Q19 1 20 6Q23 13 10 18Z'),line('M6 17Q3 9 12 4Q19 1 20 6Q23 13 10 18Z'),line('M3 21L16 8M9 15H15','trace','accent'))
icon('shell','Shell','Animals','The fan ribs unfold from the shell hinge.',line('M12 21L3.5 11Q2.5 7 6 5Q8 2 12 4Q16 2 18 5Q21.5 7 20.5 11Z'),line('M12 21L7 7M12 21V6M12 21L17 7','trace','accent'))

# Everyday identities and communication.
icon('clock','Clock','Everyday','The minute hand advances through a small interval and settles.',line(circle(12,12,8.5)),line('M12 6.5V12L16 14','clock','accent',pivot=(12,12)))
icon('alarm','Alarm','Everyday','The paired alarm bells rock once on their mounts.',line(circle(12,13,7)),line('M12 9V13L15 15M7 19L5 21M17 19L19 21'),accent('M3 7L6.5 3.5L8 5L4.5 8.5Z','ring',pivot=(6,6)),accent('M16 5L17.5 3.5L21 7L19.5 8.5Z','ring-late',pivot=(18,6)))
icon('timer','Timer','Everyday','The timing hand advances without moving the dial.',line(circle(12,13.5,7.5)),accent(box(9,2.5,6,2,0.7)),line('M12 13.5L15.5 9.5','clock','accent',pivot=(12,13.5)))
icon('watch','Watch','Everyday','The watch hand settles on its time mark.',line(box(6.5,6,11,12,3)),line('M8.5 6L9.5 2.5H14.5L15.5 6M8.5 18L9.5 21.5H14.5L15.5 18'),line('M12 9V12L14.5 13.5','clock','accent'))
icon('calculator','Calculator','Everyday','The display resolves above a fixed keypad.',line(box(5,3,14,18,2.5)),accent(box(8,6,8,4,0.8),'extend'),line('M8.5 13.5H8.6M12 13.5H12.1M15.5 13.5H15.6M8.5 17H8.6M12 17H12.1M15.5 17H15.6'))
icon('chart','Chart','Everyday','The chart line plots from left to right.',line('M4 4V20H21M8 16V18M13 13V18M18 8V18'),line('M7 11L11 7L15 9L20 4','trace','accent'))
icon('pie-chart','Pie chart','Everyday','The separate sector seats in the chart.',line('M10 4A8.5 8.5 0 1 0 20 14H10Z'),accent('M13 3V11H21A8 8 0 0 0 13 3Z','sector'))
icon('checklist','Checklist','Everyday','The first completed item is checked off.',line('M12 6H20M12 12H20M12 18H20M4 12H7M4 18H7'),line('M3 5L5 7L8 3.5','trace','accent'))
icon('mail','Mail','Everyday','The envelope flap closes about its top fold.',soft(box(3.5,5.5,17,13,2)),line(box(3.5,5.5,17,13,2)),line('M4 7L12 13L20 7','flap','accent',pivot=(12,6)))
icon('message','Message','Everyday','The short message is written inside its bubble.',line('M6 4.5H18Q20.5 4.5 20.5 7V15Q20.5 17.5 18 17.5H10L5 21V17.5Q3.5 17.5 3.5 15V7Q3.5 4.5 6 4.5Z'),line('M7.5 9H16.5M7.5 13H13','trace','accent'))
icon('phone','Phone','Everyday','The receiver inclines once from its lower end.',line('M4 3.5H8L10 8L7.5 10Q9.5 15 14 16.5L16 14L20.5 16V20Q13 23 7 17Q1 11 4 3.5Z','answer',pivot=(18,18)),accent('M4 3.5H8L10 8L6 9Z'))
icon('video','Video','Everyday','The lens aperture opens beside the body.',line(box(3.5,6,11.5,12,2.5)),accent('M15 10L21 6.5V17.5L15 14Z','open',pivot=(15,12)))
icon('megaphone','Megaphone','Everyday','The sound lines extend beyond the horn.',line('M4 10L17 5V17L4 14ZM6 15L8 21H11L10 16'),line('M20 7L22 6M20 11H22M20 15L22 16','trace','accent'))
icon('bell','Notifications','Everyday','The bell swings about its crown and returns to rest.',line('M9.5 20Q12 22 14.5 20'),accent('M5 17L7 13V9Q7 4 12 4Q17 4 17 9V13L19 17Z','ring',pivot=(12,5)),line('M12 2.5V4'))
icon('key','Key','Everyday','The key tooth turns into alignment with the shaft.',line(circle(7.5,8,4)),line('M10.5 11L20 20M15 15L17 13M18 18L20 16','unlock','accent',pivot=(10.5,11)))
icon('lock','Private','Everyday','The shackle seats into the anchored lock body.',soft(box(5,10,14,11,2.5)),line(box(5,10,14,11,2.5)),line('M8 10V7Q8 3 12 3Q16 3 16 7V10','seat','accent'),line('M12 14V17'))

# Travel identities.
icon('compass','Compass','Travel','The needle finds north and settles.',line(circle(12,12,8.5)),accent('M16.5 7.5L14 14L7.5 16.5L10 10Z','balance',pivot=(12,12)))
icon('pin','Place','Travel','The location pin seats on its map point.',line('M8 21H16'),line('M12 19Q4.5 12 5 8Q5.5 3 12 3Q18.5 3 19 8Q19.5 12 12 19Z','seat'),accent(circle(12,9,2.5),'seat'))
icon('map','Map','Travel','The final map panel opens from its fold.',line('M3.5 6L9 3.5L15 6L20.5 3.5V18L15 20.5L9 18L3.5 20.5ZM9 3.5V18M15 6V20.5'),accent('M15 6L20.5 3.5V18L15 20.5Z','open',pivot=(15,12)))
icon('route','Route','Travel','The route is drawn between its fixed endpoints.',accent(circle(5,5,2)),line(circle(19,19,2)),line('M9 5H16Q21 5 20 9Q20 12 15 12H9Q3 12 4 16Q4 19 15 19','trace'))
icon('globe','Globe','Travel','The meridian is traced inside the fixed globe.',line(circle(12,12,8.5)),line('M3.5 12H20.5'),line('M12 3.5Q4.5 12 12 20.5Q19.5 12 12 3.5Z','trace','accent'))
icon('plane','Plane','Travel','The aircraft advances a short distance along its heading.',line('M3 20H10'),accent('M4 13L10 11L8 4L11 3L15 9L20 7Q22 7 21 10L16 13L17 19L14 20L12 15L7 17Z','fly'))
icon('car','Car','Travel','The body settles onto two fixed wheels.',line('M5 18V21M19 18V21'),line('M3.5 16V12L6.5 5H17.5L20.5 12V18H3.5ZM4 12H20M7 15H8M16 15H17','seat'),accent('M7.5 7H16.5L18 10H6Z'))
icon('bike','Bicycle','Travel','The frame is drawn between anchored wheels.',line(circle(6,16,4)+circle(18,16,4)),line('M6 16L10 8L15 16H6M10 8H16L18 16M15 4H18V7M8 5H11','trace','accent'))
icon('train','Train','Travel','The train front seats above the rails.',line('M8 19L5 22M16 19L19 22'),line(box(5,3,14,16,3),'seat'),accent(box(8,6,8,6,1)),line('M8 16H8.1M16 16H16.1'))
icon('bus','Bus','Travel','The bus body settles on the wheels.',line('M6 19V21M18 19V21'),line(box(4.5,3.5,15,15.5,2.5),'seat'),accent(box(7,6,10,6,0.8)),line('M8 16H8.1M16 16H16.1M12 6V12'))
icon('ship','Ship','Travel','The hull moves through one short swell.',line('M7 11V6H17V11M10 6V3.5H14V6M3 21Q6 18 9 21T15 21T21 21'),accent('M3 13L12 10L21 13L18 18H6Z','swell'))
icon('sailboat','Sailboat','Travel','The sail opens from the mast.',line('M12 3V18M3 18H21L18 21H6Z'),accent('M10 5L3.5 15H10Z','open',pivot=(10,15)),line('M14 7L20 15H14Z'))
icon('rocket','Rocket','Travel','The exhaust extends once beneath the anchored rocket.',line('M9 15Q7 7 17 3Q22 13 13 17ZM9 12L4 13L3 18L8 17M15 16L14 21L19 20L20 15'),accent('M7 17L4 21L9 19Z','exhaust',pivot=(8,17)),line(circle(15,8.5,1.8)))
icon('tent','Tent','Travel','The entrance flap opens around its ridge.',line('M2.5 20L12 4L21.5 20ZM12 4V20'),accent('M12 10L18 20H12Z','open',pivot=(12,15)))
icon('luggage','Luggage','Travel','The telescopic handle rises above the case.',line(box(5,7,14,13,2.5)),line('M8 20V22M16 20V22M9 11V16M15 11V16'),line('M9 7V3H15V7','rise','accent'))
icon('backpack','Backpack','Travel','The front pocket seats on the pack.',line('M7 6Q7 3 12 3Q17 3 17 6M4 11Q4 6 8 6H16Q20 6 20 11V20H4Z'),accent(box(7,12,10,6,1.5),'seat'),line('M10 14.5H14',None,'surface'))
icon('anchor','Anchor','Travel','The arms are traced from the central shaft.',line(circle(12,5,2.5)),line('M12 7.5V21M8 11H16'),line('M3.5 14Q4 21 12 21Q20 21 20.5 14M3.5 14L6 16M20.5 14L18 16','trace','accent'))
icon('waypoints','Waypoints','Travel','The connecting route appears between fixed waypoints.',accent(circle(5,6,2.5)+circle(19,6,2.5)+circle(12,19,2.5)),line('M7.5 6H16.5M6.5 8.5L10.5 16.5M17.5 8.5L13.5 16.5','trace'))

# Interest identities.
icon('music','Music','Interests','The note stem is traced into its joined beam.',accent(circle(6.5,18,3)+circle(17.5,15.5,3)),line('M9.5 18V5L20.5 3V15.5M9.5 8L20.5 6','trace'))
icon('camera','Camera','Interests','The aperture closes slightly and reopens.',line('M3 8H7L9 4H15L17 8H21V20H3Z'),line(circle(12,13.5,4),'aperture','accent',pivot=(12,13.5)))
icon('palette','Palette','Interests','The final paint well seats in the palette.',line('M12 3Q3 3 3 12Q3 21 12 21Q15 21 14 17Q13 14 17 14H19Q22 14 21 10Q20 3 12 3Z'),line('M7 9H7.1M12 6.5H12.1M17 9H17.1'),accent(circle(6.5,14.5,1.5),'seat'))
icon('paintbrush','Paintbrush','Interests','The brush draws a short finishing stroke.',line('M10 13L18 3.5Q20 2.5 21 5L13 15ZM10 13Q4 12 5 17Q6 19 3.5 20.5Q11 22 13 15Z','write'),accent('M4 20Q10 21 11 16L8 15Z'))
icon('pencil-ruler','Drafting','Interests','The pencil makes a short drafting pass beside the fixed ruler.',line('M4 4L8 3L13 20L9 21ZM6 8L9 7M7.5 13L10.5 12'),accent('M14 17L14.5 13L19 3.5L21.5 4.5L17 14Z','write'))
icon('scissors','Scissors','Interests','One blade closes about the central pivot.',line(circle(6,17.5,3)+circle(18,17.5,3)),line('M8 15.5L19 3.5'),line('M16 15.5L5 3.5','snip','accent',pivot=(12,10)))
icon('lightbulb','Lightbulb','Interests','The filament is traced inside the steady bulb.',line('M8 16Q3.5 12 5.5 7Q8 1 14 3Q22 5 19 12L16 16V18H8ZM9 21H15'),line('M12 17V11L9 8M12 11L15 8','trace','accent'))
icon('coffee','Coffee','Interests','The steam rises above a fixed cup.',line('M4 9H16V15Q16 19 10 19Q4 19 4 15ZM16 10H19Q23 13 19 16H16M3 21H18'),line('M8 6Q6 4 8 2M12 6Q10 4 12 2','rise','accent'))
icon('cooking-pot','Cooking pot','Interests','The lid lowers onto the pot.',line('M5 10V17Q5 20 8 20H16Q19 20 19 17V10M2 12H5M19 12H22'),accent('M4 9Q5 5 10 5V3H14V5Q19 5 20 9Z','seat'))
icon('utensils','Utensils','Interests','The cutlery is set down in parallel.',line('M5 3V9Q5 12 8 12Q11 12 11 9V3M8 3V21'),accent('M19 3Q14 5 15 12H18V21H20V3Z','seat'))
icon('apple','Apple','Interests','The leaf unfolds from the fruit stem.',line('M12 8Q7 3 4 9Q1 15 8 21L12 20L16 21Q23 15 20 9Q17 3 12 8ZM12 8V4'),accent('M12 4Q14 0.5 19 2Q18 7 12 4Z','open',pivot=(12,4)))
icon('notebook-tabs','Tabbed notebook','Interests','The current tab pulls outward from the notebook edge.',line(box(4.5,3.5,13,17,1.5)),line('M8 4V20M17.5 5H20V9H17.5M17.5 15H20V19H17.5'),accent('M17.5 10H21V14H17.5Z','peek'))
icon('dumbbell','Training','Interests','The grip lifts a short controlled interval between the plates.',line('M4 8V16M7 5V19M17 5V19M20 8V16'),accent(box(8,10.5,8,3,1),'lift'))
icon('goal','Goal','Interests','The ball seats at the target line.',line('M3 21V4H21V21M3 4L7 8H17L21 4M7 8V17M17 8V17M7 12H17'),accent(circle(12,18.5,2.5),'goal'))
icon('gamepad','Gamepad','Interests','The right control presses once within the stable gamepad.',line('M7 7H17Q20 7 21 13L22 18Q21 21 18 19L15 16H9L6 19Q3 21 2 18L3 13Q4 7 7 7ZM7 10V14M5 12H9'),accent(circle(17,11,1.5),'press'))
icon('headphones','Headphones','Interests','The ear pad adjusts inward beneath the headband.',line('M4 14V11Q4 3 12 3Q20 3 20 11V14'),line(box(3.5,12,4,8,1.5)),accent(box(16.5,12,4,8,1.5),'join-left'))
icon('radio','Radio','Interests','The tuning needle moves to its station.',line('M5 7L18 2M4 7H20V20H4Z'),line(circle(8.5,14,2.5)),line('M14 11H17M14 17H17'),line('M15.5 10V12','tune','accent'))
icon('microphone','Microphone','Interests','The microphone capsule seats within its fixed cradle.',line('M5 11Q5 18 12 18Q19 18 19 11M12 18V21M8 21H16'),accent(box(8,3,8,12,4),'seat'))

# Navigation, data actions and functional states.
icon('case-number','Case number','Court','The numeric bars are written inside a case tab.',line('M6 4H18Q20 4 20 6V18Q20 20 18 20H6Q4 20 4 18V6Q4 4 6 4Z'),line('M10 7L9 17M15 7L14 17M7.5 10H17M7 14H16.5','trace','accent'))
icon('cnr','CNR lookup','Court','The code marker scans within fixed corner brackets.',line('M3.5 8V4H8M16 4H20.5V8M20.5 16V20H16M8 20H3.5V16'),line('M8 9V15M11 8V16M14 9V15M17 8V16','scan','accent'))
icon('fir-search','FIR search','Court','The search lens scans beside the anchored FIR shield.',line('M11 3.5L18 6V10M11 3.5L4 6V11Q4 17 11 20'),line(circle(15,14,4.5),'scan'),accent('M18 17L21 20L19.5 21.5L16.5 18.5Z','scan'))
icon('settings','Settings','Navigation','One adjustment slider moves precisely along its rail.',line('M4 6H20M4 12H20M4 18H20'),accent(box(7,4,3,4,1),'tune'),accent(box(14,10,3,4,1)),accent(box(9,16,3,4,1)))
icon('add','Add','Actions','The vertical addition stroke extends from the intersection.',line('M4.5 12H19.5'),line('M12 4.5V19.5','extend','accent'))
icon('arrow-left','Back','Navigation','The arrowhead leads a small return movement.',line('M5 12H20'),line('M10.5 5.5L4 12L10.5 18.5','back','accent'))
icon('close','Close','Navigation','The second diagonal completes the close mark.',line('M5.5 5.5L18.5 18.5'),line('M18.5 5.5L5.5 18.5','trace','accent'))
icon('more','More actions','Navigation','The centre option responds with a single controlled press.',accent(circle(5,12,1.7)),accent(circle(12,12,1.7),'press'),accent(circle(19,12,1.7)))
for id,label,d,m in [('chevron-right','Next','M9 5.5L15.5 12L9 18.5','forward'),('chevron-left','Previous','M15 5.5L8.5 12L15 18.5','back'),('chevron-up','Collapse','M5.5 15L12 8.5L18.5 15','rise'),('chevron-down','Expand','M5.5 9L12 15.5L18.5 9','seat')]:
    icon(id,label,'Navigation','The directional stroke leads a short movement and returns.',line(d,m,'accent'))
icon('refresh','Refresh','Actions','Two arrows trace the refresh cycle once, with their anchors fixed.',line('M4.5 10Q5 3.5 12 3.5Q17 3.5 19.5 8M19.5 14Q19 20.5 12 20.5Q7 20.5 4.5 16','trace'),accent('M19.5 3.5V9H14Z'),accent('M4.5 20.5V15H10Z'))
TRAY='M4 14V19Q4 20 5 20H19Q20 20 20 19V14'
for id,label,d,m in [('download','Download','M12 3V15M7.5 10.5L12 15L16.5 10.5','download'),('export','Export','M12 15V3M7.5 7.5L12 3L16.5 7.5','upload')]:
    icon(id,label,'Actions','The arrow moves into the tray.' if id=='download' else 'The arrow leaves the tray and returns to its resting position.',line(TRAY),line(d,m,'accent'))
icon('import','Import','Actions','An incoming arrow enters the open file boundary.',line('M10 3.5H18Q20 3.5 20 5.5V18.5Q20 20.5 18 20.5H10'),line('M3 12H15M10 7L15 12L10 17','forward','accent'))
icon('link','Link','Actions','The connector is traced between two stable link ends.',line('M9 15L7.5 16.5Q3 20 3 15.5Q3 14 5 12L8 9M15 9L16.5 7.5Q21 4 21 8.5Q21 10 19 12L16 15'),line('M8.5 15.5L15.5 8.5','trace','accent'))
icon('share','Share','Actions','The two delivery connections are drawn from the source node.',accent(circle(5,12,2.5)),line(circle(19,5,2.5)+circle(19,19,2.5)),line('M7.5 11L16.5 6M7.5 13L16.5 18','trace','accent'))
icon('note','Private note','Court','A short note is written above the turned corner.',line('M5 3.5H19V15L13.5 20.5H5ZM13.5 20.5V15H19'),line('M8 8H16M8 11.5H14','trace','accent'))
icon('tag','Label','Actions','The label seats against its small punched anchor.',line('M4 4H12L21 13L13 21L4 12Z'),accent(circle(8,8,1.6)),line('M11 11L15.5 15.5','trace','accent'))
icon('check','Confirm','States','The check is written from its short lead stroke.',line('M4.5 12L9.5 17L20 6.5','trace','accent'))
icon('warning','Needs attention','States','The attention mark extends inside a fixed warning outline.',soft('M12 3.5L21 20H3Z'),line('M12 3.5L21 20H3Z'),line('M12 9V13.5','extend','accent'),accent(circle(12,17,0.8)))
for id,label,d in [('info','Information','M12 10V17M12 7H12.1'),('help','Help','M9 8Q9 5 12 5Q16 5 15 9L12 12V13M12 17H12.1')]:
    icon(id,label,'States','The information mark is drawn inside its fixed boundary.',line(circle(12,12,9)),line(d,'trace','accent'))
icon('display','System theme','Settings','The display division is revealed inside the monitor.',line(box(3.5,4.5,17,12,2)),line('M12 16.5V20M8 21H16'),accent('M12 7H18V14H12Z','open',pivot=(12,10)))
icon('filter','Filter','Actions','One filter knob moves along its guide.',line('M4 6H20M6 12H18M9 18H15'),accent(box(13,4,3,4,1),'tune'),accent(box(8,10,3,4,1)))
icon('sort','Sort','Actions','The ordered rows resolve from longest to shortest.',line('M4 6H15M4 12H12M4 18H9','trace'),line('M19 5V19M16 16L19 19L22 16',None,'accent'))
icon('stop','Stop','Actions','The stop face seats within its open boundary.',line(box(3.5,3.5,17,17,4)),accent(box(8,8,8,8,1.5),'press'))
icon('trash','Remove','Actions','The bin lid lifts from a stable hinge then closes.',line('M6 8L7 20H17L18 8M10 11V17M14 11V17'),line('M4 6H20M9 6V3.5H15V6','lid','accent',pivot=(5,6)))
icon('edit','Edit','Actions','The pencil writes a short diagonal stroke.',line('M4 20.5H20'),accent('M5 16L6 11.5L16 2.5L20.5 7L10.5 16Z','write'),line('M14 4.5L18.5 9'))
icon('copy','Copy','Actions','The front sheet separates briefly from its source.',line('M15 3H5Q3 3 3 5V16'),soft(box(8,7,13,14,2)),line(box(8,7,13,14,2),'copy','accent'))
icon('wifi','Network','Settings','The network arcs are revealed outward from the fixed origin.',accent(circle(12,19,1.5)),line('M8 15Q12 11.5 16 15M5 11Q12 5 19 11M2 7Q12-1 22 7','trace'))
icon('history','History','Court','The time hand returns along a brief past interval.',line('M4 9A8.5 8.5 0 1 1 4 16M3.5 4V10H9'),line('M12 7V12L16 14','rewind','accent',pivot=(12,12)))
icon('print','Print','Actions','The printed page advances from the fixed printer.',line('M7 7V3H17V7M6 17H3.5V8H20.5V17H18M17 10.5H17.1'),accent(box(7,13,10,8,0.8),'paper'),line('M9.5 16H14.5',None,'surface'))
icon('loading','Working','States','Three short bars advance in sequence; use only while work is active.',line('M6 16V8','work-a','accent'),line('M12 16V8','work-b','accent'),line('M18 16V8','work-c','accent'),duration=1200,loop=True)
icon('progress','Progress','States','The advancing fill travels along a fixed progress track.',line('M3.5 12H20.5'),line('M5 12H11','progress','accent'),duration=1200,loop=True)
for on in [False,True]:
    icon('checkbox-'+('on' if on else 'off'),'Selected' if on else 'Unselected','Controls','The check is drawn.' if on else 'The selection boundary is drawn once.',line(box(4,4,16,16,3),None if on else 'trace'),line('M7.5 12L10.5 15L16.5 8.5','trace','accent') if on else accent('M5 5H9V6H6V9H5Z','seat'))
    icon('radio-'+('on' if on else 'off'),'Chosen option' if on else 'Available option','Controls','The centre mark seats.' if on else 'The option boundary resolves.',line(circle(12,12,8),None if on else 'trace'),accent(circle(12,12,4),'select') if on else line('M12 4A8 8 0 0 1 20 12',None,'accent'))
    icon('switch-'+('on' if on else 'off'),'Switch on' if on else 'Switch off','Controls','The thumb travels to its resting state without moving the track.',line(box(2.5,6.5,19,11,5.5)),accent(circle(16 if on else 8,12,3.5),'switch-on' if on else 'switch-off'))
icon('transfer','Court transfer','Court','The second transfer arrow follows the first.',line('M3 8H19M15 4L19 8L15 12'),line('M21 16H5M9 12L5 16L9 20','back','accent'))
icon('status-pending','Pending','States','The clock hand marks an active case.',line(circle(12,12,8.5)),line('M12 6V12L16 15','clock','accent'),accent(circle(19,5,2)))
icon('status-disposed','Disposed','States','The completion mark is applied within the case boundary.',line(box(3.5,3.5,17,17,3)),line('M7 12L10.5 15.5L17 8.5','trace','accent'))
icon('status-undated','Date not fixed','States','The open date interval is written beneath the binding.',line(box(3.5,5,17,15,2)),line('M4 9H20M8 3V6M16 3V6'),line('M8 14H16','trace','accent'))
icon('status-error','Fetch error','States','The error mark resolves inside the response boundary.',line(box(3.5,3.5,17,17,3)),line('M8 8L16 16M16 8L8 16','trace','accent'))
icon('court-order','Court order','Court','The order receives its seal after the text is written.',line('M15 20.5H5V3.5H15L19 7.5V12M14.5 3.5V8H19M8 11H14M8 14H12'),accent(circle(17,17,3.5),'press'),line('M15.5 17L17 18.5L19 16',None,'surface'))
icon('fir-document','FIR document','Court','The FIR shield is resolved over its record sheet.',line('M12 20.5H5V3.5H15L19 7.5V10M14.5 3.5V8H19M8 11H11M8 14H10'),line('M17 11L21 13V17Q21 20 17 22Q13 20 13 17V13Z','trace','accent'))
icon('empty-cases','No saved cases','Empty states','The empty filing line is drawn in the open case.',line('M4 9V6H9L11 8H20V20H4Z'),line('M8 14H16','trace','accent'))
icon('empty-search','No search results','Empty states','The empty result bar appears inside the fixed lens.',line(circle(10,10,6.5)),line('M15 15L21 21'),line('M7 10H13','trace','accent'))
icon('empty-calendar','No diary events','Empty states','The empty day marker is written on the calendar.',line(box(3.5,5,17,15,2)),line('M4 9H20M8 3V6M16 3V6'),line('M9 14.5H15','trace','accent'))
icon('empty-orders','No court orders','Empty states','The blank order line resolves beneath the page fold.',line(DOCUMENT),line('M14.5 3.5V8.5H19.5'),line('M8 14H16','trace','accent'))
icon('empty-history','No hearing history','Empty states','The empty timeline segment is drawn between the endpoints.',line('M5 5V19M8 5H18M8 19H18'),accent(circle(5,5,1.5)+circle(5,19,1.5)),line('M11 12H17','trace','accent'))
icon('empty-notes','Save before adding notes','Empty states','The addition mark appears on the unsaved note.',line('M5 3.5H19V16L14.5 20.5H5ZM14.5 20.5V16H19'),line('M8 10.5H16M12 6.5V14.5','trace','accent'))
icon('notification-fetch','Fetching notification','States','The incoming record line seats inside the notification tray.',line('M5 16V21H19V16'),line('M12 3V15M7 10L12 15L17 10','download','accent'))

# Public aliases describe meanings; geometry is stored only once.
ALIASES = {
 'case':'briefcase','calendar-days':'calendar','scale':'scales','landmark':'courthouse','court':'courthouse',
 'book-open':'book','scroll-text':'scroll','clipboard-list':'clipboard','file-text':'document','file':'document','folder-open':'folder',
 'library-big':'library','building-2':'building','graduation-cap':'graduation','user-round':'person','profile':'person','users-round':'people',
 'contact-round':'contact','person-standing':'standing','heart-handshake':'care','venetian-mask':'theatre','shield-check':'shield',
 'tree-pine':'pine','tree-deciduous':'tree','flower-2':'flower','bug':'ladybird','paw-print':'paw','rat':'mouse',
 'alarm-clock':'alarm','chart-no-axes-combined':'chart','chart-pie':'pie-chart','list-checks':'checklist','message-square':'message',
 'key-round':'key','lock-keyhole':'lock','map-pin':'pin','car-front':'car','train-front':'train','bus-front':'bus','tent-tree':'tent',
 'gamepad-2':'gamepad','mic':'microphone','utensils-crossed':'utensils','hash':'case-number','scan':'cnr','shield-search':'fir-search',
 'plus':'add','back':'arrow-left','chevron':'chevron-right','sync':'refresh','system':'display','delete':'trash','network':'wifi',
 'cause-list':'clipboard','parties':'people','orders':'court-order','fir-pdf':'fir-document'
}

if __name__=='__main__':
    print(f'{len(ICONS)} original symbols; {len(ALIASES)} semantic aliases')
