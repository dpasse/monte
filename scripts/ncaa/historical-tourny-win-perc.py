import sys
import json


def main():
    output_file = f'./data/ncaa/historical_tourny_win_perc.json'
    historical_probabilities = {
      '1st Round': {
        1: {
          16: 143 / (143 + 1),
        },
        2: {
          15: 135 / (135 + 9),
        },
        3: {
          14: 122 / (122 + 22),
        },
        4: {
          13: 113 / (113 + 31),
        },
        5: {
          12: 93 / (93 + 51),
        },
        6: {
          11: 90 / (90 + 54),
        },
        7: {
          10: 87 / (87 + 57),
        },
        8: {
          9: 71 / (71 + 73),
        },
        9: {
          8: 73 / (73 + 71),
        },
        10: {
          7: 57 / (57 + 87),
        },
        11: {
          6: 54 / (54 + 90),
        },
        12: {
          5: 51 / (51 + 93),
        },
        13: {
          4: 31 / (31 + 113),
        },
        14: {
          3: 22 / (22 + 122),
        },
        15: {
          2: 9 / (9 + 135),
        },
        16: {
          1: 1 / (1 + 143),
        },
      },
      '2nd Round': {
        1: {
          8: 57 / (57 + 14),
          9: 66 / (66 + 6),
        },
        2: {
          7: 57 / (57 + 26),
          10: 34 / (34 + 18),
        },
        3: {
          6: 45 / (45 + 29),
          11: 30 / (30 + 18),
        },
        4: {
          5: 41 / (41 + 33),
          12: 26 / (26 + 13),
        },
        5: {
          4: 33 / (33 + 41),
          13: 16 / (16 + 3),
        },
        6: {
          3: 29 / (45 + 29),
          14: 14 / (14 + 2),
        },
        7: {
          2: 26 / (26 + 57),
          15: 2 / (2 + 2),
        },
        8: {
          1: 14 / (14 + 57),
        },
        9: {
          1: 6 / (6 + 66),
          16: 1 / (1 + 0),
        },
        10: {
          2: 18 / (18 + 34),
          15: 5 / (5 + 0),
        },
        11: {
          3: 18 / (18 + 30),
          14: 6 / (6 + 0),
        },
        12: {
          4: 13 / (13 + 26),
          13: 9 / (9 + 3),
        },
        13: {
          5: 3 / (3 + 16),
          12: 3 / (3 + 9),
        },
        14: {
          6: 2 / (2 + 14),
          11: 0 / (0 + 6),
        },
        15: {
          7: 2 / (2 + 2),
          10: 0 / (0 + 5),
        },
        16: {
          9: 0 / (0 + 1),
        }
      },
      'Sweet Sixteen': {
        1: {
          4: 40 / (40 + 15),
          5: 36 / (36 + 8),
          12: 20 / (20 + 0),
          13: 4 / (4 + 0),
        },
        2: {
          3: 28 / (28 + 17),
          6: 23 / (23 + 6),
          11: 14 / (14 + 3),
        },
        3: {
          2: 17 / (17 + 28),
          7: 9 / (9 + 6),
          10: 9 / (9 + 4),
          15: 2 / (2 + 0),
        },
        4: {
          1: 15 / (15 + 40),
          8: 4 / (4 + 5),
          9: 2 / (2 + 1),
        },
        5: {
          1: 8 / (8 + 36),
          8: 0 / (0 + 2),
          9: 1 / (1 + 2),
        },
        6: {
          1: 2 / (2 + 8),
          4: 1 / (1 + 2),
          5: 0 / (0 + 1),
          8: 0 / (0 + 1),
        },
        7: {
          1: 0 / (0 + 4),
          4: 3 / (3 + 2),
          8: 0 / (0 + 1),
        },
        8: {
          4: 5 / (5 + 4),
          5: 2 / (2 + 0),
          12: 0 / (0 + 2),
          13: 1 / (1 + 0),
        },
        9: {
          4: 1 / (1 + 2),
          5: 2 / (2 + 1),
          13: 1 / (1 + 0),
        },
        10: {
          1: 1 / (1 + 4),
          4: 0 / (0 + 2),
          5: 0 / (0 + 1),
        },
        11: {
          1: 4 / (4 + 4),
        },
        12: {
          1: 0 / (0 + 20),
          8: 0 / (0 + 2),
        },
        13: {
          1: 0 / (0 + 4),
          8: 0 / (0 + 1),
          9: 0 / (0 + 1),
        }
      },
      'Regional Finals': {
        1: {
          2: 23 / (23 + 24),
          3: 16 / (16 + 10),
          6: 8 / (8 + 2),
          7: 4 / (4 + 0),
          10: 4 / (4 + 1),
          11: 4 / (4 + 4),
        },
        2: {
          1: 24 / (24 + 23),
          4: 2 / (2 + 4),
          5: 0 / (0 + 4),
          8: 2 / (2 + 3),
          9: 0 / (0 + 1),
          12: 0 / (0 + 2),
        },
        3: {
          1: 10 / (16 + 10),
          4: 2 / (2 + 3),
          5: 2 / (2 + 1),
          8: 0 / (0 + 1),
          9: 0 / (0 + 2),
        },
        4: {
          2: 4 / (4 + 2),
          3: 3 / (3 + 2),
          6: 2 / (2 + 1),
          7: 2 / (2 + 3),
          10: 2 / (2 + 0),
        },
        5: {
          2: 4 / (4 + 0),
          3: 1 / (1 + 2),
          6: 1 / (1 + 0),
          10: 1 / (1 + 0),
        },
        6: {
          1: 2 / (2 + 8),
          4: 1 / (1 + 2),
          5: 0 / (0 + 1),
          8: 0 / (0 + 1),
        },
        7: {
          1: 0 / (0 + 4),
          4: 3 / (3 + 2),
          8: 0 / (0 + 1),
        },
        8: {
          2: 3 / (3 + 2),
          3: 0 / (0 + 1),
          6: 1 / (1 + 0),
          7: 1 / (1 + 0),
        },
        9: {
          2: 1 / (1 + 0),
          3: 0 / (0 + 2),
          11: 0 / (0 + 1),
        },
        10: {
          1: 1 / (1 + 4),
          4: 0 / (0 + 2),
          5: 0 / (0 + 1),
        },
        11: {
          1: 4 / (4 + 4),
          9: 0 / (0 + 1),
        },
        12: {
          2: 0 / (0 + 2),
        },
      },
    }

    json_string = json.dumps(historical_probabilities, indent=3)
    with open(output_file, 'w') as output:
        output.write(json_string)


if __name__ == '__main__':
    main()
