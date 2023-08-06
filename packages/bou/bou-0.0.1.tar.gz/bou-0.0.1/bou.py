#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT

import yaml

BUILD_FILES = ['build.yaml', 'build.yml', 'bou.yaml', 'bou.yml']
ENV_VAR = re.compile(r'(\$([A-Za-z0-9_]+))')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', dest='build_file', help='Path to the build file')
    parser.add_argument('stage_or_step', nargs='?', default=None, help='Run a particular stage or step')
    return parser.parse_args()


def setup_env(env, base_path):
    """Set up the environment dictionary, resolving shell variables"""
    if isinstance(env, list):
        env = {pair.split('=')[0]: pair.split('=')[1] for pair in env}
    env = dict(BASE_DIR=str(base_path), **env)
    for key, value in env.items():
        match = ENV_VAR.search(value)
        if match:
            value = value.replace(match.group(1), env[match.group(2)])
            env[key] = value
    return dict(**os.environ, **env)


def setup_step(config, step_name):
    """Prepare a step for usage"""
    step = config['steps'][step_name]
    step['environment'] = config.get('environment', []) + step.get('environment', [])
    return step


def get_steps_for_stage(config, stage_name):
    steps = []
    for step_name in config['steps'].keys():
        if config['steps'][step_name]['stage'] == stage_name:
            steps.append(setup_step(config, step_name))
    return steps


def run_step(step, base_path):
    script = step['script']
    if isinstance(script, list):
        script = os.linesep.join(script)
    env = setup_env(step['environment'], base_path)
    proc = Popen([script], shell=True, stdout=PIPE, stderr=STDOUT, env=env)
    for output in iter(lambda: proc.stdout.read(1), b''):
        sys.stdout.buffer.write(output)
        sys.stdout.buffer.flush()
    return proc.returncode == 0


def run_stage(config, stage_name, base_path):
    for step in get_steps_for_stage(config, stage_name):
        result = run_step(step, base_path)
        if not result:
            break


def get_build_file():
    """Determine the local build file"""
    base_path = Path.cwd()
    for child in base_path.iterdir():
        if child.name in BUILD_FILES:
            return child.resolve()
    return None


def main():
    """Run the build system"""
    args = parse_args()
    if args.build_file:
        build_file = Path(args.build_file).resolve()
    else:
        build_file = get_build_file()
    if not build_file:
        print('Could not find a valid build file')
        return 1
    base_path = build_file.parent
    config = yaml.full_load(build_file.open())
    if args.stage_or_step:
        if args.stage_or_step in config['stages']:
            run_stage(config, args.stage_or_step, base_path)
        elif args.stage_or_step in config['steps'].keys():
            step = setup_step(config, args.stage_or_step)
            run_step(config, step, base_path)
        else:
            print('"{stage}" is not a valid stage or step name'.format(stage=args.stage_or_step))
            return 2
    else:
        for stage_name in config['stages']:
            run_stage(config, stage_name, base_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
