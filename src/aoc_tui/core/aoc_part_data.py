from pathlib import Path


class AOCPartData:
    def __init__(self, directory: Path, day: int, part: int | None = None):
        self.day = day
        self.part_number = part
        self.data_path = Path(
            directory, f"day{day}{f'_part{part}' if part else ''}.txt"
        )

        self._loaded = False
        self._data: list[str] | None = None

    def file_exists(self) -> bool:
        return self.data_path.exists()

    def data(self) -> list[str] | None:
        if not self._loaded:
            self._load_data()
        return self._data

    def _load_data(self):
        if self.file_exists():
            self._data = self.data_path.read_text().strip().split("\n")
            self._loaded = True

    def save(self, data: list[str]):
        self.data_path.write_text("\n".join(data))
        self._data = data
        self._loaded = True

    def __str__(self):
        return f"Part {self.part_number}:\n{self.data}"
