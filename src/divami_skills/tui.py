from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from rich.align import Align
from rich.console import RenderableType
from rich.style import Style
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Footer, Header, Label

from . import manager

# ── Color palette — muted, professional ──────────────────────────────────────
# Each LLM: (display_name, top_bg, global_bg, local_bg, global_icon, local_icon)
_P = {
    "claude":  ("Claude",         "#3c6aa8", "#284a78", "#163150", "#8bb7ef", "#5f8bc0"),
    "codex":   ("Codex",          "#33805a", "#215438", "#123523", "#82c49b", "#559d74"),
    "gemini":  ("Gemini",         "#9a7d35", "#6c5620", "#47390f", "#e0bf6e", "#aa8a4a"),
    "copilot": ("Github Copilot", "#71439f", "#4a2c6b", "#2b1840", "#b48cdc", "#7f5aa9"),
}

_WHITE = "white"
_DIM   = "#c0c0c0"

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
        return Text(f" {name} ", style=Style(bgcolor=l_bg, color="#e0e0e0", bold=True))


def _sub_cell(llm_name: str) -> Text:
    """Second header row — Global / Local label."""
    _, _, g_bg, l_bg, *_ = _palette(llm_name)
    if not manager.is_local(llm_name):
        return Text(" Global ", style=Style(bgcolor=g_bg, color=_WHITE, bold=True))
    else:
        return Text(" Local  ", style=Style(bgcolor=l_bg, color="#e0e0e0", bold=True))


def _icon_cell(status: str, llm_name: str) -> RenderableType:
    _, _, _, _, g_icon, l_icon = _palette(llm_name)
    color = g_icon
    if status == "full_symlink":
        return Align.center(Text("●", style=Style(color=color, bold=True), justify="center"))
    elif status == "global_symlink":
        return Align.center(Text("◎", style=Style(color=color), justify="center"))
    elif status == "partial":
        return Align.center(Text("○", style=Style(color=color), justify="center"))
    else:
        return Align.center(Text("·", style=Style(color="#d0d0d0"), justify="center"))


