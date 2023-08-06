import subprocess, os
from contextlib import contextmanager
import copy
import time

@contextmanager
def pyshell_with_values(pyshell, new_params_kwargs = {}):
    pyshell_copy = copy.deepcopy(pyshell)

    for (k, v) in new_params_kwargs.items():
        setattr(pyshell_copy, k, v)
    
    yield pyshell_copy


class ShellRunner:
    class CommandFailed(Exception):
        pass

    class CommandResult:
        def __init__(self, output, exit_code):
            self.output, self.exit_code = output, exit_code
        
        def __str__(self):
            if self.output:
                return self.output
            else:
                return ''

    def __init__(
        self,
        raise_error_on_command_fail=True,
        env=None,
        dry_run=False,
        cwd=None,
        verbosity=0,
        accepted_exit_codes=[0]):
        self.raise_error_on_command_fail=raise_error_on_command_fail
        self.env=env
        self.dry_run = ('PYSHELLRUNNER_DRY_RUN' in os.environ) or dry_run
        self.cwd = cwd
        env_verbosity = os.environ.get('PYSHELLRUNNER_VERBOSITY', verbosity)
        self.verbosity = int(env_verbosity)
        self.accepted_exit_codes = accepted_exit_codes

    def run(self, cmd, *args, **kwargs):
        params = self.__dict__.copy()
        params.update(kwargs)
        output = ""

        if params['verbosity'] > 0 or params['dry_run']:
            print('\__ \033[92m' + cmd + '\033[0m' + f" (cwd: {params['cwd']})\n")

        if not params['dry_run']:
            process = subprocess.Popen(
                cmd,
                cwd=params['cwd'],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=params['env']
            )

            while process.poll() is None:
                for line in process.stdout:
                    output += line.decode('utf-8')

                    if params['verbosity'] > 1:
                            print(line.decode('utf8'), end='')

                time.sleep(0.1)

            ret = ShellRunner.CommandResult(
                output=output,
                exit_code=process.returncode
            )

            if (not ret.exit_code in params['accepted_exit_codes']) and params['raise_error_on_command_fail']:
                raise ShellRunner.CommandFailed(f"command: {cmd} output: {ret.output}\n\n, exit_code: {ret.exit_code}")

            return ret
        else:
            return None


def run(cmd, *args, **kwargs):
    return ShellRunner(*args, **kwargs).run(cmd)
