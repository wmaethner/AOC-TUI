from textual.containers import Container
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import RichLog, Static

from aoc_tui.core.aoc_day_part import PartData


class ResultsComponent(Widget):
    results: reactive[list[str]] = reactive([], recompose=True)

    def __init__(self, results: list[str] = []):
        super().__init__()

        self.results = results

    def compose(self):
        yield Static("Results")
        with Container(classes="box"):
            if self.results:
                for result in self.results:
                    yield Static(result)


class LogComponent(Widget):
    def compose(self):
        yield Static("Log")
        yield RichLog()

    def write(self, message: str):
        self.query_one(RichLog).write(message)


class DayPartView(Widget):
    def __init__(self, results: list[str] = [], id: str | None = None):
        super().__init__(id=id)
        self.results = results

    def compose(self):
        yield ResultsComponent(self.results)
        yield LogComponent()

    def set_results(self, results: list[str]):
        self.results = results
        self.query_one(ResultsComponent).results = results

    def add_log_message(self, message: str):
        self.query_one(LogComponent).write(message)
