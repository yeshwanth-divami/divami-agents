from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from rich.style import Style
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Header, Label

from . import manager

# ── Color palette — muted, professional ──────────────────────────────────────
# Each LLM: (display_name, top_bg, global_bg, local_bg, global_icon, local_icon)
_P = {
    "claude":  ("Claude",         "#2c4f82", "#1d3660", "#0f2240", "#6fa0d8", "#456ea0"),
    "codex":   ("Codex",          "#276044", "#1a4430", "#0e2c1e", "#60a07a", "#3d7055"),
    "gemini":  ("Gemini",         "#725e28", "#4e4018", "#322808", "#b89848", "#846e30"),
    "copilot": ("Github Copilot", "#553278", "#391f54", "#221235", "#9068b8", "#624585"),
}

_WHITE = "white"
_DIM   = "#888888"

RowType = Literal["header", "skillset", "skill"]


@dataclass
class RowMeta:
    kind: RowType
    skillset: str = ""
    skill: str | None = None


def _base(llm_name: str) -> str:
    return llm_name.replace("-local", "")


def _palette(llm_name: str) -> tuple:
    return _P[_base(llm_name)]


def _top_cell(llm_name: str) -> Text:
    """First header row — LLM name in both global and local cells of the pair."""
    name, top_bg, _, l_bg, *_ = _palette(llm_name)
    if not manager.is_local(llm_name):
        return Text(f" {name} ", style=Style(bgcolor=top_bg, color=_WHITE, bold=True))
    else:
        return Text(f" {name} ", style=Style(bgcolor=l_bg, color=_DIM))


def _sub_cell(llm_name: str) -> Text:
    """Second header row — Global / Local label."""
    _, _, g_bg, l_bg, *_ = _palette(llm_name)
    if not manager.is_local(llm_name):
        return Text(" Global ", style=Style(bgcolor=g_bg, color=_WHITE))
    else:
        return Text(" Local  ", style=Style(bgcolor=l_bg, color=_DIM))


def _icon_cell(status: str, llm_name: str) -> Text:
    _, _, _, _, g_icon, l_icon = _palette(llm_name)
    color = l_icon if manager.is_local(llm_name) else g_icon
    if status == "full":
        return Text("  ✓  ", style=Style(color=color, bold=True))
    elif status == "partial":
        return Text("  ~  ", style=Style(color=color))
    else:
        return Text("  ·  ", style=Style(color=_DIM))


