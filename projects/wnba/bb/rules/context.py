from extr.entities.context import ConTextRule, \
                                  ConTextRuleGroup, \
                                  DirectionType


rule_grouping = ConTextRuleGroup(
    rules=[
        ConTextRule(
            'MISS',
            ['MISS_RIGHT'],
            direction=DirectionType.RIGHT,
            window_size=15
        ),
        ConTextRule(
            'BLOCK',
            ['BLOCK_RIGHT'],
            direction=DirectionType.RIGHT,
            window_size=15
        ),
    ]
)
