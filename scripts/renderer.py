import re
from io import BytesIO
from pathlib import Path

from lxml import etree

SVG_NS = "http://www.w3.org/2000/svg"
# Match both namespaced and bare text/tspan (handles SVGs without default ns)
_TEXT_TAGS = {f"{{{SVG_NS}}}text", f"{{{SVG_NS}}}tspan", "text", "tspan"}


def _inject_font(svg_text: str, font_path: str, family_name: str) -> str:
    # Absolute font path inside url() so browsers/renderers can locate it
    block = f'<style>@font-face{{font-family:"{family_name}";src:url("{font_path}");}}</style>'
    if "</defs>" in svg_text:
        return svg_text.replace("</defs>", block + "</defs>", 1)
    # Self-closing <defs/> — expand it
    if re.search(r"<defs\s*/>", svg_text):
        return re.sub(r"<defs\s*/>", f"<defs>{block}</defs>", svg_text, count=1)
    # No <defs> at all — insert one right after the opening <svg ...> tag
    return re.sub(r"(<svg[^>]*>)", rf"\1<defs>{block}</defs>", svg_text, count=1)


def _replace_in_element(el: etree._Element, replacement: dict) -> None:
    for ph, val in replacement.items():
        if el.text and ph in el.text:
            el.text = el.text.replace(ph, val)
        # tail is text after the closing tag, inside the parent — also needs replacement
        if el.tail and ph in el.tail:
            el.tail = el.tail.replace(ph, val)


def render(
    parsed: dict,
    template_path: str,
    font_path: str,
    out_path: str,
    placeholder_map: dict,
    placeholder_family: str,
) -> None:
    svg_text = Path(template_path).read_text(encoding="utf-8")

    # Step 1: inject @font-face via string op (keeps CSS text out of lxml's escaping path)
    svg_text = _inject_font(svg_text, font_path, placeholder_family)

    # Step 2: lxml parse → walk text/tspan → replace placeholders
    root = etree.fromstring(svg_text.encode("utf-8"))
    replacement = {v: str(parsed.get(k, "")) for k, v in placeholder_map.items()}

    for el in root.iter():
        if el.tag in _TEXT_TAGS:
            _replace_in_element(el, replacement)

    # Step 3: serialize — encoding="unicode" returns str, no XML declaration added
    out_str = etree.tostring(root, encoding="unicode")
    Path(out_path).write_text(out_str, encoding="utf-8")
