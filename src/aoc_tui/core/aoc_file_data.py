class AOCFileData:
    def __init__(self, file_path: str, json_data: bool = False):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> list[str]:
        with open(self.file_path, "r") as f:
            return f.read().splitlines()

    def get_data(self) -> list[str] | dict[str, str]:
        return self.data
