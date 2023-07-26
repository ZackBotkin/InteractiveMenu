
class InteractiveMenu(object):

    def __init__(self, manager):
        self.manager = manager
        self.sub_menu_modules = []

    def menu_print(self, items):
        print("\n")
        for item in items:
            print("> %s" % item)
        print("\n")

    def menu_print_with_exit(self, items):
        items.append("Exit")
        self.menu_print(items)

    def fancy_input(self, text=None):
        answer = None
        if text is None:
            answer = input("%s " % (self.manager.config.get("line_start")))
        else:
            answer = input("%s %s" % (self.manager.config.get("line_start"), text))
        answer = answer.strip()
        return answer

    def sub_menu_titles(self):
        sub_menu_titles = []
        for sub_menu in self.sub_menu_modules:
            sub_menu_titles.append(sub_menu.title())
        return sub_menu_titles

    def get_sub_menu_as_string(self):
        return ', '.join(self.sub_menu_titles())

    def get_sub_menu_mapping(self):
        mapping = {}
        for sub_menu in self.sub_menu_modules:
            mapping[sub_menu.title()] = sub_menu
        return mapping

    def title(self):
        raise Exception("Not implemented yet!")

    def main_loop(self):

        back_result = False
        sub_menu_mapping = self.get_sub_menu_mapping()

        while not back_result:
            prompt = ''
            sub_menu_as_str = self.get_sub_menu_as_string()
            if len(sub_menu_as_str) == 0:
                prompt = 'Back, Exit'
            else:
                prompt = '%s, Back, Exit' % sub_menu_as_str
            print("%s" % prompt)
            answer = self.fancy_input()
            pre_capitalized_answer = answer
            answer = answer.capitalize()
            if answer in sub_menu_mapping:
                sub_menu_module = sub_menu_mapping[answer]
                sub_menu_module.main_loop()
            elif answer in ["back", "Back"]:
                back_result = True
            elif answer in ["exit", "Exit"]:
                exit()
            elif answer == '':
                pass
            else:
                print("\"%s\" is not a valid choice. Please choose one of the following options" % pre_capitalized_answer)
