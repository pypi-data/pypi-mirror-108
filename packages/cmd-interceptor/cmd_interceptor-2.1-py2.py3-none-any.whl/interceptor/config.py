import copy
import os
import sys
import typing as tp
import warnings

import pkg_resources
from satella.coding import for_argument
from satella.json import read_json_from_file, write_json_to_file


class Configuration:
    @property
    def path(self) -> str:
        return os.path.join('/etc/interceptor.d', self.app_name)

    def __init__(self, args_to_disable: tp.Optional[tp.List[str]] = None,
                 args_to_append: tp.Optional[tp.List[str]] = None,
                 args_to_prepend: tp.Optional[tp.List[str]] = None,
                 args_to_replace: tp.Optional[tp.List[tp.Tuple[str, str]]] = None,
                 display_before_start: bool = False,
                 notify_about_actions: bool = False,
                 app_name: tp.Optional[str] = None,
                 deduplication: bool = False,
                 log: bool = False):
        self.args_to_disable = args_to_disable or []
        self.args_to_append = args_to_append or []
        self.args_to_prepend = args_to_prepend or []
        self.args_to_replace = args_to_replace or []
        self.display_before_start = display_before_start
        self.notify_about_actions = notify_about_actions
        self.app_name = app_name
        self.deduplication = deduplication
        self.log = log

    def to_json(self):
        return {'args_to_disable': self.args_to_disable,
                'args_to_append': self.args_to_append,
                'args_to_prepend': self.args_to_prepend,
                'args_to_replace': self.args_to_replace,
                'display_before_start': self.display_before_start,
                'notify_about_actions': self.notify_about_actions,
                'deduplication': self.deduplication,
                'log': self.log}

    @for_argument(None, copy.copy)
    def modify(self, args, *extra_args):
        process, *arguments = args
        for arg_to_take_away in self.args_to_disable:
            while arg_to_take_away in arguments:
                if self.notify_about_actions:
                    print('interceptor(%s): taking away %s' % (self.app_name, arg_to_take_away))
                del arguments[arguments.index(arg_to_take_away)]

        for arg_to_replace, arg_to_replace_with in self.args_to_replace:
            while arg_to_replace in arguments:
                if self.notify_about_actions:
                    print('interceptor(%s): replacing %s with %s' % (self.app_name, arg_to_replace,
                                                                     arg_to_replace_with))
                arguments[arguments.index(arg_to_replace)] = arg_to_replace_with

        for arg_to_append in self.args_to_append:
            if arg_to_append not in arguments:
                if self.notify_about_actions:
                    print('interceptor(%s): appending %s' % (self.app_name, arg_to_append))
                arguments.append(arg_to_append)

        for arg_to_prepend in reversed(self.args_to_prepend):
            if arg_to_prepend not in arguments:
                if self.notify_about_actions:
                    print('interceptor(%s): prepending %s' % (self.app_name, arg_to_prepend))
                arguments = [arg_to_prepend] + arguments

        if self.deduplication:
            new_arguments = []
            added_args = {}
            for arg in arguments:
                if arg not in added_args:
                    new_arguments.append(arg)
                    added_args.add(arg)
            arguments = new_arguments

        if self.display_before_start:
            print('%s %s' % (sys.argv[0], ' '.join(arguments)))

        if self.log:
            if not os.path.exists('/var/log/interceptor.d'):
                os.mkdir('/var/log/interceptor.d')
            with open(os.path.join('/var/log/interceptor.d', sys.argv[0], 'a')) as f_out:
                f_out.write(' '.join(arguments))

        return [process, *arguments]

    def save(self):
        write_json_to_file(self.path, self.to_json(), sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, dct, app_name: str):
        prepend = dct.get('args_to_prepend')
        if prepend is None:
            prepend = dct.get('args_to_append_before')
            if prepend is not None:
                warnings.warn('args_to_append_before is deprecated, use args_to_prepend',
                              DeprecationWarning)
        take_away = dct.get('args_to_disable')
        if take_away is None:
            take_away = dct.get('args_to_take_away')
            if take_away is not None:
                warnings.warn('args_to_take_away is deprecated, use args_to_prepend',
                              DeprecationWarning)

        return Configuration(take_away,
                             dct.get('args_to_append'),
                             prepend,
                             dct.get('args_to_replace'),
                             dct.get('display_before_start', False),
                             dct.get('notify_about_actions', False),
                             app_name=app_name,
                             deduplication=dct.get('deduplication', False),
                             log=dct.get('log', False))


def assert_correct_version(version: str) -> None:
    if version == '':
        # print('You have used an older version of interceptor to intercept this command.\n'
        #       'It is advised to undo the interception and reintercept the call to upgrade.')
        return
    my_version = pkg_resources.require('interceptor')[0].version
    if int(version.split('.')[0]) > int(my_version.split('.')[0]):
        sys.stderr.write('You have intercepted this call using a higher version of Interceptor. \n'
                         'This might not work as advertised. Try undo\'ing the interception \n'
                         'and intercepting this again.\n'
                         'Aborting.')
        sys.exit(1)


def load_config_for(name: str, version: tp.Optional[str] = '') -> Configuration:
    if version is not None:
        assert_correct_version(version)

    file_name = os.path.join('/etc/interceptor.d', name)
    if not os.path.isfile(file_name):
        print('Configuration for %s does not exist or is not a file' % (name,))
        sys.exit(1)

    cfg = Configuration.from_json(read_json_from_file(file_name), app_name=name)
    return cfg
