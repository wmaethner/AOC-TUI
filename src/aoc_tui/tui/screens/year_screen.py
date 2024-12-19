import time

from textual.app import App, ComposeResult, RenderResult
from textual.binding import Binding
from textual.containers import Container, Grid, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Log,
    RichLog,
    Static,
    TabbedContent,
    TabPane,
)

from aoc_tui.core.aoc_day import AOCDay
from aoc_tui.core.aoc_year import AOCYear
from aoc_tui.tui.components.day_view import DayView
from aoc_tui.tui.components.title import Title


class NewDayScreen(ModalScreen[int]):
    def compose(self):
        yield Grid(Label("What day do you want to create?"), Input(type="integer"))

    def on_input_submitted(self, message: Input.Submitted):
        self.dismiss(message.value)


class DayListView(ListView):
    class DayHighlighted(Message):
        def __init__(self, day: AOCDay):
            self.day = day
            super().__init__()

    def __init__(self, year: AOCYear):
        self.days: dict[str, AOCDay] = {
            f"Day_{day.day}": day for day in year.days.values()
        }

        super().__init__(
            *[
                ListItem(Static(f"Day: {value.day}"), id=key)
                for key, value in self.days.items()
            ]
        )

    def on_list_view_highlighted(self, message: ListView.Highlighted):
        if message.item:
            self.post_message(self.DayHighlighted(self.days[message.item.id]))


class TestWidget(Widget):
    def compose(self):
        yield Static("Hello, world!")


class PartResults(Widget):
    result: reactive[str | None] = reactive(None, recompose=True)

    def __init__(self, day: AOCDay, part: int):
        super().__init__()
        self.day = day
        self.part = part

    def compose(self):
        results = self.day.part(self.part).result()

        yield Vertical(
            Horizontal(
                Label("Result: "),
                Static("\n".join(results) if results else "No result"),
            ),
            Static("Log"),
            RichLog(),
        )
        # with Container():
        #     # yield Label(f"Part {self.part} Results")
        #     results = self.day.part(self.part).result()
        #     if results:
        #         yield Static("\n".join(results))
        #     else:
        #         yield Static("No results")

    def on_mount(self):
        self.query_one(RichLog).write("Hello, world!")


class DayResults(Widget):
    BINDINGS = [
        Binding("b", "back", "Back"),
    ]

    day: reactive[AOCDay | None] = reactive(None, recompose=True)

    def __init__(self):
        super().__init__()

    def compose(self):
        yield Title(
            f"Day {self.day.day} Results" if self.day else "No day selected",
            font_size="small",
        )

        if self.day:
            with TabbedContent(initial="part_1"):
                with TabPane("Part 1", id="part_1"):
                    with Container():
                        yield PartResults(self.day, 1)
                with TabPane("Part 2", id="part_2"):
                    with Container():
                        yield PartResults(self.day, 2)

    def switch_tab(self, tab: str):
        self.get_child_by_type(TabbedContent).active = tab

    def active_part(self) -> int:
        return int(self.get_child_by_type(TabbedContent).active[-1])


class YearScreen(Screen):
    BINDINGS = [
        Binding("b", "back", "Back"),
        Binding("1", "show_tab('part_1')", "Show Part 1"),
        Binding("2", "show_tab('part_2')", "Show Part 2"),
        Binding("r", "run_part", "Run Part"),
        Binding("n", "new_day", "New Day"),
    ]
    CSS_PATH = ["../css/year_screen.tcss", "../css/day_view.tcss"]

    year: reactive[AOCYear] = reactive(None, recompose=True)

    def __init__(self, year: AOCYear):
        super().__init__()
        self.year = year

    def compose(self):
        yield Header()
        yield Title(f"Year: {self.year.year}")

        yield DayListView(self.year)

        # yield DayResults()
        with Container(classes="box"):
            yield DayView()
        yield DayView()
        yield Footer()

    def on_mount(self):
        self.title = f"Year {self.year.year}"
        # self.title = f"Time: {time.time()}"

    def on_day_list_view_day_highlighted(self, message: DayListView.DayHighlighted):
        self.query_one(DayView).day = message.day
        # self.query_one(DayResults).day = message.day

    def action_run_part(self):
        day_view = self.query_one(DayView)
        self._action_run_part_by_number(day_view.active_part())
        # day_results = self.query_one(DayResults)
        # self._action_run_part_by_number(day_results.active_part())
        # day.part(1).run()

    def action_run_part_1(self):
        self._action_run_part_by_number(1)

    def action_run_part_2(self):
        self._action_run_part_by_number(2)

    def _action_run_part_by_number(self, part: int):
        day_view = self.query_one(DayView)
        day = day_view.day
        # day = self.query_one(DayResults).day
        result = day.part(part).run()
        day_view.set_result(result)
        # part_components = self.query(PartResults)
        # [comp for comp in part_components if comp.part == part][0].result = result
        day.save()

    def action_new_day(self):
        def handle_new_day(day: int | None) -> None:
            self.year.new_day(day)
            self.mutate_reactive(YearScreen.year)

        self.app.push_screen(NewDayScreen(), handle_new_day)

    # def action_show_tab(self, tab: str) -> None:
    #     """Switch to a new tab."""
    #     self.get_child_by_type(DayResults).switch_tab(tab)

    def action_back(self):
        self.app.pop_screen()
