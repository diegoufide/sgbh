import html as _h, os, subprocess, sys
BLUE = '#2B338C'; BLUE2 = '#4B53A8'; LIGHT = '#EEF0FA'; GRAY = '#6B7280'; INK = '#1F2340'; ORANGE = '#C2410C'
def e(t): return _h.escape(str(t))
class SVG:
    def __init__(s, w, h):
        s.w, s.h = w, h; s.back = []; s.mid = []; s.front = []
    def rect(s, x, y, w, h, fill='#fff', stroke=BLUE, sw=1.5, rx=6, dash=None, layer='mid'):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        getattr(s, layer).append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(s, x, y, t, size=13, weight='normal', anchor='middle', color=INK, italic=False, layer='front', halo=False):
        st = ' font-style="italic"' if italic else ''
        hl = ' paint-order="stroke" stroke="#fff" stroke-width="4" stroke-linejoin="round"' if halo else ''
        getattr(s, layer).append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}"{st}{hl}>{e(t)}</text>')
    def box(s, x, y, w, h, title, lines=(), fill='#fff', head=BLUE, stereo=None, size=12.5, head_h=None, align='middle', dash=None, title_color='#fff'):
        hh = head_h or (40 if stereo else 28)
        s.rect(x, y, w, h, fill=fill, stroke=head if head else BLUE, dash=dash)
        if head:
            s.mid.append(f'<path d="M{x},{y+6} a6,6 0 0 1 6,-6 h{w-12} a6,6 0 0 1 6,6 v{hh-6} h-{w} z" fill="{head}"/>')
            if stereo:
                s.text(x + w/2, y + 15, f'«{stereo}»', 11, color=title_color, italic=True)
                s.text(x + w/2, y + 32, title, 13.5, 'bold', color=title_color)
            else:
                s.text(x + w/2, y + 19, title, 13.5, 'bold', color=title_color)
        else:
            hh = 6
        ty = y + hh + 18
        for ln in lines:
            if align == 'start':
                s.text(x + 10, ty, ln, size, anchor='start')
            else:
                s.text(x + w/2, ty, ln, size)
            ty += size + 5
    def group(s, x, y, w, h, label, sub=None, fill='#F7F8FC', stroke=BLUE, dash='6 4'):
        s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=10, dash=dash, layer='back')
        s.text(x + 12, y + 20, label, 13.5, 'bold', 'start', color=stroke, layer='back')
        if sub: s.text(x + 12, y + 37, sub, 11.5, anchor='start', color=GRAY, italic=True, layer='back')
    def arrow(s, pts, label=None, dashed=False, both=False, lpos=None, lanchor='middle', color=BLUE, head=True, size=11.5):
        d = 'M' + ' L'.join(f'{x},{y}' for x, y in pts)
        da = ' stroke-dasharray="6 4"' if dashed else ''
        me = ' marker-end="url(#ah)"' if head else ''
        ms = ' marker-start="url(#ahs)"' if both else ''
        s.mid.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6"{da}{me}{ms}/>')
        if label:
            if lpos is None:
                (x1, y1), (x2, y2) = pts[0], pts[1]
                lpos = ((x1 + x2) / 2 + 6, (y1 + y2) / 2 + 4); lanchor = 'start'
            for i, ln in enumerate(label.split('\n')):
                s.text(lpos[0], lpos[1] + i * 14, ln, size, anchor=lanchor, color=INK, italic=True, halo=True)
    def node3d(s, x, y, w, h, title, stereo=None, depth=12, fill='#fff', stroke=BLUE, lines=(), head_fill=None):
        s.back.append(f'<path d="M{x},{y} l{depth},{-depth} h{w} v{h} l{-depth},{depth}" fill="{LIGHT if fill=="#fff" else fill}" stroke="{stroke}" stroke-width="1.4"/>')
        s.back.append(f'<path d="M{x+w},{y} l{depth},{-depth}" stroke="{stroke}" stroke-width="1.4"/>')
        s.back.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        ty = y + 18
        if stereo:
            s.text(x + 10, ty, f'«{stereo}»', 11, anchor='start', italic=True, color=GRAY, layer='back'); ty += 17
        s.text(x + 10, ty, title, 13.5, 'bold', 'start', color=stroke, layer='back'); ty += 18
        for ln in lines:
            s.text(x + 10, ty, ln, 11.5, anchor='start', layer='back'); ty += 15
    def artifact(s, x, y, w, h, name, lines=()):
        s.rect(x, y, w, h, fill='#fff', stroke=BLUE2, sw=1.2, rx=3)
        fx, fy = x + w - 18, y + 6
        s.mid.append(f'<path d="M{fx},{fy} h7 l5,5 v11 h-12 z M{fx+7},{fy} v5 h5" fill="#fff" stroke="{BLUE2}" stroke-width="1"/>')
        s.text(x + 8, y + 15, '«artifact»', 10.5, anchor='start', italic=True, color=GRAY)
        s.text(x + 8, y + 31, name, 12.5, 'bold', 'start')
        ty = y + 46
        for ln in lines:
            s.text(x + 8, ty, ln, 11, anchor='start', color=GRAY); ty += 14
    def package(s, x, y, w, h, name, lines=(), fill='#fff', stroke=BLUE, tab_w=None):
        tw = tab_w or min(w * 0.55, len(name) * 8 + 20)
        s.mid.append(f'<path d="M{x},{y} h{tw} v18 h{w-tw} v{h-18} h{-w} z" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        s.mid.append(f'<path d="M{x},{y+18} h{tw}" stroke="{stroke}" stroke-width="1.4"/>')
        s.text(x + 8, y + 14, name, 12.5, 'bold', 'start', color=stroke)
        ty = y + 37
        for ln in lines:
            s.text(x + 8, ty, ln, 11, anchor='start', color=INK); ty += 14
    def note(s, x, y, w, lines, size=11.5):
        h = 14 + len(lines) * (size + 5)
        s.mid.append(f'<path d="M{x},{y} h{w-12} l12,12 v{h-12} h{-w} z" fill="#FFF8E6" stroke="#C2410C" stroke-width="1.1"/>')
        ty = y + 18
        for ln in lines:
            s.text(x + 9, ty, ln, size, anchor='start', color='#7C2D12'); ty += size + 5
    def svg(s):
        defs = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
                f'<marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{s.w}" height="{s.h}" font-family="Arial, Helvetica, sans-serif">' + defs +
                ''.join(s.back) + ''.join(s.mid) + ''.join(s.front) + '</svg>')
    def render(s, out_png):
        base = os.path.splitext(out_png)[0]
        with open(base + '.html', 'w', encoding='utf-8') as f:
            f.write('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}</style></head><body>' + s.svg() + '</body></html>')
        here = os.path.dirname(os.path.abspath(__file__))
        subprocess.run([sys.executable, os.path.join(here, 'render.py'), base + '.html', out_png, str(s.w + 40), str(s.h + 40), '1000'], check=True)