class SkillsApp(App):
    CSS = """
    #help_primary, #help_secondary {
        height: 1;
        padding: 0 1;
        color: #e0e0e0;
    }
    #status {
        height: 1;
        padding: 0 1;
        color: #f0f0f0;
    }
    DataTable {
        height: 1fr;
        color: #f2f2f2;
    }
    #legend {
        width: 52;
        margin-left: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("enter", "toggle", "Expand / Toggle"),
        Binding("space", "toggle", "Expand / Toggle"),
        Binding("t", "view_toggle", "Global / Local"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, cwd: Path | None = None,
                 registry: manager.Registry | None = None):
        super().__init__()
        self._cwd = cwd or Path.cwd()
        self._skill_roots = registry
        self._reg: manager.Registry = {}
        self._llms: dict[str, Path] = {}
        self._show_local: bool = True
        self._skillsets: list[str] = []
        self._expanded: set[str] = set()
        self._rows: list[RowMeta] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Label("", id="help_primary")
            yield Label("", id="help_secondary")
            with Horizontal():
                yield DataTable(id="matrix", show_header=False)
                yield DataTable(id="legend", show_header=True)
            yield Label("", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "divami-skills manager"
        self._build_table()

    def _view_llms(self) -> dict[str, Path]:
        """Return only global or only local LLMs depending on current view."""
        return {n: p for n, p in self._llms.items()
                if manager.is_local(n) == self._show_local}

    def _global_llm_path(self, llm_name: str) -> Path | None:
        if not manager.is_local(llm_name):
            return self._llms.get(llm_name)
        return self._llms.get(_base(llm_name))

    def _desired_full_status(self) -> str:
        return "full_symlink"

    def _skill_cell_status(self, llm_name: str, llm_path: Path, skill_name: str) -> str:
        local_kind = manager.install_kind(llm_path, skill_name)
        if local_kind is not None:
            return "full_symlink"
        if manager.is_local(llm_name):
            global_path = self._global_llm_path(llm_name)
            if global_path is not None:
                if manager.install_kind(global_path, skill_name) is not None:
                    return "global_symlink"
        return "none"

    def _skillset_cell_status(self, llm_name: str, llm_path: Path, skillset: str) -> str:
        skills = manager._skills_in(skillset, self._reg)
        if not skills:
            return "none"
        statuses = [self._skill_cell_status(llm_name, llm_path, skill.name) for skill in skills]
        if all(status == "none" for status in statuses):
            return "none"
        first = statuses[0]
        if first != "none" and all(status == first for status in statuses):
            return first
        return "partial"

    # ── Table construction ────────────────────────────────────────────────────

    def _build_table(self, restore_cursor: tuple[int, int] | None = None) -> None:
        self._reg = self._skill_roots if self._skill_roots is not None \
                    else manager.build_registry()
        self._llms = manager.load_all_llms(local_base=self._cwd)
        self._skillsets = manager.discover_skill_sets(self._reg)

        view = self._view_llms()
        view_label = "Local" if self._show_local else "Global"
        self.sub_title = f"[{view_label}]"
        self.query_one("#help_primary", Label).update(
            "Name: ENTER=expand  ·  LLM: ENTER=install/remove"
        )
        self.query_one("#help_secondary", Label).update("T=Global/Local  ·  R=refresh  ·  Q=quit")

        table = self.query_one("#matrix", DataTable)
        legend = self.query_one("#legend", DataTable)
        table.clear(columns=True)
        table.cursor_type = "cell"
        table.zebra_stripes = True
        legend.clear(columns=True)
        legend.cursor_type = "none"
        legend.zebra_stripes = True

        # Hidden column labels (still needed for structure/keys)
        table.add_column("", key="__name__")
        for llm_name in view:
            table.add_column("", key=llm_name)
        legend.add_column("Symbol", key="symbol", width=10)
        legend.add_column("Meaning", key="meaning", width=39)

        self._rows = []

        # ── Row 0: LLM group names ────────────────────────────────────────
        top_row: list[str | Text] = [Text("")]
        for llm_name in view:
            top_row.append(_top_cell(llm_name))
        table.add_row(*top_row, key="__top__")
        self._rows.append(RowMeta(kind="header"))
        legend.add_row("Controls", "T = switch local/global view", height=None)
        legend.add_row("", "R = rebuild the matrix from disk", height=None)
        legend.add_row("", "Q = quit the TUI", height=None)
        legend.add_row("", "", height=None)
        legend.add_row("●", "Installed locally in this repo for this LLM", height=None)
        legend.add_row("◎", "Installed only in the global location for this LLM", height=None)
        legend.add_row("○", "Partially installed from this skill-set for this LLM", height=None)
        legend.add_row("·", "Not installed in this repo for this LLM", height=None)

        # ── Row 1: Global / Local labels ──────────────────────────────────
        sub_row: list[str | Text] = [Text("Skill / Set", style="bold dim")]
        for llm_name in view:
            sub_row.append(_sub_cell(llm_name))
        table.add_row(*sub_row, key="__sub__")
        self._rows.append(RowMeta(kind="header"))

        # ── Data rows ─────────────────────────────────────────────────────
        for skillset in self._skillsets:
            expanded = skillset in self._expanded
            prefix = "▼  " if expanded else "▶  "

            cells: list[str | Text] = [prefix + skillset]
            for llm_name, llm_path in view.items():
                status = self._skillset_cell_status(llm_name, llm_path, skillset)
                cells.append(_icon_cell(status, llm_name))
            table.add_row(*cells, key=f"ss:{skillset}")
            self._rows.append(RowMeta(kind="skillset", skillset=skillset))

            if expanded:
                for skill_path in manager._skills_in(skillset, self._reg):
                    skill_name = skill_path.name
                    cells = [Text(f"    · {skill_name}", style=_DIM)]
                    for llm_name, llm_path in view.items():
                        cells.append(
                            _icon_cell(
                                self._skill_cell_status(llm_name, llm_path, skill_name),
                                llm_name,
                            )
                        )
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

            llm_name = list(self._view_llms().keys())[col_idx - 1]
            llm_path = self._llms[llm_name]
            status = self._skillset_cell_status(llm_name, llm_path, meta.skillset)
            if status == self._desired_full_status():
                manager.unlink(llm_path, meta.skillset, self._reg)
                self._set_status(f"Removed  {meta.skillset}  →  {llm_name}")
            else:
                manager.link(llm_path, meta.skillset, self._reg)
                n = len(manager._skills_in(meta.skillset, self._reg))
                self._set_status(f"Linked {n} skills  {meta.skillset}  →  {llm_name}")

        elif meta.kind == "skill":
            if col_idx == 0:
                return

            llm_name = list(self._view_llms().keys())[col_idx - 1]
            llm_path = self._llms[llm_name]
            status = self._skill_cell_status(llm_name, llm_path, meta.skill)
            if status == self._desired_full_status():
                manager.unlink_skill(llm_path, meta.skill)
                self._set_status(f"Removed  {meta.skill}  →  {llm_name}")
            else:
                manager.link_skill(llm_path, meta.skillset, meta.skill, self._reg)
                self._set_status(f"Linked  {meta.skill}  →  {llm_name}")

        self._build_table(restore_cursor=(row_idx, col_idx))

    def action_view_toggle(self) -> None:
        self._show_local = not self._show_local
        table = self.query_one("#matrix", DataTable)
        self._build_table(restore_cursor=(table.cursor_row, 0))

    def action_refresh(self) -> None:
        table = self.query_one("#matrix", DataTable)
        self._build_table(restore_cursor=(table.cursor_row, table.cursor_column))

    def _set_status(self, msg: str) -> None:
        self.query_one("#status", Label).update(msg)