class SkillsApp(App):
    CSS = """
    #status {
        height: 1;
        padding: 0 1;
        color: $text-muted;
    }
    DataTable {
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("enter", "toggle", "Expand / Toggle"),
        Binding("space", "toggle", "Expand / Toggle"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, cwd: Path | None = None,
                 registry: manager.Registry | None = None):
        super().__init__()
        self._cwd = cwd or Path.cwd()
        self._skill_roots = registry
        self._reg: manager.Registry = {}
        self._llms: dict[str, Path] = {}
        self._skillsets: list[str] = []
        self._expanded: set[str] = set()
        self._rows: list[RowMeta] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield DataTable(id="matrix", show_header=False)
            yield Label("", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "divami-skills manager"
        self.sub_title = (
            "Name col: ENTER=expand  ·  LLM col: ENTER=toggle  ·  R=refresh  ·  Q=quit"
        )
        self._build_table()

    # ── Table construction ────────────────────────────────────────────────────

    def _build_table(self, restore_cursor: tuple[int, int] | None = None) -> None:
        self._reg = self._skill_roots if self._skill_roots is not None \
                    else manager.build_registry()
        self._llms = manager.load_all_llms(local_base=self._cwd)
        self._skillsets = manager.discover_skill_sets(self._reg)

        table = self.query_one("#matrix", DataTable)
        table.clear(columns=True)
        table.cursor_type = "cell"
        table.zebra_stripes = True

        # Hidden column labels (still needed for structure/keys)
        table.add_column("", key="__name__")
        for llm_name in self._llms:
            table.add_column("", key=llm_name)

        self._rows = []

        # ── Row 0: LLM group names ────────────────────────────────────────
        top_row: list[str | Text] = [Text("")]
        for llm_name in self._llms:
            top_row.append(_top_cell(llm_name))
        table.add_row(*top_row, key="__top__")
        self._rows.append(RowMeta(kind="header"))

        # ── Row 1: Global / Local labels ──────────────────────────────────
        sub_row: list[str | Text] = [Text("Skill / Set", style="bold dim")]
        for llm_name in self._llms:
            sub_row.append(_sub_cell(llm_name))
        table.add_row(*sub_row, key="__sub__")
        self._rows.append(RowMeta(kind="header"))

        # ── Data rows ─────────────────────────────────────────────────────
        for skillset in self._skillsets:
            expanded = skillset in self._expanded
            prefix = "▼  " if expanded else "▶  "

            cells: list[str | Text] = [prefix + skillset]
            for llm_name, llm_path in self._llms.items():
                status = manager.link_status(llm_path, skillset, self._reg)
                cells.append(_icon_cell(status, llm_name))
            table.add_row(*cells, key=f"ss:{skillset}")
            self._rows.append(RowMeta(kind="skillset", skillset=skillset))

            if expanded:
                for skill_path in manager._skills_in(skillset, self._reg):
                    skill_name = skill_path.name
                    cells = [Text(f"    · {skill_name}", style=_DIM)]
                    for llm_name, llm_path in self._llms.items():
                        linked = manager.skill_is_linked(llm_path, skill_name)
                        cells.append(_icon_cell("full" if linked else "none", llm_name))
                    table.add_row(*cells, key=f"sk:{skillset}:{skill_name}")
                    self._rows.append(RowMeta(kind="skill", skillset=skillset,
                                              skill=skill_name))

        # ── Status bar ────────────────────────────────────────────────────
        rc_exists = (self._cwd / manager.RC_FILENAME).exists()
        total_skills = sum(len(manager._skills_in(s, self._reg)) for s in self._skillsets)
        rc_note = "" if rc_exists else f"  [no {manager.RC_FILENAME}]"
        self._set_status(
            f"{len(self._skillsets)} skill-set(s) · {total_skills} skills · "
            f"cwd: {self._cwd}{rc_note}"
        )

        if restore_cursor:
            row, col = restore_cursor
            row = min(row, max(0, len(self._rows) - 1))
            table.move_cursor(row=row, column=col)

    # ── Actions ───────────────────────────────────────────────────────────────

    def action_toggle(self) -> None:
        table = self.query_one("#matrix", DataTable)
        row_idx = table.cursor_row
        col_idx = table.cursor_column

        if row_idx >= len(self._rows):
            return

        meta = self._rows[row_idx]

        if meta.kind == "header":
            return

        if meta.kind == "skillset":
            if col_idx == 0:
                if meta.skillset in self._expanded:
                    self._expanded.discard(meta.skillset)
                else:
                    self._expanded.add(meta.skillset)
                self._build_table(restore_cursor=(row_idx, col_idx))
                return

            llm_name = list(self._llms.keys())[col_idx - 1]
            llm_path = self._llms[llm_name]
            status = manager.link_status(llm_path, meta.skillset, self._reg)
            if status in ("full", "partial"):
                manager.unlink(llm_path, meta.skillset, self._reg)
                self._set_status(f"Unlinked all  {meta.skillset}  →  {llm_name}")
            else:
                manager.link(llm_path, meta.skillset, self._reg)
                n = len(manager._skills_in(meta.skillset, self._reg))
                self._set_status(f"Linked {n} skills  {meta.skillset}  →  {llm_name}")

        elif meta.kind == "skill":
            if col_idx == 0:
                return

            llm_name = list(self._llms.keys())[col_idx - 1]
            llm_path = self._llms[llm_name]
            if manager.skill_is_linked(llm_path, meta.skill):
                manager.unlink_skill(llm_path, meta.skill)
                self._set_status(f"Unlinked  {meta.skill}  →  {llm_name}")
            else:
                manager.link_skill(llm_path, meta.skillset, meta.skill, self._reg)
                self._set_status(f"Linked  {meta.skill}  →  {llm_name}")

        self._build_table(restore_cursor=(row_idx, col_idx))

    def action_refresh(self) -> None:
        table = self.query_one("#matrix", DataTable)
        self._build_table(restore_cursor=(table.cursor_row, table.cursor_column))

    def _set_status(self, msg: str) -> None:
        self.query_one("#status", Label).update(msg)
