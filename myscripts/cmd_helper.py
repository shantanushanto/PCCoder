import os
import argparse

import router
from libpy import pyutils, JobLauncher, commonutils

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


def launch_gen_prg_from_model(cluster='palab', prod=False, atlas_ratio=4):
    # dir to save data in
    data_dir = os.path.join(router.expdata_root, 'model_rb_individual')  # as there are different nn but fitness function name is nn, use different directory
    data_dir = pyutils.dir_choice(data_dir)  # dir checking

    # create multiple run tasks for batch submission
    def batch_generator():
        tasks = []

        for tm_limit in [60, 60*30, 60*60]:
            for prg_len in [5, 7]:
                for prg_id in range(100):
                    target = 'baseline.robustfill.solve_problems'
                    prg_path = os.path.join(router.input_root, f'testing_prg/testing_dataset_{prg_len}_{prg_id}.txt')
                    model_path = os.path.join(router.model_root, 'model_rb_350k/model_rb_350k.39')
                    result_path = os.path.join(data_dir, f'result_{tm_limit}_{prg_len}_{prg_id}.log')

                    # for module run we need full path
                    py_module = f'PYTHONPATH={router.project_root}'
                    cmd = f'{py_module} python -m {target} {prg_path} {result_path} {model_path} {tm_limit} {prg_len} --num_workers=1'

                    task = JobLauncher.Task(cmd=cmd, out=result_path)
                    tasks.append(task)

        return tasks

    # callback to use
    callback_batch_gen = JobLauncher.TaskGenerator(batch_generator=batch_generator, data_dir=data_dir).get_callback_batch_gen()

    sbatch_extra_cmd = 'conda activate pccoder\n'
    if cluster=='palab':  # ignoring gpu node as it is creating problem with tensor gpu
        sbatch_extra_cmd = f'#SBATCH --exclude=gpu01\n\n{sbatch_extra_cmd}'

    # launch job in cluster
    JobLauncher.launch_job(cluster=cluster, callback_batch_gen=callback_batch_gen, job_name='cmaes_bin', submission_check=not prod,
               acc_id=122818927574, time='15:00:00', atlas_ratio=atlas_ratio, sbatch_extra_cmd=sbatch_extra_cmd, no_exlude_node=0)

    # create readme file in the folder to easy remember
    commonutils.readme(data_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--which", required=True, type=int, help="Which program to run?\n"
                                                                 "0: gen_prg\n"
                                                                 "1: train_rb_model\n"
                                                                 "2: test_prg\n")
    parser.add_argument("--cluster", default='palab', choices=['palab', 'tamulauncher', 'atlas'], required=False,
                        help="Cluster name.")
    parser.add_argument("--prod", default=False, required=False, action='store_true',
                        help="Submit in production cluster.")

    parser.add_argument("--atlas_ratio", default=4, required=False, help="Atlas ratio if needed", type=int)

    args = parser.parse_args()

    if args.which == 0:
        launch_gen_prg(args.prod)
    elif args.which == 1:
        launch_model_rb_train(args.prod)
    elif args.which == 2:
        launch_gen_prg_from_model(cluster=args.cluster, prod=args.prod, atlas_ratio=args.atlas_ratio)


if __name__ == '__main__':
    main()
