"""Rebuild the original profile artwork using only Python's standard library."""

from pathlib import Path
from xml.etree import ElementTree


ASSETS = Path(__file__).resolve().parents[1] / "assets"
PALETTES = {
    "dark": ("#091426", "#EAF3FF", "#9FB4CE", "#62D8E4", "#FFAD87", "#223957"),
    "light": ("#ECF3FA", "#17304E", "#48617C", "#007D8C", "#B44F35", "#CADAE8"),
}


def hero(theme: str, compact: bool) -> str:
    base, ink, muted, signal, copper, grid = PALETTES[theme]
    width, height = (640, 320) if compact else (1200, 320)
    margin = 40 if compact else 58
    # A compact composition keeps the name readable on a phone; it isn't a crop.
    field_transform = "translate(155 100) scale(.40)" if compact else "translate(350 -5) scale(.65)"
    name_y, name_size = (105, 56) if compact else (113, 60)
    subtitle_y = 155 if compact else 166
    field = []
    # Floating storage layers, drawn back to front in an isometric projection.
    for index in range(5, -1, -1):
        cy = 145 + index * 31
        color = copper if index == 0 else signal
        top = f"M 920 {cy - 65} 1070 {cy} 920 {cy + 65} 770 {cy} Z"
        side = f"M 770 {cy} v 10 l 150 65 150 -65 v -10 l -150 65 Z"
        field.extend([
            f'<path d="{side}" fill="{color}" fill-opacity=".06" stroke="{color}" stroke-opacity=".45"/>',
            f'<path d="{top}" fill="{base}" fill-opacity=".94" stroke="{color}" stroke-width="1.6"/>',
            f'<path d="M 797 {cy} 920 {cy + 53} 1043 {cy}" fill="none" stroke="{color}" stroke-opacity=".25"/>',
        ])
        for pin in range(6):
            x, y = 819 + pin * 18, cy + 28 + pin * 7.8
            field.append(f'<path d="M {x} {y:.1f} v 4" stroke="{color}" stroke-width="2"/>')
    # A small circuit on the top layer; no monogram or oversized letterform.
    field.append(f'<path d="M 863 145 920 120 977 145 920 170 Z" fill="{copper}" fill-opacity=".09" stroke="{copper}"/>')
    for dx in (-24, 0, 24):
        field.append(f'<path d="M {920 + dx} {120 + abs(dx) * .44} l 32 14 -32 14 -32 -14 Z" fill="none" stroke="{copper}" stroke-opacity=".3"/>')
    wires = [
        "M 650 335 710 361 770 335 830 361",
        "M 684 389 744 415 830 378 870 395",
        "M 1040 308 1100 282 1134 297",
    ]
    highlights = []
    for path in wires:
        field.append(f'<path d="{path}" fill="none" stroke="{signal}" stroke-opacity=".4" stroke-width="1.5"/>')
        highlights.append(f'<path class="packet" pathLength="100" d="{path}" fill="none" stroke="{signal}" stroke-width="3"/>')
    font = "'Trebuchet MS', 'Segoe UI', sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Steven Yang</title>
  <desc id="desc">Systems research and developer tools. Floating isometric storage layers with fine circuit traces and a brief pulse of data.</desc>
  <defs>
    <radialGradient id="pool">
      <stop stop-color="{signal}" stop-opacity=".10"/>
      <stop offset="1" stop-color="{signal}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".8" fill="{grid}"/>
    </pattern>
    <clipPath id="frame"><rect width="{width}" height="{height}" rx="22"/></clipPath>
  </defs>
  <style>
    .packet {{ stroke-dasharray: 5 95; opacity: 0; animation: travel 5s ease-in-out 1 both; }}
    @keyframes travel {{
      0% {{ stroke-dashoffset: 8; opacity: 0; }}
      12% {{ opacity: .8; }}
      84% {{ opacity: .7; }}
      100% {{ stroke-dashoffset: -100; opacity: 0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{ .packet {{ animation: none; opacity: 0; }} }}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{width}" height="{height}" fill="{base}"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    <g transform="{field_transform}">
      <ellipse cx="920" cy="240" rx="250" ry="210" fill="url(#pool)"/>
      <path d="M 680 354 920 458 1160 354 920 250 Z M 800 302 1040 406 M 800 406 1040 302" fill="none" stroke="{grid}" stroke-dasharray="3 7"/>
      {''.join(field)}
      {''.join(highlights)}
      <circle cx="650" cy="335" r="3" fill="{signal}"/>
      <circle cx="1134" cy="297" r="3" fill="{signal}"/>
    </g>
    <g font-family="{font}">
      <text x="{margin}" y="42" fill="{muted}" font-size="16" font-family="'Cascadia Code', Consolas, monospace">/steventimes</text>
      <text x="{margin - 2}" y="{name_y}" fill="{ink}" font-weight="600" font-size="{name_size}" letter-spacing="-1.5">Steven Yang</text>
      <text x="{margin}" y="{subtitle_y}" fill="{ink}" font-size="{23 if compact else 22}">Systems research &amp; developer tools</text>
      <text x="{margin}" y="{subtitle_y + 33}" fill="{muted}" font-size="{17 if compact else 18}">Adaptive storage, data pipelines &amp; AI workflows.</text>
      <path d="M {margin} {height - 62} h 28" stroke="{signal}" stroke-width="2" stroke-linecap="round"/>
      <text x="{margin}" y="{height - 35}" fill="{muted}" font-size="16">Brandeis University</text>
    </g>
    <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="21.5" fill="none" stroke="{grid}"/>
  </g>
</svg>
'''


def pipelines(theme: str, compact: bool) -> str:
    base, ink, muted, signal, copper, grid = PALETTES[theme]
    width, height = (640, 280) if compact else (1200, 230)
    font = "'Trebuchet MS', 'Segoe UI', sans-serif"
    mono = "'Cascadia Code', Consolas, monospace"
    if compact:
        content = f'''
    <text x="32" y="48" fill="{muted}" font-size="22">PYTHON DATA PIPELINES</text>
    <path d="M 32 85 v 118 h 16" fill="none" stroke="{signal}" stroke-width="3"/>
    <text x="56" y="111" fill="{ink}" font-size="30" font-family="{mono}">flow(records)</text>
    <text x="56" y="156" fill="{signal}" font-size="26" font-family="{mono}">.filter(...).map(...)</text>
    <text x="56" y="201" fill="{copper}" font-size="30" font-family="{mono}">.collect(...)</text>
    <text x="32" y="252" fill="{muted}" font-size="23">Read records. Transform. Collect.</text>'''
    else:
        nodes = [
            (32, "flow(records)", "Read records", ink),
            (420, ".filter(...).map(...)", "Filter and transform", signal),
            (808, ".collect(...)", "Collect results", copper),
        ]
        content = f'<text x="32" y="43" fill="{muted}" font-size="18">PYTHON DATA PIPELINES</text>'
        for x, code, label, color in nodes:
            content += f'''
    <rect x="{x}" y="71" width="360" height="83" rx="10" fill="{base}" stroke="{grid}"/>
    <text x="{x + 20}" y="122" fill="{color}" font-size="24" font-family="{mono}">{code}</text>
    <text x="{x + 20}" y="194" fill="{muted}" font-size="20">{label}</text>'''
        for x in (398, 786):
            content += f'<path d="M {x} 112 h 16 m -6 -6 6 6 -6 6" fill="none" stroke="{signal}" stroke-width="2"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">fpstreams: lazy Python pipelines</title>
  <desc id="desc">Illustrative pipeline: read records with flow, filter and map them, then collect results. The ellipses stand for user-defined operations.</desc>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="14" fill="{base}" stroke="{grid}"/>
  <g font-family="{font}">{content}
  </g>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for theme in PALETTES:
        for compact in (False, True):
            suffix = "-compact" if compact else ""
            for name, render in (("hero", hero), ("pipelines", pipelines)):
                svg = render(theme, compact)
                root = ElementTree.fromstring(svg)
                width = 640 if compact else 1200
                height = 320 if name == "hero" else (280 if compact else 230)
                assert root.attrib["width"] == str(width)
                assert root.attrib["height"] == str(height)
                assert root.attrib["viewBox"] == f"0 0 {width} {height}"
                assert "<script" not in svg and "<foreignObject" not in svg
                assert "infinite" not in svg
                if name == "hero":
                    assert "prefers-reduced-motion" in svg
                (ASSETS / f"{name}-{theme}{suffix}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
