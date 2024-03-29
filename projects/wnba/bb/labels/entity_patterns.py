import re
from extr import RegEx, \
                 RegExLabel

entity_patterns = [
    RegExLabel(
        label='SHOT',
        regexes=[
            RegEx(
                expressions=[
                    r'\b((?:tip|hook|dunk)\s+shot)\b',
                    r'\b(jump\s+bank\s+shot)\b',
                    r'\b(free\s*throw)\b',
                    r'\b(jump\s*shot)\b',
                    r'\b(jumper)\b',
                    r'\b(dunk|shot|layup|pointer)\b'
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
    RegExLabel(
        label='ACTION',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(two|three)\s+point\s+pullup\b',
                    r'\b(two|three)\s+point\b',
                    r'\b(two|three)\b',
                    r'\b(alley\s*oop)\b',
                    r'\b((?:driving|running)\s+(?:pullup|floating))\b',
                    r'\b(step\s*back)\b',
                    r'\b(pullup|floating|driving)\b',
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
    RegExLabel(
        label='QUANTITY',
        regexes=[
            RegEx(
                expressions=[
                    r'\d+',
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
    RegExLabel(
        label='UNITS',
        regexes=[
            RegEx(
                expressions=[
                    r'\bfoot(?:er)?\b',
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
    RegExLabel(
        label='MISS_RIGHT',
        regexes=[
            RegEx(
                expressions=[
                    r'\bmisses\b',
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
    RegExLabel(
        label='BLOCK_RIGHT',
        regexes=[
            RegEx(
                expressions=[
                    r'\bblocks\b',
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
]
