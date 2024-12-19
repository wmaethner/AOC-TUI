from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static

from aoc_tui.core.aoc_day import AOCDay
from aoc_tui.core.aoc_day_part import PartData
from aoc_tui.tui.components.day_view import DayView
from aoc_tui.tui.components.title import Title

components = [
    "Title",
    "Day View",
]


class ComponentContainer(Container):
    component: reactive[Widget] = reactive(Static("DEFAULT"), recompose=True)

    def compose(self):
        yield self.component


class ComponentTester(Screen):
    BINDINGS = [
        Binding("b", "back", "Back"),
        Binding("w", "log_message", "Log Message"),
    ]
    CSS_PATH = "../css/component_tester.tcss"

    selected_component: reactive[Widget] = reactive(
        Static("Component Tester"), recompose=True
    )

    reactive_title = reactive("Component Tester Title")

    def compose(self):
        yield Footer()

        yield ListView(
            *[ListItem(Label(name), name=name) for name in components],
        )
        yield ComponentContainer()

    def on_list_view_highlighted(self, message: ListView.Highlighted):
        if message.item:
            self.query_one(ComponentContainer).component = self.get_widget(
                message.item.name
            )

    def get_widget(self, name: str) -> Widget:
        if name == "Title":
            return self.get_title_widget()
        elif name == "Day View":
            return self.get_day_view_widget()
        return Static("DEFAULT")

    def get_title_widget(self) -> Widget:
        return Title("TITLE")

    def get_day_view_widget(self) -> Widget:
        day_view = DayView()
        day = AOCDay(2021, 1)
        day.part(1).data = PartData(year=2021, day=1, part=1, result=["1", "2", "3"])
        day.part(2).data = PartData(year=2021, day=1, part=2, result=["1", "2", "3"])
        day_view.day = day
        return day_view

    def action_log_message(self):
        self.query_one(DayView).add_log_message("Test message")

    def action_back(self):
        self.app.pop_screen()
