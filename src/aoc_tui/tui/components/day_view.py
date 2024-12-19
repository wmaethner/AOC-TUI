from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import RichLog, Static, TabbedContent, TabPane

from aoc_tui.core.aoc_day import AOCDay
from aoc_tui.tui.components.day_part_view import DayPartView


class DayView(Widget):
    day: reactive[AOCDay | None] = reactive(None, recompose=True)

    def compose(self):
        if self.day:
            yield Static(f"Day: {self.day.day}")
            with TabbedContent():
                with TabPane("Part 1", id="part_1"):
                    yield DayPartView(self.day.part(1).data.result, id="part_1_view")
                with TabPane("Part 2", id="part_2"):
                    yield DayPartView(self.day.part(2).data.result, id="part_2_view")

        else:
            yield Static("No day selected")

    def watch_day(self, day: AOCDay):
        if day:
            day.log_message_event_handler(self.add_log_message)

    def active_part(self) -> int:
        tabs = self.query_one(TabbedContent)
        return int(tabs.active[-1])

    def active_part_view(self) -> DayPartView:
        tabs = self.query_one(TabbedContent)
        return self.query_one(f"#{tabs.active}_view")

    def set_result(self, results: list[str]):
        self.active_part_view().set_results(results)

    def add_log_message(self, message: str):
        tabs = self.query_one(TabbedContent)
        day_part_view: DayPartView = self.query_one(f"#{tabs.active}_view")
        day_part_view.add_log_message(message)
