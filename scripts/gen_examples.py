import os
import json

import router

from dsl.program import Program
from dsl.constraint import get_input_output_examples

from scripts.gen_programs import write_programs_to_file

def get_prg_io(prg):
    return get_input_output_examples(program=prg, num_examples=5, num_tries=1000)

def get_prg(prg_str):
    return Program.parse(prg_str)

def main():
    for prg_len in [5, 7]:
        prg_str_path = os.path.join(router.input_root, f'RPS_cmaes_100_prg_{prg_len}.txt')

        with open(prg_str_path, 'r') as f:
            for prg_id, line in enumerate(f):

                examples = {}
                train_programs = []

                prg = get_prg(prg_str=line.strip('\n'))
                io = get_prg_io(prg=prg)

                # io can be none. Thus taking only not none
                if prg and io:
                    train_programs.append(prg)
                    examples[prg] = io

                    # writing each program to a file
                    prgio_str_path = os.path.join(router.input_root, f'testing_prg/testing_dataset_{prg_len}_{prg_id}.txt')
                    with open(prgio_str_path, 'w') as f:
                        write_programs_to_file(f=f, programs=train_programs, examples=examples)

'''
-> Generate string program from RPS pipeline program
-> Run this script to generate io and program string that accept PCCoder
'''

if __name__ == '__main__':
    main()