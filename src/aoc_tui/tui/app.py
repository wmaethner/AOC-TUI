from art import text2art
from textual import events
from textual.app import App
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.keys import Keys
from textual.message import Message
from textual.widgets import Button, Footer, Header, Label, Static

from aoc_tui.core.aoc_app import AOCApp
from aoc_tui.core.aoc_year import AOCYear
from aoc_tui.tui.components.title import Title
from aoc_tui.tui.screens.component_tester import ComponentTester
from aoc_tui.tui.screens.year_screen import YearScreen


class YearDetails(Static):
    def __init__(self, year: AOCYear):
        super().__init__()
        self.year = year

    def compose(self):
        yield Static(f"Stars: {self.year.stars}")
        yield Static(f"Completed Days: {self.year.completed_days}")
        yield Static(f"Started Days: {self.year.days_started}")


class YearDisplay(Static):
    def __init__(self, year: AOCYear):
        super().__init__()
        self.year = year
        self.can_focus = True

    def compose(self):
        yield Static(f"Year: {self.year.year}", classes="box title", expand=True)
        yield YearDetails(self.year)


class AOCTuiApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("c", "comp_tester", "Component Tester"),
    ]
    CSS_PATH = "css/app.tcss"

    def __init__(self, app: AOCApp):
        super().__init__()
        self.aoc_app = app
        # self.load_years()

    def load_years(self):
        self.aoc_app._find_years()
        self.recompose()

    def compose(self):
        yield Header()
        yield Footer()
        yield Title("AOC TUI")
        for year in self.aoc_app.get_year_objects():
            yield YearDisplay(year)

    def on_mount(self) -> None:
        self.load_years()

    def on_key(self, event: events.Key) -> None:
        if isinstance(self.focused, YearDisplay):
            if event.key == Keys.Enter:
                self.push_screen(YearScreen(self.focused.year))

    def action_comp_tester(self):
        self.push_screen(ComponentTester())

    def action_quit(self):
        self.exit()
