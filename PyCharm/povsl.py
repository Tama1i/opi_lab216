#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from datetime import date
import jsonschema


def add(pep):
     # Запросить данные о работнике.
    name = input("name faname? ")
    num = int(input("number? "))
    br = int(input("burftday? "))

        # Создать словарь.
    chel = {
            'name': name,
            'num': num,
            'br': br,
            }

            # Добавить словарь в список.
    pep.append(chel)
            # Отсортировать список в случае необходимости.
    if len(pep) > 1:
        pep.sort(key=lambda item: item.get('br',''))
    return pep

def li(pep):
     line = '+-{}-+-{}-+-{}-+-{}-+'.format(
                '-' * 4,
                '-' * 30,
                '-' * 20,
                '-' * 8
            )
     print(line)
     print(
          '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
              "№",
              "F.I.O.",
              "NUMBER",
              "BRDAY"
          )
     )
     print(line)
     for idx, chel in enumerate(pep, 1):
        print(
             '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                 idx,
                 chel.get('name', ''),
                 chel.get('num', ''),
                 chel.get('br', 0)
             )
        )
        print(line)


def sel(pep):
     # Получить требуемый стаж.
     zapros = int(input("zapros po numeru  "))

     # Инициализировать счетчик.
     count = 0
     # Проверить сведения работников из списка.
     for chel in pep:
        if chel.get('num') == zapros:
            count += 1
            print(
                 '{:>4}: {}'.format(count, chel.get('name', ''))
            )

            # Если счетчик равен 0, то работники не найдены.
     if count == 0:
        print("cheela s takim nomerom net")


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    schema = {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "name": {
              "type": "string"
            },
            "num": {
              "type": "integer"
            },
            "br": {
              "type": "integer"
            }
          },
          "required": [
            "name",
            "num",
            "br"
          ]
        }
      ]
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("валидация успешна")
        except jsonschema.exceptions.ValidationError:
            print("ошибка валидации", file=sys.stderr)
            exit()
    return loadfile


if __name__ == '__main__':
    # Список работников.
    pep = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            pep = add(pep)

        elif command == 'list':
            li(pep)
        elif command == 'select':
            sel(pep)
        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_workers(file_name, pep)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            pep = load_workers(file_name)
        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - add chel;")
            print("list - show list of pep;")
            print("select <стаж> - запросить работников со стажем;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)

