#! /usr/bin/env python3

import configparser
import sys

DEFAULT_ACCELS = [
    ('delete', 'Delete'),
    ('page-format', 'c'),
    ('rotate(90)', '<Ctrl>Right'),
    ('rotate(-90)', '<Ctrl>Left'),
    ('save', '<Ctrl>s'),
    ('save-as', '<Ctrl><Shift>s'),
    ('export-selection(2)', '<Ctrl>e'),
    ('export-all', '<Ctrl><Shift>e'),
    ('quit', '<Ctrl>q'),
    ('import', '<Ctrl>o'),
    ('zoom(5)', ['plus', 'KP_Add']),
    ('zoom(-5)', ['minus', 'KP_Subtract']),
    ('undo', '<Ctrl>z'),
    ('redo', '<Ctrl>y'),
    ('cut', '<Ctrl>x'),
    ('copy', '<Ctrl>c'),
    ('paste(0)', '<Ctrl>v'),
    ('paste(1)', '<Ctrl><Shift>v'),
    ('select(0)', '<Ctrl>a'),
    ('select(1)', '<Ctrl><Shift>a'),
    ('main-menu', 'F10'),
]
parser = configparser.ConfigParser()
parser.add_section('accelerators')
s = parser['accelerators']
for k, v in DEFAULT_ACCELS:
     s[k] = v if isinstance(v, str) else " ".join(v)
with open("titi.ini", "w") as f:
    parser.write(f)
parser = configparser.ConfigParser()
parser.read("titi.ini")
accels=[]
for k, v in parser['accelerators'].items():
     accels.append((k, v.split() if " " in v else v,))
print(accels)
