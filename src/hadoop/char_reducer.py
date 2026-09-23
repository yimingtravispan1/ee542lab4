#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    code, val = line.strip().split('\t')
    counts[int(code)] += int(val)

for code in sorted(counts):
    print(f"U+{code:04X}\t{counts[code]}")
