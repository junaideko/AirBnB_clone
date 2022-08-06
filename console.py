#!/usr/bin/python3
"""Console module for the AirBnB clone"""
import cmd
import models


class HBNBCommand(cmd.Cmd):
    """cmd clone"""
    intro = 'Welcome to the Airbnb console. Type help or ? to list commands.\n'
    prompt = '(hbnb)'

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        """init method"""
        super().__init__(completekey, stdin, stdout)

    def do_quit(self, arg):
        """quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command"""
        return True

    def emptyline(self):
        """empty line. Do nothing"""
        return False

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it
        (to the JSON file) and prints the id
        """

        if arg == "":
            print('** class name missing **')
        elif arg not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
            return
        try:
            model = models.classes[arg]()
            models.storage.new(model)
            models.storage.save()
            print(model.id)
        except Exception as e:
            print(e)

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        """
        if arg == "":
            print('** class name missing **')
        elif arg not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
            return
        try:
            model_name, model_id = arg.split(' ')
            model = models.storage.find(model_name, model_id)
            print(model.__str__())

        except Exception as e:
            if arg.count(' ') == 0:
                print('** instance id missing **')
            elif arg.count(' ') > 1:
                print('** too many arguments (2 arguments required)**')
            else:
                print(e)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and
        id (save the change into the JSON file)
        """

        if arg == "":
            print('** class name missing **')
        elif arg not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
            return

        try:
            model_name, model_id = arg.split(' ')
            models.classes[model_name]
            models.storage.delete(model_name, model_id)
            models.storage.save()

        except Exception as e:
            if arg.count(' ') == 0:
                print('** instance id missing **')
            elif arg.count(' ') > 1:
                print('** too many arguments (2 arguments required)**')
            else:
                print(e)

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name
        """
        if arg == "":
            print([x.__str__() for x in models.storage.all().values()])
        elif arg not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
            return
        else:
            try:
                model = models.classes[arg]
                resp = []
                for i in models.storage.all().values():
                    if type(i) == model:
                        resp.append(i.__str__())
                print(resp)
            except Exception as e:
                print(e)

    def do_update(self, arg):
        """Updates an instance based on the
        class name and id (save the change into the JSON file)

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """

        if arg == "":
            print('** class name missing **')
        elif arg not in HBNBCommand.classes:
            print('** class doesn\'t exist **')
            return

        try:
            model_name, model_id, attr, value = arg.split(' ')
            models.storage.update(model_name, model_id, attr, value)
            models.storage.save()

        except Exception as e:
            if arg.count(' ') == 0:
                print('** instance id missing **')
            elif arg.count(' ') == 1:
                print("** attribute name missing **")
            elif arg.count(' ') == 2:
                print("** value missing **")
            elif arg.count(' ') > 3:
                print('** too many arguments (2 arguments required)**')
            else:
                print(e)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
