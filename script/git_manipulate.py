#!/usr/bin/env python

with open(".gitmodules") as file:
    txt = file.readlines()
    for line in txt:
        if line[:7] == "\turl = ":
            # TODO support when git/ssh
            print(line[7:])
