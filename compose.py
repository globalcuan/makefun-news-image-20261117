from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = '#f6f1e5'
INK = '#14181f'
RED = '#b3202c'
NAVY = '#1d3557'
TEAL = '#14666b'
GREEN = '#2e6b34'
SAND = '#c9a86a'
ORANGE = '#e07b24'

FONT_PATHS = {
    'serif': ['/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'],
    'bold': ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'],
    'regular': ['/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
}

def font(kind, size):
    for path in FONT_PATHS[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)

def centered(text, y, fnt, fill, xcenter=W//2):
    d.text((xcenter, y), text, font=fnt, fill=fill, anchor='mt')

def wrap(text, fnt, max_width):
    words = text.split()
    lines, line = [], ''
    for word in words:
        candidate = word if not line else line + ' ' + word
        if d.textlength(candidate, font=fnt) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def draw_wrapped(text, xy, fnt, fill, max_width, line_gap=3, max_lines=None):
    x, y = xy
    lines = wrap(text, fnt, max_width)
    if max_lines:
        lines = lines[:max_lines]
    ascent, descent = fnt.getmetrics()
    step = ascent + descent + line_gap
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y

# Masthead
# top rule
d.rectangle((28, 20, 996, 25), fill=RED)
centered('THE WORLD IN ONE DAY', 31, font('serif', 63), INK)
d.rectangle((28, 112, 996, 158), fill=RED)
centered('TUESDAY, 17 NOVEMBER 2026', 116, font('bold', 30), PAPER)
d.line((28, 165, 996, 165), fill=INK, width=2)
d.line((28, 170, 996, 170), fill=INK, width=1)

# Lead illustration panel
px, py, ps = 35, 181, 300
d.rectangle((px, py, px+ps, py+ps), fill=NAVY)
# distant skyline accents
for bx, by, bw, bh in [(48, 334, 34, 72), (91, 354, 40, 52), (240, 346, 33, 60), (277, 360, 42, 46)]:
    d.rectangle((bx, by, bx+bw, by+bh), fill='#294866')
# water
for yy in (435, 448, 461):
    for xx in range(48, 320, 48):
        d.arc((xx, yy-5, xx+35, yy+7), 0, 180, fill='#79b8c3', width=3)
# bridge towers and deck
for tx in (106, 248):
    d.rectangle((tx-9, 248, tx+9, 394), fill='#e7dfc8')
    d.rectangle((tx-16, 244, tx+16, 253), fill='#f6f1e5')
# cables, spans, deck broken portion
for pts in [((106, 258), (142, 282)), ((106, 258), (174, 294)), ((106, 258), (207, 282)), ((248, 258), (215, 282)), ((248, 258), (180, 294)), ((248, 258), (167, 282))]:
    d.line(pts, fill='#f6f1e5', width=3)
d.line((50, 306, 150, 306), fill='#f6f1e5', width=9)
d.line((150, 306, 181, 306), fill='#f6f1e5', width=9)
d.line((202, 306, 304, 306), fill='#f6f1e5', width=9)
# tilted broken segment, dropping toward the water
d.polygon([(177, 302), (201, 306), (190, 334), (167, 326)], fill='#f6f1e5')
d.line((177, 302, 190, 334), fill=RED, width=3)
# explosion starburst
cx, cy = 190, 296
points = []
for i in range(24):
    import math
    a = -math.pi/2 + i*math.pi/12
    r = 34 if i % 2 == 0 else 19
    points.append((cx + math.cos(a)*r, cy + math.sin(a)*r))
d.polygon(points, fill=ORANGE, outline='#ffd67a')
d.ellipse((cx-9, cy-9, cx+9, cy+9), fill='#ffe4a3')

# Lead copy
lx = 361
d.text((lx, 181), 'UKRAINE WAR', font=font('bold', 22), fill=RED)
y = draw_wrapped('UKRAINE BLOWS UP CRIMEAN BRIDGE', (lx, 207), font('serif', 48), INK, 620, line_gap=-1, max_lines=3)
draw_wrapped("Span partly collapses in an 'unprecedented' strike; Russia hits back at Kyiv bridges as the Zaporizhzhia death toll reaches 40", (lx, y+2), font('regular', 21), INK, 620, line_gap=2, max_lines=4)
d.line((28, 488, 996, 488), fill=INK, width=2)

# 2x2 news grid
col_x = [36, 526]
row_y = [503, 667]
cell_w, cell_h = 462, 174
stories = [
    (TEAL, 'US-IRAN WAR', 'TANKER HITS MINE IN HORMUZ', 'Fourth tanker ablaze in 24 hours as the war spreads; Bahrain intercepts Iranian drones aimed at a US radar base', 'ship'),
    (RED, 'DIPLOMACY', 'XI, TRUMP AND PUTIN TO MEET', 'First-ever trilateral summit set for Thursday in Shenzhen, on the sidelines of APEC', 'flags'),
    (SAND, 'GAZA', 'WEST URGES GAZA CROSSINGS OPEN', 'UK, Canada, Australia and Italy demand rapid aid access; 1.7 million displaced people face a winter emergency', 'aid'),
    (GREEN, 'CLIMATE — COP31', 'COP31 DRAFT: FASTER FOSSIL PHASE-OUT', 'Antalya text seeks an accelerated phase-out and $120bn a year in climate finance by 2035', 'climate'),
]

def icon_base(x, y, color):
    d.rectangle((x, y, x+92, y+92), fill=color)

def draw_icon(kind, x, y, color):
    icon_base(x, y, color)
    if kind == 'ship':
        # waves and mine
        for yy in (y+78, y+85):
            d.arc((x+5, yy-5, x+43, yy+5), 0, 180, fill='#b8e0df', width=2)
            d.arc((x+48, yy-5, x+87, yy+5), 0, 180, fill='#b8e0df', width=2)
        d.polygon([(x+11,y+60),(x+76,y+60),(x+65,y+73),(x+23,y+73)], fill='#14181f')
        d.rectangle((x+28,y+42,x+61,y+60), fill='#f6f1e5')
        d.rectangle((x+38,y+31,x+53,y+42), fill='#f6f1e5')
        d.rectangle((x+51,y+26,x+59,y+39), fill=ORANGE)
        mx, my = x+77, y+49
        for i in range(12):
            import math
            a = i*math.pi/6
            d.line((mx+math.cos(a)*5,my+math.sin(a)*5,mx+math.cos(a)*12,my+math.sin(a)*12), fill=INK, width=2)
        d.ellipse((mx-5,my-5,mx+5,my+5), fill=INK)
    elif kind == 'flags':
        fx = [x+6, x+34, x+62]
        for xx in fx:
            d.line((xx,y+15,xx,y+75), fill='#f6f1e5', width=2)
        d.rectangle((x+8,y+18,x+31,y+50), fill='#b3202c')
        d.ellipse((x+12,y+21,x+17,y+26), fill='#f4d35e')
        d.rectangle((x+36,y+18,x+61,y+50), fill='#f6f1e5')
        for yy in (20,26,32,38,44): d.rectangle((x+36,yy+y-18,x+61,yy+y-15), fill=RED)
        d.rectangle((x+36,y+18,x+47,y+32), fill=NAVY)
        d.rectangle((x+64,y+18,x+87,y+28), fill='#f6f1e5')
        d.rectangle((x+64,y+28,x+87,y+39), fill=NAVY)
        d.rectangle((x+64,y+39,x+87,y+50), fill=RED)
    elif kind == 'aid':
        d.polygon([(x+12,y+60),(x+43,y+27),(x+74,y+60)], fill='#f6f1e5')
        d.rectangle((x+18,y+60,x+68,y+76), fill='#dfd3b5')
        d.rectangle((x+48,y+48,x+81,y+75), fill='#fffdf5', outline=INK, width=1)
        d.rectangle((x+61,y+52,x+67,y+71), fill=RED)
        d.rectangle((x+55,y+58,x+74,y+64), fill=RED)
    elif kind == 'climate':
        d.ellipse((x+59,y+10,x+81,y+32), fill='#f7d76a')
        for a in range(0,360,45):
            import math
            r1,r2=15,22
            d.line((x+70+math.cos(math.radians(a))*r1,y+21+math.sin(math.radians(a))*r1,x+70+math.cos(math.radians(a))*r2,y+21+math.sin(math.radians(a))*r2), fill='#f7d76a', width=2)
        d.ellipse((x+16,y+29,x+67,y+78), fill='#f6f1e5')
        d.polygon([(x+19,y+72),(x+47,y+30),(x+63,y+49),(x+41,y+75)], fill='#9fc778')
        d.line((x+27,y+68,x+51,y+43), fill=GREEN, width=3)

for (color,kicker,headline,sub,kind), x, y in zip(stories, [col_x[0],col_x[1],col_x[0],col_x[1]], [row_y[0],row_y[0],row_y[1],row_y[1]]):
    draw_icon(kind, x, y+27, color)
    tx = x+105
    d.text((tx,y), kicker, font=font('bold', 17), fill=RED)
    hy = draw_wrapped(headline, (tx,y+21), font('serif', 27), INK, 350, line_gap=-1, max_lines=2)
    draw_wrapped(sub, (tx,hy+1), font('regular', 16), INK, 350, line_gap=1, max_lines=3)
    if x == col_x[0]:
        d.line((x, y+cell_h-3, x+cell_w, y+cell_h-3), fill='#8e887c', width=1)

# separator and Japan strip
d.line((28, 845, 996, 845), fill=INK, width=2)
# Japan roundel and jet
jx,jy=39,857
d.ellipse((jx,jy,jx+60,jy+60), fill='#fffdf8', outline=INK, width=1)
d.ellipse((jx+18,jy+18,jx+42,jy+42), fill=RED)
d.polygon([(jx+65,jy+31),(jx+90,jy+22),(jx+81,jy+31),(jx+91,jy+38),(jx+67,jy+35),(jx+62,jy+43)], fill=NAVY)
d.text((145, 852), 'JAPAN SCRAMBLES JETS AS RUSSIAN JETS VIOLATE ITS AIRSPACE', font=font('serif', 25), fill=INK)
d.text((145, 889), 'Tokyo protests after Russian aircraft enter airspace over waters near Fukuoka', font=font('regular', 19), fill=INK)
d.line((28, 925, 996, 925), fill=INK, width=2)

# Bottom ticker and footer
d.rectangle((0, 927, 1024, 989), fill=INK)
ticker = "ALSO ON TUESDAY: US loses measles-free status after 26 years • Houthis advance in Yemen • Depardieu pleads guilty in Paris • Russian military plane crash kills 19"
draw_wrapped(ticker, (28, 932), font('bold', 17), PAPER, 968, line_gap=0, max_lines=2)
centered("The world's news of Tuesday 17 November 2026, summed up in one image", 992, font('regular', 14), INK)

im.save('entry.png', format='PNG', optimize=True)
