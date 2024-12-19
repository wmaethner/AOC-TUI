from art import text2art
from textual.widget import Widget
from textual.widgets import Static


class Title(Widget):
    def __init__(self, text: str, font_size: str = "standard"):
        super().__init__()
        self.styles.align = "center", "middle"
        self.styles.height = 10
        self.styles.width = "100%"

        self.text = text
        self.font_size = font_size

    def compose(self):
        yield TitleStatic(self.text, self.font_size)


class TitleStatic(Static):
    def __init__(self, text: str, font_size: str):
        super().__init__(text2art(text, font=font_size))
        self.styles.width = "auto"
