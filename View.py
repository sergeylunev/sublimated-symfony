import sublime
import sublime_plugin
import re
import os


jump_to_action = ''


class SublimatedSymfonyViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global jump_to_action
        opened_file = self.view.file_name()
        reg_controller = re.compile(r'(.+)[/\\](.+)Controller.php')
        reg_twig = re.compile(r'(.+)[/\\](.+)[/\\](.+).html.twig')
        file_is_symfony_controller = reg_controller.search(opened_file)
        if file_is_symfony_controller:
            folder = file_is_symfony_controller.group(1)
            controller_name = file_is_symfony_controller.group(2)
            action = self.get_current_function(self.view)
            if action:
                action_name = re.search('(\w+)Action', action).group(1)
                template_file = self.search_for_template(folder, controller_name, action_name)
                if not os.path.exists(template_file):
                    f = open(template_file, 'w')
                    f.close
                self.view.window().open_file(template_file)
        elif reg_twig.search(opened_file):
            file_match = reg_twig.search(opened_file)
            folder = file_match.group(1)
            controller = file_match.group(2)
            action = file_match.group(3)
            controller_file = self.search_for_controller(folder, controller)
            self.view.window().open_file(controller_file)
            jump_to_action = action
        else:
            sublime.status_message('Wrong type of file provided.')

    def get_current_function(self, view):
        sel = view.sel()[0]
        function_regs = view.find_by_selector('entity.name.function')
        cf = None
        for r in reversed(function_regs):
            if r.a < sel.a:
                cf = view.substr(r)
                break
        return cf

    def search_for_template(self, folder, controller_name, action):
        bundle_folder = folder + os.sep + '..' + os.sep
        views_folder = 'Resources' + os.sep + 'views' + os.sep
        tempate_file = controller_name + os.sep + action + '.html.twig'
        return bundle_folder + views_folder + tempate_file

    def search_for_controller(self, folder, controller):
        bundle_folder = folder + os.sep + '..' + os.sep + '..' + os.sep
        controller = 'Controller' + os.sep + controller + 'Controller.php'
        return bundle_folder + controller


class SymfonyEvent(sublime_plugin.EventListener):
    def on_load(self, view):
        global jump_to_action
        if jump_to_action:
            sel = view.find(jump_to_action + "Action", 0)
            view.show(sel)
            jump_to_action = ''
