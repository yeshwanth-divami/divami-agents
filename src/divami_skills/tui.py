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
    if status == "full_symlink":
        return Text(" ✓* ", style=Style(color=color, bold=True))
    elif status == "full_copy":
        return Text(" ✓✝︎ ", style=Style(color=color, bold=True))
    elif status == "global_symlink":
        return Text(" o* ", style=Style(color=color))
    elif status == "global_copy":
        return Text(" o✝︎ ", style=Style(color=color))
    elif status == "partial":
        return Text("  ~  ", style=Style(color=color))
    else:
        return Text("  ·  ", style=Style(color=_DIM))


class SkillsApp(App):
    CSS = """
    #help_primary, #help_secondary {
        height: 1;
        padding: 0 1;
        color: $text-muted;
    }
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
        Binding("t", "view_toggle", "Global / Local"),
        Binding("m", "mode_toggle", "Copy / Symlink"),
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
        self._use_copy: bool = True
        self._skillsets: list[str] = []
        self._expanded: set[str] = set()
        self._rows: list[RowMeta] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Label("", id="help_primary")
            yield Label("", id="help_secondary")
            yield DataTable(id="matrix", show_header=False)
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

    def _install_kind(self, llm_path: Path, skill_name: str) -> str | None:
        return manager.install_kind(llm_path, skill_name)

    def _desired_full_status(self) -> str:
        return "full_copy" if self._use_copy else "full_symlink"

    def _skill_cell_status(self, llm_name: str, llm_path: Path, skill_name: str) -> str:
        local_kind = self._install_kind(llm_path, skill_name)
        if local_kind == "symlink":
            return "full_symlink"
        if local_kind == "copy":
            return "full_copy"
        if manager.is_local(llm_name):
            global_path = self._global_llm_path(llm_name)
            if global_path is not None:
                global_kind = self._install_kind(global_path, skill_name)
                if global_kind == "symlink":
                    return "global_symlink"
                if global_kind == "copy":
                    return "global_copy"
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
        mode_label = "Copy" if self._use_copy else "Symlink"
        self.sub_title = f"[{view_label}] [{mode_label}]"
        self.query_one("#help_primary", Label).update(
            "Name: ENTER=expand  ·  LLM: ENTER=install/remove"
        )
        self.query_one("#help_secondary", Label).update(
            "T=Global/Local  ·  M=Copy/Symlink  ·  *=symlink  ·  ✝︎=copy  ·  "
            "R=refresh  ·  Q=quit"
        )

        table = self.query_one("#matrix", DataTable)
        table.clear(columns=True)
        table.cursor_type = "cell"
        table.zebra_stripes = True

        # Hidden column labels (still needed for structure/keys)
        table.add_column("", key="__name__")
        for llm_name in view:
            table.add_column("", key=llm_name)

        self._rows = []

        # ── Row 0: LLM group names ────────────────────────────────────────
        top_row: list[str | Text] = [Text("")]
        for llm_name in view:
            top_row.append(_top_cell(llm_name))
        table.add_row(*top_row, key="__top__")
        self._rows.append(RowMeta(kind="header"))

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
                manager.link(llm_path, meta.skillset, self._reg, copy=self._use_copy)
                n = len(manager._skills_in(meta.skillset, self._reg))
                mode = "Copied" if self._use_copy else "Linked"
                self._set_status(f"{mode} {n} skills  {meta.skillset}  →  {llm_name}")

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
                manager.link_skill(llm_path, meta.skillset, meta.skill, self._reg,
                                   copy=self._use_copy)
                mode = "Copied" if self._use_copy else "Linked"
                self._set_status(f"{mode}  {meta.skill}  →  {llm_name}")

        self._build_table(restore_cursor=(row_idx, col_idx))

    def action_view_toggle(self) -> None:
        self._show_local = not self._show_local
        table = self.query_one("#matrix", DataTable)
        self._build_table(restore_cursor=(table.cursor_row, 0))

    def action_mode_toggle(self) -> None:
        self._use_copy = not self._use_copy
        mode = "Copy" if self._use_copy else "Symlink"
        table = self.query_one("#matrix", DataTable)
        self._build_table(restore_cursor=(table.cursor_row, table.cursor_column))
        self._set_status(f"Install mode switched to: {mode}")

    def action_refresh(self) -> None:
        table = self.query_one("#matrix", DataTable)
        self._build_table(restore_cursor=(table.cursor_row, table.cursor_column))

    def _set_status(self, msg: str) -> None:
        self.query_one("#status", Label).update(msg)
