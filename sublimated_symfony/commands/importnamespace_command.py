import sublime
import sublime_plugin
import re
import mmap
import contextlib
import os

from ..utils import *

class ImportNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings(settings_filename()).get

        region = self.view.find(r"^\s*namespace\s[\w\\]+;", 0)

        if not region.empty():
            return sublime.status_message('namespace definition already exist!')

        # Filename to namespace
        filename = self.view.file_name()

        if (not filename.endswith(".php")):
            sublime.error_message("No .php extension")
            return

        # namespace begin at first camelcase dir
        namespaceStmt = os.path.dirname(filename)

        if (settings("start_dir_pattern")):
            pattern = re.compile(settings("start_dir_pattern"))
        else:
            pattern = r"^.*?((?:\/[A-Z][^\/]*)+)$"

        namespaceStmt = re.sub(pattern, '\\1', namespaceStmt)
        namespaceStmt = re.sub('/', '\\\\', namespaceStmt)
        namespaceStmt = namespaceStmt.strip("\\")

        region = self.view.find(r"<\?php", 0)
        if not region.empty():
            line = self.view.line(region)
            line_contents = "\nnamespace " + namespaceStmt + ";"
            self.view.insert(edit, line.end(), line_contents)
            return True