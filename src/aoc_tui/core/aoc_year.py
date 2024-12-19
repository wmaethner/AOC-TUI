import inspect
import os
import shutil
import sys
from pathlib import Path

import requests

from aoc_tui.core.aoc_day import AOCDay


class AOCYear:
    def __init__(self, year: int, directory: Path):
        self.year = year
        self.directory = directory
        self.days: dict[int, AOCDay] = {}
        self.stars = 0
        self.completed_days = 0
        self.days_started = 0
        self.modules = []
        self.loaded_days = []
        self._find_days()

    def new_day(self, day: int):
        if day in self.days:
            return

        # Copy template day file and replace
        shutil.copy(Path(__file__).parent / "templates/day.txt", self.directory)
        shutil.move(
            Path(self.directory, "day.txt"), Path(self.directory, f"day{day}.py")
        )

        file = Path(self.directory, f"day{day}.py")
        text = file.read_text()
        text = text.replace("{x}", str(day))
        file.write_text(text)

        self._find_days()

        # Download input
        # self.days[day]._fetch_input_data()
        self._fetch_input_data(day)

    def _find_days(self):
        day_files = sorted(
            [Path(f) for f in os.scandir(self.directory) if f.name.startswith("day")]
        )
        self.modules = [str(f) for f in day_files]
        for day_path in day_files:
            self._load_day(day_path)
        self.days = dict(sorted(self.days.items(), reverse=True))

    def _load_day(self, path: Path):
        module_name, _ = self.prepare_import(str(path))
        __import__(module_name)
        day_classes = [
            c for c in AOCDay.__subclasses__() if c.__module__ == module_name
        ]
        self._add_day(day_classes[0](self.year, int(path.stem[3:])))

    def _add_day(self, day: AOCDay):
        day.set_year(self.year)
        self.days[day.day] = day

    def _fetch_input_data(self, day: int) -> list[str]:
        response = requests.get(
            f"https://adventofcode.com/{self.year}/day/{day}/input",
            cookies={
                # "session": "53616c7465645f5f69a85fdaf165277035ea8ba9d66e9748f47a15d9736105233a419cdf544e44e1f2008a2f3fe52b17f6d4e77ceeffb0598a88aa0e24500aab"
                "session": os.getenv("AOC_SESSION")
            },
        )
        # input = response.text.strip().split("\n")
        if not os.path.exists(self._input_directory()):
            os.makedirs(self._input_directory())

        with open(Path(self._input_directory(), f"day{day}.txt"), "w") as f:
            f.write(response.text.strip())

    def _parent_directory(self) -> Path:
        return Path().absolute()

    def _input_directory(self) -> Path:
        return Path(self.directory, "inputs")

    # Follows Flask pattern
    def prepare_import(self, path: str) -> tuple[str, str]:
        path = os.path.realpath(path)
        fname, ext = os.path.splitext(path)
        if ext == ".py":
            path = fname

        if os.path.basename(path) == "__init__":
            path = os.path.dirname(path)

        module_name = []

        # move up until outside package structure (no __init__.py)
        while True:
            path, name = os.path.split(path)
            module_name.append(name)

            if not os.path.exists(os.path.join(path, "__init__.py")):
                break

        if sys.path[0] != path:
            sys.path.insert(0, path)

        return ".".join(module_name[::-1]), path
