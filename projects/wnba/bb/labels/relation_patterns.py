from extr import RegExRelationLabelBuilder

relation_patterns = [
    RegExRelationLabelBuilder('is_units_of') \
        .add_e1_to_e2(
            e1='QUANTITY',
            relation_expressions=[
                r'\s*(-)\s*',
            ],
            e2='UNITS'
        ) \
        .build(),
    RegExRelationLabelBuilder('is_out_of') \
        .add_e1_to_e2(
            e1='QUANTITY',
            relation_expressions=[
                r'\s+(of)\s+',
            ],
            e2='QUANTITY'
        ) \
        .build(),
    RegExRelationLabelBuilder('is_of_type') \
        .add_e2_to_e1(
            e2='ACTION',
            relation_expressions=[
                r'\s+',
            ],
            e1='SHOT'
        ) \
        .build(),
]