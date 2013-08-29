import sublime
import sublime_plugin
import re
import mmap
import contextlib
import os

from .settings import filename as settings_filename

def get_settings():
    return sublime.load_settings(settings_filename())

def get_setting(key, default=None, view=None):
    try:
        if view == None:
            view = sublime.active_window().active_view()
        s = view.settings()
        if s.has("sublimated_%s" % key):
            return s.get("sublimated_%s" % key)
    except:
        pass
    return get_settings().get(key, default)

def find_symbol(symbol, window):
    files = window.lookup_symbol_in_index(symbol)
    namespaces = []
    pattern = re.compile(b'^\s*namespace\s+([^;]+);', re.MULTILINE)
    def filter_file(file):
        for pattern in setting('exclude_dir'):
            pattern = re.compile(pattern)
            if pattern.match(file[1]):
                return False
        return file
    for file in files:
        if filter_file(file):
            with open(file[0], "rb") as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                    for match in re.findall(pattern, m):
                        namespaces.append([match.decode('utf-8') + "\\" + symbol, file[1]])
                        break
    return namespaces