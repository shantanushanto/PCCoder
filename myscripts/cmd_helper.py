import os
import argparse

import router
from libpy import pyutils

def launch_gen_prg(prod):
    target = 'scripts.gen_programs'
    train_data_path = os.path.join(router.data_root, 'train_dataset_1000')
    test_data_path = os.path.join(router.data_root, 'test_dataset_500')

    # check if train and test file already exist
    pyutils.file_exists(train_data_path)
    pyutils.file_exists(test_data_path)

    # make sure there is a space after each following line
    cmd = f'python -m {target} --num_train=1000 --num_test=500 ' \
          f'--train_output_path={train_data_path} ' \
          f'--test_output_path={test_data_path} ' \
          f'--max_train_len=5 --test_lengths="5" --num_workers=8'

    print(f'{cmd}')
    if prod:
        os.system(f'{cmd}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--which", required=True, type=int, help="Which program to run?\n"
                                                                 "0: gen_prg\n")
    parser.add_argument("--prod", default=False, required=False, action='store_true',
                        help="Submit in production cluster.")
    args = parser.parse_args()

    if args.which == 0:
        launch_gen_prg(args.prod)

if __name__ == '__main__':
    main()