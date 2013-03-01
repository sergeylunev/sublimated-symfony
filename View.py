import sublime
import sublime_plugin
import re
import os


jump_to_action = ''


class SublimatedSymfonyViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global jump_to_action
        self.is_controller = False
        self.is_twig = False
        self.reg_exp = None
        self.file = self.view.file_name()

        self.file_is(self.file)
        if self.is_controller:
            folder = self.reg_exp.group(1)
            controller_name = self.reg_exp.group(2)
            action = self.get_current_function(self.view)
            if action:
                action_name = re.search('(\w+)Action', action).group(1)
                template_file = self.search_for_template(folder, controller_name, action_name)
                if not os.path.exists(template_file):
                    self.create_template_file(folder, controller_name, action_name)
                self.view.window().open_file(template_file)
        elif self.is_twig:
            folder = self.reg_exp.group(1)
            controller = self.reg_exp.group(2)
            action = self.reg_exp.group(3)
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

    def file_is(self, file_name):
        if re.search(r'(.+)[/\\](.+)Controller.php', file_name):
            self.is_controller = True
            self.reg_exp = re.search(r'(.+)[/\\](.+)Controller.php', file_name)
        elif re.search(r'(.+)[/\\](.+)[/\\](.+).html.twig', file_name):
            self.is_twig = True
            self.reg_exp = re.search(r'(.+)[/\\](.+)[/\\](.+).html.twig', file_name)

    def create_template_file(self, folder, controller_name, action):
        views_folder = folder + os.sep + '..' + os.sep + 'Resources' + os.sep + 'views' + os.sep + controller_name
        if not os.path.exists(views_folder):
            os.makedirs(views_folder)
        file_path = views_folder + os.sep + action + '.html.twig'
        f = open(file_path, 'w')
        f.close

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
