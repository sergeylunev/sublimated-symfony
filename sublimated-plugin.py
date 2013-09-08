import sublime
import sublime_plugin
import re
import mmap
import contextlib
import os

jump_to_action = ''

from .sublimated_symfony.commands.action2view_command import SublimatedSymfonyViewCommand
from .sublimated_symfony.commands.finduse_command import FindUseCommand
from .sublimated_symfony.commands.importuse_command import ImportUseCommand
from .sublimated_symfony.commands.importnamespace_command import ImportNamespaceCommand
from .sublimated_symfony.commands.entity2repository_command import EntityToRepositoryCommand

class SymfonyEvent(sublime_plugin.EventListener):
    def on_load(self, view):
        global jump_to_action
        if jump_to_action:
            sel = view.find(jump_to_action + "Action", 0)
            view.show(sel)
            jump_to_action = ''
