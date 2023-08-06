# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdp_playground',
 'mdp_playground.analysis',
 'mdp_playground.config_processor',
 'mdp_playground.envs',
 'mdp_playground.scripts',
 'mdp_playground.spaces']

package_data = \
{'': ['*']}

install_requires = \
['atari-py==0.2.5',
 'colorama>=0.4.4,<0.5.0',
 'dill>=0.3.3,<0.4.0',
 'gym[atari]==0.14.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.19.5,<2.0.0']

extras_require = \
{'extras': ['pandas==0.25.0',
            'requests==2.22.0',
            'configspace==0.4.10',
            'scipy>=1.3.0,<2.0.0',
            'pillow>=6.1.0,<7.0.0',
            'tensorflow==2.2.0',
            'ray[rllib,debug,default]>=1.3.0,<2.0.0'],
 'extras_cont': ['pandas==0.25.0',
                 'requests==2.22.0',
                 'configspace==0.4.10',
                 'scipy>=1.3.0,<2.0.0',
                 'tensorflow-probability==0.9.0',
                 'mujoco-py==2.0.2.13'],
 'extras_disc': ['pandas==0.25.0',
                 'requests==2.22.0',
                 'configspace==0.4.10',
                 'scipy>=1.3.0,<2.0.0',
                 'pillow>=6.1.0,<7.0.0'],
 'extras_test': ['pandas==0.25.0',
                 'requests==2.22.0',
                 'configspace==0.4.10',
                 'scipy>=1.3.0,<2.0.0',
                 'tensorflow-probability==0.9.0']}

entry_points = \
{'console_scripts': ['run-mdpp-experiments = '
                     'mdp_playground.scripts.run_experiments:cli']}

