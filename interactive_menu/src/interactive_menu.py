from datetime import datetime

class InteractiveMenu(object):

    def __init__(self, manager, path=[], title_text=None):
        self.manager = manager
        self.sub_menu_modules = []
        self.path = []
        self.title_text = title_text
        for path_part in path:
            self.path.append(path_part)
        self.path.append(self.title())

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

    def get_path_as_string(self):
        path_str = ""
        for path_part in self.path:
            path_str += (path_part + " -> ")
        path_str = path_str[:-3]
        box_length = len(path_str)
        return " -%s- \n| %s|\n -%s- " % ("-"*box_length, path_str, "-"*box_length)

    def get_sub_menu_mapping(self):
        mapping = {}
        for sub_menu in self.sub_menu_modules:
            mapping[sub_menu.title()] = sub_menu
        return mapping

    def title(self):
        if self.title_text is None:
            raise Exception("Not implemented yet!")
        else:
            return self.title_text

    def main_loop(self, **kwargs):

        back_result = False
        sub_menu_mapping = self.get_sub_menu_mapping()

        if "continued_commands" in kwargs:
            continued_commands = kwargs["continued_commands"]
            this_command = continued_commands.pop(0)
            pre_capitalized_answer = this_command
            this_command = this_command.capitalize()
            if this_command in sub_menu_mapping:
                sub_menu_module = sub_menu_mapping[this_command]
                if len(continued_commands) > 0:
                    sub_menu_module.main_loop(**{'continued_commands': continued_commands})
                else:
                    sub_menu_module.main_loop()
            elif this_command in ["back", "Back"]:
                pass
            elif this_command in ["exit", "Exit"]:
                pass
            else:
                print("\"%s\" is not a valid choice. Please choose one of the following options" % pre_capitalized_answer)
        else:
            while not back_result:
                path_as_str = self.get_path_as_string()
                print(path_as_str)
                print("|")
                for submenu_title in self.sub_menu_titles():
                    print("| > %s" % submenu_title)
                print("| ")
                print("| > Back")
                print("| > Exit")
                print("|")
                print("")
                answer = self.fancy_input()
                answer_parts = answer.split(" ")
                pre_capitalized_answer = answer_parts[0]
                answer = answer_parts.pop(0).capitalize()
                if answer in sub_menu_mapping:
                    sub_menu_module = sub_menu_mapping[answer]
                    if len(answer_parts) > 0:
                        sub_menu_module.main_loop(**{'continued_commands': answer_parts})
                    else:
                        sub_menu_module.main_loop()
                elif answer in ["back", "Back"]:
                    back_result = True
                elif answer in ["exit", "Exit"]:
                    exit()
                elif answer == '':
                    pass
                else:
                    print("\"%s\" is not a valid choice. Please choose one of the following options" % pre_capitalized_answer)


    #
    #   [ { "question": "", "expected_response_type": "", "return_as": "", "nullable": True }]
    #
    def interactive_form(self, form_contents):

        to_return = {
        }

        for content in form_contents:
            print(content["question"])
            answer = self.fancy_input()
            if answer == "":
                answer = content["default"]
            if content["expected_response_type"] == "YYYYMMDD_Date":
                valid_string = self.validate_YYYYMMDD_date(answer)
            elif content["expected_response_type"] == "FLOAT":
                valid_string = self.validate_FLOAT(answer)
            else:
                valid_string = True
            if answer == "" and not content["allow_empty"]:
                valid_string = False
            to_return[content["return_as"]] = {
                "value": answer,
                "valid": valid_string
            }

        for value_name, content in to_return.items():
            print("|\t> %s -----------> %s" % (value_name, to_return[value_name]["value"]))
        print("OK?")
        answer = self.fancy_input()
        if answer in ["yes", "Yes", "ok", "OK"]:
            to_return["user_accept"] = True
            return to_return
        else:
            return {
                "user_accept": False
            }

    def interactive_form_and_validate(self, form_contents):
        form_results = self.interactive_form(form_contents)
        if form_results["user_accept"] != True:
            print("Aborting!")
            return None
        form_results.pop("user_accept")
        for answer_key in form_results.keys():
            if not form_results[answer_key]["valid"]:
                print("%s is not a valid value! Aborting" % answer_key)
                return None

    ## outsource this to utils project
    def validate_YYYYMMDD_date(self, text):
        accepted_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]
        parsed = []
        for _format in accepted_formats:
            try:
                d = datetime.strptime(text, _format)
                parsed.append(d)
            except:
                pass
        return len(parsed) >= 1

    def validate_FLOAT(self, text):
        try:
            float(text)
            return True
        except:
            return False
