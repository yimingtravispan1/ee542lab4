#!/usr/bin/env python3
import sys

for line in sys.stdin:
    for ch in line.rstrip('\r\n'):
        print(f"{ord(ch)}\t1")
