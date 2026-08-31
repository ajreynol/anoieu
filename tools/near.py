#!/usr/bin/env python3
"""Print 1 when two repo ids are one edit apart, 0 otherwise.

Its only caller is `scripts/prompts/welcome_eo`, which uses it to refuse a repo id that
looks like a typo of one already recorded. Membership in the ecosystem is not a
thing to corrupt by mistyping a name, and the cost of asking is a flag.
"""
import sys

a, b = sys.argv[1], sys.argv[2]
if abs(len(a) - len(b)) > 1 or a == b:
    print(0)
    raise SystemExit
d = [[j if i == 0 else (i if j == 0 else 0) for j in range(len(b) + 1)]
     for i in range(len(a) + 1)]
for i in range(1, len(a) + 1):
    for j in range(1, len(b) + 1):
        d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                      d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
        # transposition counts as one edit: `koien` for `koine` is the typo
        # people actually make, and plain Levenshtein scores it as two.
        if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
            d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
print(1 if d[-1][-1] == 1 else 0)
