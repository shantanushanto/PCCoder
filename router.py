import os
from libpy.pyutils import mkdir_p

def fix_root(project_name='PCCoder'):
    root = os.getcwd()
    first, last = os.path.split(root)
    if last==project_name:
        return root
    else:
        return first

# project_root = os.getcwd()
project_root = fix_root()

data_root = os.path.join(project_root, 'data') # all data
model_root = os.path.join(data_root, 'model')  # ml model
fig_root = os.path.join(data_root, 'fig')  # figure
bigdata_root = os.path.join(data_root, 'big')  # big size data
expdata_root = os.path.join(data_root, 'exp')  # experimental data
input_root = os.path.join(data_root, 'input')  # input to program. e.g. programs, io examples
tmp_root = os.path.join(data_root, 'tmp')

job_dir = os.path.join(project_root, '.job')  # jobs

# conference submission folder
conf_root = os.path.join(data_root, 'conf')  # conference data root
nips20 = os.path.join(conf_root, 'nips20')

# creating all directory
for folder in [data_root, model_root, fig_root, bigdata_root, expdata_root, input_root, job_dir, tmp_root,
               conf_root, nips20]:
    mkdir_p(folder)