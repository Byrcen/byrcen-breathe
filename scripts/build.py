"""把 src/theme.template.css 里的占位符换成纸纹素材，生成仓库根目录的 theme.css。

用法：python3 scripts/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def uri(svg):
    s = svg.replace('%', '%25').replace('#', '%23').replace('"', "'")
    return 'url("data:image/svg+xml;utf8,' + s + '")'


def grain(rgb, a1, a2):
    """纸纹：一层横向的纤维，一层细颗粒，都是 SVG 噪点。"""
    r, g, b = rgb
    svg = ("<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
           f"<filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.018 .55' numOctaves='2' seed='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 {r}  0 0 0 0 {g}  0 0 0 0 {b}  0 0 0 {a1} 0'/></filter>"
           f"<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' seed='7' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 {r}  0 0 0 0 {g}  0 0 0 0 {b}  0 0 0 {a2} 0'/></filter>"
           "<rect width='100%' height='100%' filter='url(#f)'/><rect width='100%' height='100%' filter='url(#n)'/></svg>")
    return uri(svg)


ASSETS = {
    '__GRAIN_LIGHT__': grain((.42, .35, .25), .06, .16),
    '__GRAIN_DARK__': grain((1, 1, 1), .025, .06),
}

text = (ROOT / 'src' / 'theme.template.css').read_text()
for key, value in ASSETS.items():
    text = text.replace(key, value)
assert '__' not in text.replace('--', ''), '模板里还有没替换的占位符'
(ROOT / 'theme.css').write_text(text)
print('theme.css', len(text.encode()), 'bytes')
