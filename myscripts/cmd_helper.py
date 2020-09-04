import os
import argparse

import router
from libpy import pyutils

def launch_gen_prg(prod):
    target = 'scripts.gen_programs'
    train_data_path = os.path.join(router.data_root, 'train_dataset_1000')
    test_data_path = os.path.join(router.data_root, 'test_dataset_5')

    # check if train and test file already exist
    pyutils.file_exists(train_data_path)
    pyutils.file_exists(test_data_path)

    # make sure there is a space after each following line
    cmd = f'python -m {target} --num_train=1000 --num_test=5 ' \
          f'--train_output_path={train_data_path} ' \
          f'--test_output_path={test_data_path} ' \
          f'--max_train_len=5 --test_lengths="5" --num_workers=8'

    print(f'{cmd}')
    if prod:
        os.system(f'{cmd}')


def launch_model_rb_train(prod):

    target = 'baseline.robustfill.train'
    train_data_path = os.path.join(router.data_root, 'train_dataset_1000')
    model_path = os.path.join(router.data_root, 'model_rb_1000')
    
    # check if model exists
    pyutils.file_exists(model_path)

    # make sure there is a space after each following line
    cmd = f'python -m {target} {train_data_path} {model_path}'
    

    print(f'{cmd}')
    if prod:
        os.system(f'{cmd}')


def launch_gen_prg_from_model(prod):

    for prg_len in [5, 7]:
        target = 'baseline.robustfill.solve_problems'
        prg_path = os.path.join(router.input_root, f'testing_dataset_{prg_len}.txt')
        model_path = os.path.join(router.model_root, 'model_rb_350k/model_rb_350k.39')
        result_path = os.path.join(router.expdata_root, 'model_rb_350k')

        pyutils.dir_choice(dir=result_path)
        result_path = os.path.join(result_path, 'result')

        # make sure there is a space after each following line
        # python3.6 -m scripts.solve_problems dataset result model 60 5 --num_workers=8
        cmd = f'python -m {target} {prg_path} {result_path} {model_path} 60 {prg_len} --num_workers=8'

        print(f'{cmd}')
        if prod:
            os.system(f'{cmd}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--which", required=True, type=int, help="Which program to run?\n"
                                                                 "0: gen_prg\n"
                                                                 "1: train_rb_model\n"
                                                                 "2: test_prg\n")
    parser.add_argument("--prod", default=False, required=False, action='store_true',
                        help="Submit in production cluster.")
    args = parser.parse_args()

    if args.which == 0:
        launch_gen_prg(args.prod)
    elif args.which == 1:
        launch_model_rb_train(args.prod)
    elif args.which == 2:
        launch_gen_prg_from_model(args.prod)

if __name__ == '__main__':
    main()
