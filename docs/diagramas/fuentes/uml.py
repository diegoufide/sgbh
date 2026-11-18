"""Motor mínimo para dibujar diagramas UML en SVG con control total del layout.

Uso: crear Diagram(), agregar clases con posición (x, y) y relaciones con lados de anclaje.
"""
import html, subprocess, os, sys
from PIL import ImageFont

FONT_DIR = '/System/Library/Fonts/Supplemental/'
F = {
    'r': ImageFont.truetype(FONT_DIR + 'Arial.ttf', 13),
    'b': ImageFont.truetype(FONT_DIR + 'Arial Bold.ttf', 14),
    'bi': ImageFont.truetype(FONT_DIR + 'Arial Bold Italic.ttf', 14),
    'i': ImageFont.truetype(FONT_DIR + 'Arial Italic.ttf', 12),
    's': ImageFont.truetype(FONT_DIR + 'Arial.ttf', 12),
}
BLUE = '#2B338C'
LH = 18          # alto de línea de atributos
PADX = 9
HEAD_H = 26

def tw(text, f='r'):
    return F[f].getlength(text)

def esc(t):
    return html.escape(t, quote=True)


class Box:
    def __init__(self, name, x, y, attrs=(), methods=(), stereo=None, abstract=False, kind='class',
                 w=None, ref=False, note=None):
        self.name, self.x, self.y = name, x, y
        self.attrs, self.methods = list(attrs), list(methods)
        self.stereo, self.abstract, self.kind, self.ref = stereo, abstract, kind, ref
        head_lines = 1 + (1 if stereo else 0)
        self.head_h = HEAD_H + (16 if stereo else 0)
        widths = [tw(name, 'bi' if abstract else 'b') + 2 * PADX]
        if stereo:
            widths.append(tw('«%s»' % stereo, 'i') + 2 * PADX)
        for a in self.attrs + self.methods:
            widths.append(tw(a.lstrip('_'), 'r') + 2 * PADX)
        self.w = w or max(widths + [120])
        if ref:
            self.h = self.head_h
        else:
            self.attr_h = max(1, len(self.attrs)) * LH + 8 if (self.attrs or kind != 'enum') else 8
            self.meth_h = (len(self.methods) * LH + 8) if self.methods else (0 if kind == 'enum' else 12)
            self.h = self.head_h + self.attr_h + self.meth_h

    def anchor(self, side, t=0.5):
        if side == 'L': return (self.x, self.y + self.h * t)
        if side == 'R': return (self.x + self.w, self.y + self.h * t)
        if side == 'T': return (self.x + self.w * t, self.y)
        if side == 'B': return (self.x + self.w * t, self.y + self.h)
        raise ValueError(side)

    def svg(self):
        o = []
        x, y, w = self.x, self.y, self.w
        if self.ref:
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{self.h}" rx="2" fill="#F3F4F6" stroke="#6B7280" stroke-dasharray="5 3" stroke-width="1.3"/>')
            ty = y + self.head_h / 2 + 5
            if self.stereo:
                o.append(f'<text x="{x + w/2}" y="{y + 15}" text-anchor="middle" font-size="12" font-style="italic" fill="#374151">«{esc(self.stereo)}»</text>')
                ty = y + 34
            o.append(f'<text x="{x + w/2}" y="{ty}" text-anchor="middle" font-size="14" font-weight="bold" fill="#374151">{esc(self.name)}</text>')
            return '\n'.join(o)
        head_fill = '#4B53A8' if self.kind == 'enum' else BLUE
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{self.h}" fill="#FFFFFF" stroke="{BLUE}" stroke-width="1.4"/>')
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{self.head_h}" fill="{head_fill}" stroke="{BLUE}" stroke-width="1.4"/>')
        ty = y + 18
        if self.stereo:
            o.append(f'<text x="{x + w/2}" y="{ty - 1}" text-anchor="middle" font-size="12" font-style="italic" fill="#FFFFFF">«{esc(self.stereo)}»</text>')
            ty += 16
        style = 'font-style="italic" ' if self.abstract else ''
        o.append(f'<text x="{x + w/2}" y="{ty}" text-anchor="middle" font-size="14" font-weight="bold" {style}fill="#FFFFFF">{esc(self.name)}</text>')
        cy = y + self.head_h
        for i, a in enumerate(self.attrs):
            deco = ''
            if a.startswith('_'):
                deco = ' text-decoration="underline"'; a = a[1:]
            o.append(f'<text x="{x + PADX}" y="{cy + 17 + i * LH}" font-size="13" fill="#111827"{deco}>{esc(a)}</text>')
        cy += self.attr_h
        if self.kind != 'enum' or self.methods:
            o.append(f'<line x1="{x}" y1="{cy}" x2="{x + w}" y2="{cy}" stroke="{BLUE}" stroke-width="1.1"/>')
        for i, m in enumerate(self.methods):
            deco = ''
            txt = m
            if m.startswith('_'):           # estático = subrayado
                deco = ' text-decoration="underline"'
                txt = m[1:]
            if m.startswith('*'):           # abstracto = cursiva
                deco = ' font-style="italic"'
                txt = m[1:]
            o.append(f'<text x="{x + PADX}" y="{cy + 17 + i * LH}" font-size="13" fill="#111827"{deco}>{esc(txt)}</text>')
        return '\n'.join(o)


