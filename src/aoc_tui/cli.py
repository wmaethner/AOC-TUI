import inspect
import os
import sys
from pathlib import Path
from types import ModuleType

import click
import dotenv

from .core.aoc_app import AOCApp
from .tui.app import AOCTuiApp


class AppContext:
    def __init__(self):
        self.app = self.load_app()

    def load_app(self) -> AOCApp | None:
        module_name, path = prepare_import("app.py")
        self.app_path: Path = Path(path)
        __import__(module_name)
        module = sys.modules[module_name]

        app = find_app(module)
        return app

    def set_mode(self, mode: str) -> None:
        self.mode = mode


pass_app_context = click.make_pass_decorator(AppContext, ensure=True)


class AppGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        self.add_command(run_command)
        self.add_command(new_group)
        self.add_command(run_tui)

    def make_context(self, info_name, args, parent=None, **extra):
        load_dotenv()
        return super().make_context(info_name, args, parent, **extra)


@click.group("new")
@pass_app_context
def new_group(ctx: AppContext) -> None:
    ctx.set_mode("New")


# Follows Flask pattern
def prepare_import(path: str) -> tuple[str, str]:
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


def find_app(module: ModuleType) -> AOCApp | None:
    app = getattr(module, "app", None)
    if isinstance(app, AOCApp):
        return app

    print("No app found in module")


@click.command("run")
@click.argument("year", type=int)
@click.argument("day", type=int)
@pass_app_context
def run_command(app_context: AppContext, year: int, day: int) -> None:
    app_context.app.run(year, day)
    # app_context.app._find_years()


@new_group.command("day")
@click.argument("year", type=int)
@click.argument("day", type=int)
@pass_app_context
def new_day_command(ctx: AppContext, year: int, day: int) -> None:
    file_path = Path(ctx.app_path, f"year_{year}", f"day{day}.py")
    if file_path.exists():
        print("Day already exists")
        return
    with open(file_path, "w") as f:
        f.writelines(
            [
                f"{line}\n"
                for line in [
                    "from aoc_tui.core.aoc_day import AOCDay",
                    "\n",
                    f"class Day{day}(AOCDay):",
                    "    def __init__(self):",
                    f"        super().__init__({day})\n",
                    "    def part1(self):",
                    "        pass\n",
                    "    def part2(self):",
                    "        pass",
                ]
            ]
        )


@click.command("tui")
@pass_app_context
def run_tui(ctx: AppContext) -> None:
    print("Running TUI")
    tui_app = AOCTuiApp(ctx.app)
    tui_app.run()


def load_dotenv():
    path = dotenv.find_dotenv(".env", usecwd=True)
    if path:
        dotenv.load_dotenv(path)


cli = AppGroup()


def main() -> None:
    cli.main()


if __name__ == "__main__":
    main()