setup_kwargs = {
    'name': 'mdp-playground',
    'version': '0.0.2',
    'description': 'A python package to design and debug RL agents',
    'long_description': '<p align="center">\n\n<a href="https://github.com/automl/mdp-playground/actions/workflows/gh-test.yml" target="_blank">\n    <img src="https://github.com/automl/mdp-playground/actions/workflows/gh-test.yml/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/automl/mdp-playground/actions/workflows/publish.yml" target="_blank">\n    <img src="https://github.com/automl/mdp-playground/actions/workflows/publish.yml/badge.svg" alt="Publish">\n</a>\n<a href="https://codecov.io/gh/automl/mdp-playground" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/automl/mdp-playground?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/mdp-playground/" target="_blank">\n    <img src="https://img.shields.io/pypi/v/mdp-playground?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/mdp-playground/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/mdp-playground.svg" alt="Python Versions">\n</a>\n</p>\n\n\n# MDP Playground\nA python package to inject low-level dimensions of difficulties in RL environments. There are toy environments to design and debug RL agents. And complex environment wrappers for Atari and Mujoco to test robustness to these dimensions in complex environments.\n\n## Getting started\nThere are 4 parts to the package:\n1) **Toy Environments**: The base toy Environment in [`mdp_playground/envs/rl_toy_env.py`](mdp_playground/envs/rl_toy_env.py) implements the toy environment functionality, including discrete and continuous environments, and is parameterised by a `config` dict which contains all the information needed to instantiate the required MDP. Please see [`example.py`](example.py) for some simple examples of how to use the MDP environments in the package. For further details, please refer to the documentation in [`mdp_playground/envs/rl_toy_env.py`](mdp_playground/envs/rl_toy_env.py).\n\n2) **Complex Environment Wrappers**: Similar to the toy environment, this is parameterised by a `config` dict which contains all the information needed to inject the dimensions into Atari or Mujoco environments. Please see [`example.py`](example.py) for some simple examples of how to use these. The Atari wrapper is in [`mdp_playground/envs/gym_env_wrapper.py`](mdp_playground/envs/gym_env_wrapper.py) and the Mujoco wrapper is in [`mdp_playground/envs/mujoco_env_wrapper.py`](mdp_playground/envs/mujoco_env_wrapper.py).\n\n3) **Experiments**: Experiments are launched using [`run_experiments.py`](run_experiments.py). Config files for experiments are located inside the [`experiments`](experiments) directory. Please read the [instructions](#running-experiments) below for details.\n\n4) **Analysis**: [`plot_experiments.ipynb`](plot_experiments.ipynb) contains code to plot the standard plots from the paper.\n\n## Installation\n\n### Production use\nWe recommend using `conda` to manage environments. After setup of the environment, you can install MDP Playground in two ways:\n#### Manual\nTo install MDP Playground manually, clone the repository and run:\n```bash\npip install -e .[extras]\n```\nThis might be the preferred way if you want easy access to the included experiments.\n\n#### From PyPI\nMDP Playground is also on PyPI. Just run:\n```bash\npip install mdp_playground[extras]\n```\n\n\n### Reproducing results from the paper\nWe recommend using `conda` environments to manage virtual `Python` environments to run the experiments. Unfortunately, you will have to maintain 2 environments - 1 for the "older" **discrete toy** experiments and 1 for the "newer" **continuous and complex** experiments from the paper. As mentioned in Appendix P in the paper, this is because of issues with Ray, the library that we used for our baseline agents.\n\nPlease follow the following commands to install for the discrete toy experiments:\n```bash\nconda create -n py36_toy_rl_disc_toy python=3.6\nconda activate py36_toy_rl_disc_toy\ncd mdp-playground\npip install -e .[extras_disc]\n```\n\nPlease follow the following commands to install for the continuous and complex experiments:\n```bash\nconda create -n py36_toy_rl_cont_comp python=3.6\nconda activate py36_toy_rl_cont_comp\ncd mdp-playground\npip install -e .[extras_cont]\nwget \'https://ray-wheels.s3-us-west-2.amazonaws.com/master/8d0c1b5e068853bf748f72b1e60ec99d240932c6/ray-0.9.0.dev0-cp36-cp36m-manylinux1_x86_64.whl\'\npip install ray-0.9.0.dev0-cp36-cp36m-manylinux1_x86_64.whl[rllib,debug]\n```\n\n## Running experiments\nFor reproducing experiments from the main paper, please see [below](#running-experiments-from-the-main-paper).\n\nFor general instructions, please continue reading.\n\nYou can run experiments using:\n```\nrun-mdpp-experiments -c <config_file> -e <exp_name> -n <config_num>\n```\nThe `exp_name` is a prefix for the filenames of CSV files where stats for the experiments are recorded. The CSV stats files will be saved to the current directory.<br>\nEach of the command line arguments has defaults. Please refer to the documentation inside [`run_experiments.py`](run_experiments.py) for further details on the command line arguments. (Or run it with the `-h` flag to bring up help.)\n\nThe config files for experiments from the [paper](https://arxiv.org/abs/1909.07750) are in the experiments directory.<br>\nThe name of the file corresponding to an experiment is formed as: `<algorithm_name>_<dimension_names>.py`<br>\nSome sample `algorithm_name`s are: `dqn`, `rainbow`, `a3c`, `a3c_lstm`, `ddpg`, `td3` and `sac`<br>\nSome sample `dimension_name`s are: `seq_del` (for **delay** and **sequence length** varied together), `p_r_noises` (for **P** and **R noises** varied together),\n`target_radius` (for varying **target radius**) and `time_unit` (for varying **time unit**)<br>\nFor example, for algorithm **DQN** when varying dimensions **delay** and **sequence length**, the corresponding experiment file is [`dqn_seq_del.py`](experiments/dqn_seq_del.py)\n\n## Running experiments from the main paper\nWe list here the commands for the experiments from the main paper:\n```bash\n# Discrete toy environments:\n# Image representation experiments:\nconda activate py36_toy_rl_disc_toy\npython run_experiments.py -c experiments/dqn_image_representations.py -e dqn_image_representations\npython run_experiments.py -c experiments/rainbow_image_representations.py -e rainbow_image_representations\npython run_experiments.py -c experiments/a3c_image_representations.py -e a3c_image_representations\npython run_experiments.py -c experiments/dqn_image_representations_sh_quant.py -e dqn_image_representations_sh_quant\n\n# Continuous toy environments:\nconda activate py36_toy_rl_cont_comp\npython run_experiments.py -c experiments/ddpg_move_to_a_point_time_unit.py -e ddpg_move_to_a_point_time_unit\npython run_experiments.py -c experiments/ddpg_move_to_a_point_irr_dims.py -e ddpg_move_to_a_point_irr_dims\n# Varying the action range and time unit together for transition_dynamics_order = 2\npython run_experiments.py -c experiments/ddpg_move_to_a_point_p_order_2.py -e ddpg_move_to_a_point_p_order_2\n\n# Complex environments:\nconda activate py36_toy_rl_cont_comp\npython run_experiments.py -c experiments/dqn_qbert_del.py -e dqn_qbert_del\npython run_experiments.py -c experiments/ddpg_halfcheetah_time_unit.py -e ddpg_halfcheetah_time_unit\n\n# For the spider plots, experiments for all the agents and dimensions will need to be run from the experiments directory, i.e., for discrete: dqn_p_r_noises.py, a3c_p_r_noises, ..., dqn_seq_del, ..., dqn_sparsity, ..., dqn_image_representations, ...\n# for continuous:, ddpg_move_to_a_point_p_noise, td3_move_to_a_point_p_noise, ..., ddpg_move_to_a_point_r_noise, ..., ddpg_move_to_a_point_irr_dims, ..., ddpg_move_to_a_point_action_loss_weight, ..., ddpg_move_to_a_point_action_max, ..., ddpg_move_to_a_point_target_radius, ..., ddpg_move_to_a_point_time_unit\n# and then follow the instructions in plot_experiments.ipynb\n\n# For the bsuite debugging experiment, please run the bsuite sonnet dqn agent on our toy environment while varying reward density. Commit https://github.com/deepmind/bsuite/commit/5116216b62ce0005100a6036fb5397e358652530 should work fine.\n```\n\nThe CSV stats files will be saved to the current directory and can be analysed in [`plot_experiments.ipynb`](plot_experiments.ipynb).\n\n## Plotting\nTo plot results from experiments, run `jupyter-notebook` and open [`plot_experiments.ipynb`](plot_experiments.ipynb) in Jupyter. There are instructions within each of the cells on how to generate and save plots.\n\n## Citing\nIf you use MDP Playground in your work, please cite the following paper:\n\n```bibtex\n@article{rajan2020mdp,\n      title={MDP Playground: Controlling Dimensions of Hardness in Reinforcement Learning},\n      author={Raghu Rajan and Jessica Lizeth Borja Diaz and Suresh Guttikonda and Fabio Ferreira and André Biedenkapp and Frank Hutter},\n      year={2020},\n      eprint={1909.07750},\n      archivePrefix={arXiv},\n      primaryClass={cs.LG}\n}\n```\n',
    'author': 'Raghu Rajan',
    'author_email': 'rajanr@cs.uni-freiburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://automl.github.io/mdp-playground',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