class Note:
    def __init__(self, x, y, w, lines, h=None):
        self.x, self.y, self.w, self.lines = x, y, w, lines
        self.h = h or (len(lines) * 16 + 16)

    def svg(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        c = 12
        o = [f'<path d="M{x},{y} L{x+w-c},{y} L{x+w},{y+c} L{x+w},{y+h} L{x},{y+h} Z" fill="#FFFBEB" stroke="#B45309" stroke-width="1.2"/>',
             f'<path d="M{x+w-c},{y} L{x+w-c},{y+c} L{x+w},{y+c}" fill="none" stroke="#B45309" stroke-width="1.2"/>']
        for i, l in enumerate(self.lines):
            o.append(f'<text x="{x+8}" y="{y+18+i*16}" font-size="12" fill="#78350F">{esc(l)}</text>')
        return '\n'.join(o)


def _dir(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    return dx / n, dy / n


class Edge:
    """kind: assoc (flecha navegable), line (asociación sin flecha), comp, agg, inh, real, dep."""
    def __init__(self, a, sa, b, sb, kind='assoc', ma=None, mb=None, label=None, ta=0.5, tb=0.5,
                 via=None, mid=None, label_pos=None, ma_off=None, mb_off=None, label_t=None, straight=False,
                 label_side=None, label_anchor=None):
        self.a, self.sa, self.b, self.sb = a, sa, b, sb
        self.kind, self.ma, self.mb, self.label = kind, ma, mb, label
        self.ta, self.tb, self.via, self.mid = ta, tb, via, mid
        self.label_pos, self.ma_off, self.mb_off, self.label_t = label_pos, ma_off, mb_off, label_t
        self.straight, self.label_side, self.label_anchor = straight, label_side, label_anchor

    def points(self):
        p1 = self.a.anchor(self.sa, self.ta)
        p2 = self.b.anchor(self.sb, self.tb)
        if self.via:
            return [p1] + list(self.via) + [p2]
        h1, h2 = self.sa in 'LR', self.sb in 'LR'
        if self.straight:
            if h1 and h2: return [p1, (p2[0], p1[1])]
            if not h1 and not h2: return [p1, (p1[0], p2[1])]
        if h1 and h2:
            mx = self.mid if self.mid is not None else (p1[0] + p2[0]) / 2
            if abs(p1[1] - p2[1]) < 0.5: return [p1, p2]
            return [p1, (mx, p1[1]), (mx, p2[1]), p2]
        if not h1 and not h2:
            my = self.mid if self.mid is not None else (p1[1] + p2[1]) / 2
            if abs(p1[0] - p2[0]) < 0.5: return [p1, p2]
            return [p1, (p1[0], my), (p2[0], my), p2]
        if h1 and not h2:
            return [p1, (p2[0], p1[1]), p2]
        return [p1, (p1[0], p2[1]), p2]

    def svg(self):
        return self.svg_lines() + '\n' + self.svg_texts()

    def svg_lines(self):
        pts = self.points()
        o = []
        dashed = self.kind in ('dep', 'real')
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        dash = ' stroke-dasharray="6 4"' if dashed else ''
        o.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="1.3"{dash}/>')
        # marcador en destino
        end, prev = pts[-1], pts[-2]
        ux, uy = _dir(prev, end)
        px, py = -uy, ux
        if self.kind in ('assoc', 'dep'):
            L, W = 11, 5.5
            b1 = (end[0] - ux * L + px * W, end[1] - uy * L + py * W)
            b2 = (end[0] - ux * L - px * W, end[1] - uy * L - py * W)
            o.append(f'<path d="M{b1[0]:.1f},{b1[1]:.1f} L{end[0]:.1f},{end[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f}" fill="none" stroke="{BLUE}" stroke-width="1.4"/>')
        if self.kind in ('inh', 'real'):
            L, W = 14, 8
            b1 = (end[0] - ux * L + px * W, end[1] - uy * L + py * W)
            b2 = (end[0] - ux * L - px * W, end[1] - uy * L - py * W)
            o.append(f'<path d="M{end[0]:.1f},{end[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f} Z" fill="#FFFFFF" stroke="{BLUE}" stroke-width="1.4"/>')
        # rombo en origen (todo)
        if self.kind in ('comp', 'agg'):
            st, nx = pts[0], pts[1]
            ux2, uy2 = _dir(st, nx)
            px2, py2 = -uy2, ux2
            L, W = 16, 6.5
            m = (st[0] + ux2 * L / 2, st[1] + uy2 * L / 2)
            tip = (st[0] + ux2 * L, st[1] + uy2 * L)
            s1 = (m[0] + px2 * W, m[1] + py2 * W)
            s2 = (m[0] - px2 * W, m[1] - py2 * W)
            fill = BLUE if self.kind == 'comp' else '#FFFFFF'
            o.append(f'<path d="M{st[0]:.1f},{st[1]:.1f} L{s1[0]:.1f},{s1[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} L{s2[0]:.1f},{s2[1]:.1f} Z" fill="{fill}" stroke="{BLUE}" stroke-width="1.3"/>')
        return '\n'.join(o)

    def svg_texts(self):
        pts = self.points()
        o = []
        HALO = 'stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'
        # multiplicidades
        def mult(text, p, q, off):
            ux3, uy3 = _dir(p, q)
            anchor = 'middle'
            if off:
                x, y = p[0] + off[0], p[1] + off[1]
            else:
                dist = 24 if self.kind in ('comp', 'agg') and p == pts[0] else 16
                if abs(uy3) < 0.5:   # segmento horizontal: multiplicidad debajo
                    x = p[0] + ux3 * dist
                    y = p[1] + 15
                else:                # segmento vertical: multiplicidad a la izquierda
                    x = p[0] - 6
                    y = p[1] + uy3 * dist + 4
                    anchor = 'end'
            return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="12" fill="#111827" {HALO}>{esc(text)}</text>'
        if self.ma: o.append(mult(self.ma, pts[0], pts[1], self.ma_off))
        if self.mb: o.append(mult(self.mb, pts[-1], pts[-2], self.mb_off))
        if self.label:
            anchor = 'middle'
            if self.label_pos:
                lx, ly = self.label_pos
                anchor = self.label_anchor or 'middle'
            else:
                # punto medio del segmento más largo
                best, bi = -1, 0
                for i in range(len(pts) - 1):
                    l = abs(pts[i+1][0] - pts[i][0]) + abs(pts[i+1][1] - pts[i][1])
                    if l > best: best, bi = l, i
                t = self.label_t if self.label_t is not None else 0.5
                lx = pts[bi][0] + (pts[bi+1][0] - pts[bi][0]) * t
                ly = pts[bi][1] + (pts[bi+1][1] - pts[bi][1]) * t
                horiz = abs(pts[bi+1][1] - pts[bi][1]) < 0.5
                side = self.label_side or ('above' if horiz else 'right')
                if side == 'above': ly -= 7
                elif side == 'below': ly += 15
                elif side == 'right': lx += 7; anchor = 'start'; ly += 4
                elif side == 'left': lx -= 7; anchor = 'end'; ly += 4
                elif side == 'center': ly += 4
            o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="12" font-style="italic" fill="#1F2937" {HALO}>{esc(self.label)}</text>')
        return '\n'.join(o)


class Diagram:
    def __init__(self, title=None):
        self.boxes, self.edges, self.notes, self.extra = {}, [], [], []
        self.title = title

    def cls(self, name, x, y, attrs=(), methods=(), **kw):
        b = Box(name, x, y, attrs, methods, **kw)
        self.boxes[name] = b
        return b

    def enum(self, name, x, y, literals, **kw):
        return self.cls(name, x, y, literals, (), stereo='enumeration', kind='enum', **kw)

    def ref(self, name, x, y, stereo=None, w=None):
        key = name + '#ref%d' % len(self.boxes)
        b = Box(name, x, y, stereo=stereo, ref=True, w=w)
        self.boxes[key] = b
        return b

    def rel(self, a, sa, b, sb, kind='assoc', **kw):
        A = a if isinstance(a, Box) else self.boxes[a]
        B = b if isinstance(b, Box) else self.boxes[b]
        e = Edge(A, sa, B, sb, kind, **kw)
        self.edges.append(e)
        return e

    def note(self, x, y, w, lines, h=None):
        n = Note(x, y, w, lines, h)
        self.notes.append(n)
        return n

    def svg(self):
        items = list(self.boxes.values()) + self.notes
        W = max(b.x + b.w for b in items) + 30
        H = max(b.y + b.h for b in items) + 30
        for e in self.edges:
            for p in e.points():
                W, H = max(W, p[0] + 40), max(H, p[1] + 40)
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="Arial, Helvetica, sans-serif">',
             f'<rect width="100%" height="100%" fill="#FFFFFF"/>']
        o += self.extra
        for e in self.edges: o.append(e.svg_lines())
        for b in self.boxes.values(): o.append(b.svg())
        for n in self.notes: o.append(n.svg())
        for e in self.edges: o.append(e.svg_texts())
        # etiquetas de aristas por encima de las cajas
        o.append('</svg>')
        return '\n'.join(o), W, H

    def render(self, out_png):
        s, W, H = self.svg()
        base = os.path.splitext(out_png)[0]
        html_path = base + '.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#fff}</style></head><body>' + s + '</body></html>')
        here = os.path.dirname(os.path.abspath(__file__))
        subprocess.run([sys.executable, os.path.join(here, 'render.py'), html_path, out_png, str(int(W) + 40), str(int(H) + 40), '1000'], check=True)
        return W, H
