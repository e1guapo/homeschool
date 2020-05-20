"""
Generate arithmetic puzzles for solving a phrase (e.g. a limerick).

This is about at the typical second-grade level.

TODO:
- The presentation could definitely use some work.
"""

import re
import sys
import random
import argparse

from pprint import pformat


def gen_problems(digits, string):
    random.seed()
    pattern = re.compile('[\W_]+')
    string = string.lower()
    
    chars = set(pattern.sub('', string))
    max_num = 10**digits - 1
    rand_nums = random.sample(range(9, max_num), len(chars))
    answers = {k: a for k, a in zip(chars, rand_nums)}
    problems = {}
    
    for char, answer in answers.items():
        if random.random() < 0.5:
            # Add
            op = '+'
            top = random.randint(1, answer - 1)
            bot = answer - top
        else:
            # Subtract
            op = '-'
            top = random.randint(answer + 1, max_num + 1)
            bot = top - answer
        problems[char] = ' '.join((str(top), op, str(bot), '='))
    
    # TODO: Add some nice formatting... LaTeX?
    problems = '\n'.join(['{}: {}'.format(k, v) for k,v in problems.items()])
    blanks = '_'.join([str(answers[c]) if c in answers else c for c in string])
    blanks = blanks.replace('\n', '\n\n\n')
    blanks = blanks.replace(' ', '   ')

    worksheet = f'{problems}\n\n\n\n\n{blanks}'
    answers = pformat(answers)
    print(worksheet)
    print(answers)
    return worksheet, answers

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--out_file_name', required=True)
    parser.add_argument('-d', '--digits', required=True, type=int, help='Number of digits to use for problems.')
    args = parser.parse_args()
    with open(args.input_file, 'r') as inf:
        worksheet, key = gen_problems(args.digits, inf.read())
    with open(f'{args.out_file_name}.txt', 'w') as of, open(f'{args.out_file_name}_key.txt', 'w') as af:
        of.write(worksheet)
        af.write(key)

if __name__ == '__main__':
    main()
