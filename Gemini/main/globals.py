'''
Created on 23 gen 2022

@author: david
'''


def echo_message(s):
    print(s)


def check_locals(dic):
    for key, value in dic.items():
        print(key + " = " + str(value))
        if value is None:
            raise Exception("Argument " + key + " = None")
