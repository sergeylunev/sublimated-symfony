import sublime
import sublime_plugin
import re
import mmap
import contextlib
import os

from ..utils import *

class EntityToRepositoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.is_entity = False
        self.is_repository = False
        self.file = self.view.file_name()
        
        self.file_is(self.file)
        if self.is_entity:
            if self.view.find('(repositoryClass)', 0):
                repository_class_region = self.view.find('(repositoryClass)', 0)
                repository_class_line = self.view.line(repository_class_region)
                repository_class_string = self.view.substr(repository_class_line)
                repository_class = re.search(r'(repositoryClass\=\")(.*)(\")', repository_class_string).group(2)
                repository_class_path = os.sep.join(repository_class.split('\\'))
                src_position = self.reg_search_file_name.group(1).find('src') + 3
                repository_class_file = self.reg_search_file_name.group(1)[:src_position] + os.sep + repository_class_path + '.php'
                if os.path.exists(repository_class_file):
                    self.view.window().open_file(repository_class_file)
                else:
                    sublime.status_message('There is no Repository Class for Entity.')
        elif self.is_repository:
            print("Repository")

    def file_is(self, file_name):
        self.reg_search_file_name = re.search(r'^(.*)(\/)(Entity)(\/)(.*)$', file_name)
        if self.reg_search_file_name:
            # If we are in Repository class
            if re.search(r'^(Repository)(\/)', self.reg_search_file_name.group(5)):
                self.is_repository = True
            # If we are in Entity class
            else:
                self.is_entity = True
