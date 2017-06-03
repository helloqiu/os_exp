#!/usr/bin/python
# -*- coding: utf-8 -*-

from terminal import handle_input
from termcolor import colored

if __name__ == '__main__':
    print(colored('init', 'yellow'))
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            print(handle_input(l))
