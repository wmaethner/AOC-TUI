from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import requests
from dataclasses_json import dataclass_json

from aoc_tui.core.aoc_part_data import AOCPartData


@dataclass_json
@dataclass
class PartData:
    year: int
    day: int
    part: int
    result: list[str] | None = None
    completed: bool = False


class AOCDayPart:
    def __init__(
        self,
        data: PartData,
        fn: Callable[[list[str]], str | list[str]],
        parent_dir: Path,
        unique_inputs: bool = False,
    ):
        self.data = data
        self.fn = fn
        self.parent_dir = parent_dir

        self._input_data: AOCPartData = AOCPartData(
            Path(self.parent_dir, "inputs"),
            self.data.day,
            self.data.part if unique_inputs else None,
        )
        self._result_data: AOCPartData = AOCPartData(
            Path(self.parent_dir, "results"), self.data.day, self.data.part
        )

    def run(self) -> str | None:
        if not self._input_data.file_exists():
            self._fetch_input_data()
        result = self.fn(self._input_data.data())

        if result:
            if isinstance(result, list):
                result = [str(r) for r in result]
            else:
                result = [str(result)]
            # self._result_data.save(result)
            self.data.result = result

        return self.result()

    def result(self) -> list[str] | None:
        # return self._result_data.data()
        return self.data.result

    def _fetch_input_data(self) -> list[str]:
        response = requests.get(
            f"https://adventofcode.com/{self.data.year}/day/{self.data.day}/input",
            cookies={
                "session": "53616c7465645f5f72464f2324b2e31a3ee1f59cd65ff454f226c5b6427cb97fa024f6f169460960a0d5a5ec158141090c81e01f700a6c6be4099bcbc095a7b1"
            },
        )
        self._input_data.save(response.text.strip().split("\n"))

    def save_input(self, input_data: list[str]):
        self._input_data.save(input_data)

    @staticmethod
    def from_dict(data: dict[str, str]) -> "AOCDayPart":
        return AOCDayPart()

    def _to_json(self) -> str:
        return self.data.to_json()
