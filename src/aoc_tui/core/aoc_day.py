import inspect
import json
import os
from pathlib import Path
from typing import Callable

import requests

from aoc_tui.core.aoc_day_part import AOCDayPart, PartData


class AOCDay:
    def __init__(self, year: int, day: int):
        self.year = year
        self.day = day
        self._data = self.load()

        self._part_1 = AOCDayPart(
            self._part_data(1), self.part1, self._parent_directory()
        )
        self._part_2 = AOCDayPart(
            self._part_data(2), self.part2, self._parent_directory()
        )
        self._parts = {1: self._part_1, 2: self._part_2}
        self.input: str | None = None

        self.event_handlers = {}

    def set_year(self, year: int):
        self.year = year

    def part(self, part: int) -> AOCDayPart:
        return self._parts[part]

    def result(self, part: int) -> str | None:
        return self._parts[part].result()

    def _parent_directory(self) -> Path:
        return Path(os.path.dirname(os.path.realpath(inspect.getfile(self.__class__))))

    def part1(self) -> str:
        raise NotImplementedError()

    def part2(self) -> str:
        raise NotImplementedError()

    def log_message_event_handler(self, handler: Callable[[str], None]):
        self.event_handlers["log_message"] = handler

    def log_message(self, message: str):
        if "log_message" in self.event_handlers:
            self.event_handlers["log_message"](message)

    def _to_json(self) -> dict[str, str]:
        return {
            "year": self.year,
            "day": self.day,
            "part_1": self._part_1._to_json(),
            "part_2": self._part_2._to_json(),
        }

    def save(self):
        with open(self._results_file(), "w") as f:
            f.write(json.dumps(self._to_json(), indent=4))

    def load(self) -> dict[str, any]:
        if self._results_file().exists():
            with open(self._results_file(), "r") as f:
                return json.load(f)

    def _part_data(self, part: int) -> PartData:
        if not self._data:
            return PartData(self.year, self.day, part)
        return PartData(**json.loads(self._data[f"part_{part}"]))

    def _results_directory(self) -> Path:
        dir = Path(self._parent_directory(), "results")
        if not dir.exists():
            os.makedirs(dir)
        return dir

    def _results_file(self) -> Path:
        return Path(self._results_directory(), f"day{self.day}.json")

    def _fetch_input_data(self) -> list[str]:
        response = requests.get(
            f"https://adventofcode.com/{self.year}/day/{self.day}/input",
            cookies={
                "session": "53616c7465645f5f72464f2324b2e31a3ee1f59cd65ff454f226c5b6427cb97fa024f6f169460960a0d5a5ec158141090c81e01f700a6c6be4099bcbc095a7b1"
            },
        )
        input = response.text.strip().split("\n")
        self.part(1).save_input(input)
        self.part(2).save_input(input)
        # self._input_data.save(response.text.strip().split("\n"))
