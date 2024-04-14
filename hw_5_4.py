# Доробіть консольного бота помічника з попереднього домашнього завдання та 
# додайте обробку помилок за допомоги декораторів.

# Вимоги до завдання:
# 1. Всі помилки введення користувача повинні оброблятися за допомогою
# декоратора input_error. Цей декоратор відповідає за повернення 
# користувачеві повідомлень типу "Enter user name", "Give me name and phone please" тощо.
# 
# 2. Декоратор input_error повинен обробляти винятки, що виникають у 
# функціях - handler і це винятки: KeyError, ValueError, IndexError. Коли 
# відбувається виняток декоратор повинен повертати відповідну відповідь 
# користувачеві. Виконання програми при цьому не припиняється.
#
# К ритерії оцінювання:
#
# Наявність декоратора input_error, який обробляє помилки введення користувача для всіх команд.
# Обробка помилок типу KeyError, ValueError, IndexError у функціях за допомогою декоратора input_error.
# Кожна функція для обробки команд має власний декоратор input_error, який обробляє відповідні помилки і повертає відповідні повідомлення про помилку.
# Коректна реакція бота на різні команди та обробка помилок введення без завершення програми.

from functools import wraps
from pathlib import Path
import math

def file_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:  
            phones_list = []
            phones_list = func(*args)
            print("Phones list imported and saved successfully")
            return phones_list
        except FileNotFoundError as ex:
            print(f"Error while importing or saving data. Please check Path and File. Error: {ex}")
    return inner

def find_dictionary_by_name(phone_info:list , target_name:str):   
    for dictionary in phone_info:
        if dictionary.get(target_name):
            return dictionary
    return None

@file_error
def get_phones_info(file_path:Path):
    try:
        user_str = []
        user_dict= {}
        phones_list=[]
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    line = line.strip()
                    user_str = line.split(",")
                    user_dict ={user_str[0] : user_str[1].strip()}
                    phones_list.append(user_dict)
                except Exception as ex:
                    print(f"mistake in data structure: {ex}, line: {line}")
    except Exception as ex:
        print(f"{ex}")
    return phones_list

@file_error
def save_to_file(phones_info:list, file_path:Path):
        with open(file_path, "w", encoding="utf-8") as file:
            for dictionary in phones_info:
                key = list(dictionary.keys())[0]
                file.write(f"{key},{dictionary.get(key)}\n")
    #     return "data saved"
    # except Exception as ex:
    #     print(f"{ex}")
# 
def input_error(func):
    @wraps(func)
    def inner(*args):
        phone_list=[]
        name =''
        phone=''
        try:
            if func.__name__ == 'parse_input':
                user_input = args[0]
            else:
                phone_list = args[0]
                name = args[1][0]
                phone = args[1][1]
        except (IndexError, ValueError, TypeError):
            pass
        
        match func.__name__:
            case "add_contact":
                try:
                   return func(phone_list, name, phone)
                except Exception as ex:
                    print(f"Unable to add contact. Error: {ex}")
            case "change_contact":                                                    
                try:
                    return func(phone_list, name, phone)
                except Exception as ex:
                    print(f"Unable to change contact. No such Name or mistake in data structure. Error: {ex}")
            case "show_phone":
                try:
                    return func(phone_list, name)
                except Exception as ex:
                    print(f"Unable to show phone number. Error: {ex}")
            case "show_all":
                try:
                    return func(phone_list)
                except Exception as ex:
                    print(f"Unable to show all database. Error: {ex}")
            case "parse_input":
                try:
                    return func(*args)
                except Exception as ex:
                    print(f"Unable to parse parameters from command prompt. please use 'help' for help. Error: {ex}")
            case _:
                print("no such function")
    return inner
# 
# 
# 
# 
# 
# 
# 
@input_error
def add_contact(phones_info:list,name_to_add:str, phone_to_add:str)->str:
        phones_info.append({name_to_add: phone_to_add})
        return "data added"
    # except Exception as ex:
    #     return f"error in add_contact {ex}"

@input_error
def change_contact(phones_info:list,name_to_change:str,new_phone:str)->str:
    dict_to_change = {}
    dict_to_change = find_dictionary_by_name (phones_info,name_to_change)
    if dict_to_change != None:
        dict_to_change.update({name_to_change: new_phone})
        message = f"data updated! name:{name_to_change}, phone:{dict_to_change.get(name_to_change)}"
    else:    
        message = "No such name in a list"
    return message

@input_error
def show_phone(phones_info:list, name_to_find:str)->str:
    dict_to_find = find_dictionary_by_name(phones_info,name_to_find)
    if dict_to_find != None:
        message = f"Phone number of {name_to_find} is {dict_to_find.get(name_to_find)}"
    else:    
        message = "No such name in a list"
    return message

@input_error
def show_all(phones_info:list):
    symbol = " "
    i = 1
    # line = {}
    if len(phones_info)>=1:
        message = " №  |          name          |         phone\n__________\n"
    for line in phones_info:
        key = list(line.keys())[0]
        move_name = math.trunc(12-len(key)/2)
        move_name_right = move_name if (len(key) % 2) == 0  else move_name+1
        move_phone = math.trunc(12-len(line[key])/2)
        message += f" {i}{symbol*math.trunc(3-len(str(i))/2)}|{symbol*move_name}{key}{symbol*(move_name_right)}|{symbol*move_phone}{line[key]}"
        i+=1
    else: 
        message = None
    return message

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split(' ')
    cmd = cmd.strip().lower()
    args = [arg.strip() for arg in args]
    return cmd, args

def main():
    file_path = Path("phones.txt")
    phones_info = get_phones_info(file_path)
    
    print("Welcome to the assistant bot!")
    while True:
            message = ""
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input) 
            command = command.lower()
       
            match command:
                case "close"|"exit":
                    print("Good bye!")
                    break
            
                case "hello":
                    print("How can I help you?")

                case "get from file"|"get":
                    phones_info = get_phones_info(file_path)
           
                case "add":
                    print (add_contact(phones_info, args[0],args[1]))

                case "change":
                    print (change_contact(phones_info, args[0],args[1]))
                    
                case "all":
                    print(f"Your contact database: \n {show_all(phones_info)}")

                case "phone":
                    print(show_phone(phones_info, args))

                case "save":
                    message = save_to_file(phones_info,file_path)

                case "help"|"?"|"/?":
                    print("""available command of bot is:  
                        "hello" - to say hello to bot   
                        "close" or "exit" - to stop bot
                        commands for contacts: 
                            "add" with arguments "Name" and "Phone" will add contact to database (DB). for example add NewName NewPhone
                            "change" with arguments "Name" and "Phone" will change contact in DB
                            "all" - to show all contacts in DB
                            "phone" - with argument "Name" will show the phone of contact
                            "save" - save names and phones to file
                        """)
                case _:
                    print("Invalid command. is you need assistance please enter: help")

if __name__ == "__main__":
    main()
