from pathlib import Path
from fasthtml.common import *
from . import manager
SHOW_LOCAL = True
app, rt = fast_app(pico=True)
def panel():
    view = {n: p for n, p in manager.load_all_llms(local_base=Path.cwd()).items() if manager.is_local(n) == SHOW_LOCAL}
    reg = manager.build_registry()
    head = Tr(Th("Skill / Set"), *[Th(n) for n in view])
    rows = [head]
    for skillset in manager.discover_skill_sets(reg):
        cells = [Td(skillset)]
        for llm, path in view.items():
            status = manager.link_status(path, skillset, reg)
            cells.append(Td({"full": "●", "partial": "◎", "none": "·"}[status]))
        rows.append(Tr(*cells))
    return Div(P(f"View: {'Local' if SHOW_LOCAL else 'Global'}"), Button("Toggle local/global", hx_get="/toggle", hx_target="#panel"), Table(Thead(rows[0]), Tbody(*rows[1:])))
@rt("/")
def index():
    return Titled("Divami Skills Web UI", Div(id="panel", hx_get="/panel", hx_trigger="load"))
@rt("/panel")
def panel_route():
    return panel()
@rt("/toggle")
def toggle_route():
    global SHOW_LOCAL
    SHOW_LOCAL = not SHOW_LOCAL
    return panel()
def main():
    serve(appname=__name__)
