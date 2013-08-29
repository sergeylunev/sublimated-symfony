import sublime
import sublime_plugin
import re
import mmap
import contextlib
import os

from ..utils import *

class ImportUseCommand(sublime_plugin.TextCommand):
    def run(self, edit, namespace):
        view = self.view
        use_stmt = "use " + namespace + ";"

        region = view.find(use_stmt.replace('\\', '\\\\'), 0)
        if not region.empty():
            return sublime.status_message('Use already exist !')

        regions = view.find_all(r"^(use\s+.+[;])")
        use_stmt = "\n" + use_stmt

        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)
            view.insert(edit, region.end(), use_stmt)
            return sublime.status_message('Successfully imported' + namespace)

        region = view.find(r"^\s*namespace\s+[\w\\]+[;{]", 0)
        if not region.empty():
            line = view.line(region)
            view.insert(edit, line.end(), use_stmt)
            return sublime.status_message('Successfully imported' + namespace)

        region = view.find(r"<\?php", 0)
        if not region.empty():
            line = view.line(region)
            view.insert(edit, line.end(), use_stmt)
            return sublime.status_message('Successfully imported' + namespace)