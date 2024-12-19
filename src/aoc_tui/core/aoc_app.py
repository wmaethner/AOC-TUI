import inspect
import os
from pathlib import Path

from aoc_tui.core.aoc_year import AOCYear


class AOCApp:
    def __init__(self):
        self.years: dict[int, AOCYear] = {}
        self._find_years()

    def add_year(self, year: AOCYear):
        self.years[year.year] = year

    def run(self, year: int, day: int):
        self.years[year].days[day].part(1).run()
        self.years[year].days[day].part(2).run()

    def get_year(self, year: int) -> AOCYear:
        return self.years[year]

    def get_years(self) -> list[int]:
        return list(self.years.keys())

    def get_year_objects(self) -> list[AOCYear]:
        return list(self.years.values())

    def _find_years(self):
        for year_directory in self._year_directories():
            year = AOCYear(int(year_directory.name.split("_")[1]), year_directory)
            self.add_year(year)
        self.years = dict(sorted(self.years.items(), reverse=True))

    def _parent_directory(self) -> Path:
        return Path().absolute()

    def _year_directories(self) -> list[Path]:
        subfolders = sorted(
            [
                Path(f)
                for f in os.scandir(self._parent_directory())
                if f.is_dir() and f.name.startswith("year_")
            ]
        )
        return subfolders
