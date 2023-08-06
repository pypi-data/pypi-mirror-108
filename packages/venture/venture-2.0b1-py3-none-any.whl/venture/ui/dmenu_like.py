from __future__ import annotations
from typing import Iterable
import subprocess
from .ui_provider import UIProvider
from .. import util
from ..icons import icon_map, iconize


class DmenuLike(UIProvider):
    command: str
    default_args: Iterable[str] = []
    argument_format: str
    seperator: str = "\n"

    def run(self):
        args = self.get_commandline_args()
        output = self.execute(args)
        parsed = self.parse_output(output)
        return self.items.get(self._display_items.get(parsed))

    def get_commandline_args(self) -> Iterable[str]:
        if not self.config.args:
            return []

        return [
            item
            for name, value in self.config.args.items()
            for item in self.format_arg(name, value)
        ]

    def format_arg(self, name, value):
        if value == False:
            return []
        if value == True:
            value = ""

        return (
            self.argument_format.format(name=name, value=value).rstrip(" ").split(" ")
        )

    def execute(self, args):
        """Execute the UI command.

        This implementation expects the UI to be an external process
        and for it to recieve it's input as a newline-seperated
        list of strings from stdin.
        """
        proc = subprocess.Popen(
            [self.command, *self.default_args, *args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        return proc.communicate(
            bytes(self.seperator.join(self._display_items), "utf-8")
        )[0]

    def parse_output(self, output: bytes):
        choice = output.decode("utf-8").strip("\n")
        return choice


class Dmenu(DmenuLike):
    command = "dmenu"
    argument_format = "--{name} {value}"


class Rofi(DmenuLike):
    command = "rofi"
    seperator = "|"
    default_args = ["-dmenu", "-markup-rows", "-sep", seperator]
    argument_format = "-{name} {value}"


class QL(DmenuLike):
    tag_sep: str = "\n"

    def format_tags(self, item):
        tags = [iconize(tag, self.config.color_icons) for tag in item.get("tags", [])]

        all_tags = (
            [f"{icon_map.get('directory')}  {item['path']}"] + tags
            if self.config.quicklaunch.show_filepath
            else tags
        )
        return util.pango_span(
            ", ".join(all_tags),
            color="#9c9c9c",
            size="smaller",
            weight="light",
        )

    def format_items(self, items):
        return {
            f"{iconize(item.get('icon', ''), self.config.color_icons):<2} "
            f"{name}{self.tag_sep}{self.format_tags(item)}": name
            for name, item in items.items()
        }


class RofiQL(Rofi, QL):
    default_args = Rofi.default_args + ["-eh", "2"]


class Wofi(DmenuLike):
    command = "wofi"
    default_args = ["--dmenu", "--allow-markup"]
    argument_format = "--{name} {value}"


class WofiQL(Wofi, QL):
    tag_sep = " "
