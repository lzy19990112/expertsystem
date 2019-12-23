#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''Json parser'''
import io
import json
import time
import re


class JsonParser:
    '''Main class of JSON Parser'''
    def __init__(self):
        '''Initializing variables'''
        self.__parsed_string = ''
        self.__user_answers = []
        self.matching_meals = {}

    def open_file(self, path):
        '''Initialize a parsed string data'''
        string_to_parse = ''
        with io.open(path, encoding='utf-8') as json_file:
            for line in json_file:
                string_to_parse += line
        self.__parsed_string = json.loads(string_to_parse)

    def parse_question_file(self, path='JSON files/questions.json'):
        '''Parsing a question file to ask user'''
        self.open_file(path=path)

        for element in self.__parsed_string:
            print("____________________________")
            print(element['QuestionValue'])

            for sub_element in element['Answers']:
                print("{0}: {1}".format(
                    sub_element['AnswerId'],
                    sub_element['AnswerValue']))

            user_answer = input("回答：")
            s = []
            s = re.findall("\d+",user_answer)

            for i in s:
                self.__user_answers.extend(
                    answer['AnswerValue'] for answer in element['Answers']
                      if str(answer['AnswerId']) == i)

        print('------------------------------')
        print("您拥有的食材如下：")
        for answer in self.__user_answers:
            print(answer)
        print('------------------------------')

    def parse_answer_file(self, path='JSON files/answer.json'):
        '''
            Parsing an answer file to compare user's answers with rating system
        '''
        self.open_file(path)
        for element in self.__parsed_string:
            matches = 0
            count = 0
            for tags in element['tags']:
                count += 1
                for ans in self.__user_answers:
                    if str(ans).lower() == str(tags).lower():
                        matches += 1
                    else:
                        continue

            if matches > 0:
                meal = element['meal']
                self.matching_meals[matches] = meal

    def print_matching_tech(self):
        '''This method prints found technology'''
        print("")
        print("正在为您寻找最合适的菜肴...")
        print("")
        time.sleep(1.5)
        print("------------------------------------")
        print("所有合适的选择: ")
        print("")
        time.sleep(0.5)
        for number in self.matching_meals:
            print("菜肴 - {0}, 匹配系数 - {1}".format(
                self.matching_meals[number], number))
            time.sleep(.5)

        print("")
        print("------------------------------------")
        print("这是最适合您的菜肴: {0}".format(
            self.matching_meals[max(self.matching_meals)]))
        print("")


if __name__ == "__main__":
    print("本专家系统旨在根据您拥有的食材选出最适合您烹饪的菜肴，所有选项均可多选！！\n")
    JsonParser = JsonParser()
    JsonParser.parse_question_file()
    JsonParser.parse_answer_file()
    JsonParser.print_matching_tech()
