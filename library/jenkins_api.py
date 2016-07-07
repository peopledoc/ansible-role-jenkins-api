#!/usr/bin/python
from functools import partial
from ansible.module_utils.basic import *
import jenkins


def _jenkins_api(jenkins_url=None, command=None, args=None, kwargs=None):

    result = {
        'cmd': '{} {} {}'.format(jenkins_url, args, kwargs),
        'changed': False,
        'failed': True,
        'stdout_lines': '',
        'stderr_lines': '',
        'rc': 1
    }

    server = jenkins.Jenkins(jenkins_url)

    if not hasattr(server, command):
        result['stderr_lines'] = ['Unknown command: {}'.format(command)]
        return result

    cmd = partial(getattr(server, command))
    if args:
        cmd = partial(cmd, *args)
    if kwargs:
        cmd = partial(cmd, **kwargs)
    try:
        result['ansible_facts'] = {
            command: cmd()
        }
    except jenkins.JenkinsException as e:
        result['stderr_lines'] = [e.message]
        return result

    result['changed'] = True
    result['failed'] = False
    result['rc'] = 0

    return result


if __name__ == '__main__':
    global module
    module = AnsibleModule(
        argument_spec={
            'jenkins_url': {'required': True},
            'command': {'required': True},
            'args': {'required': False, 'type': 'list'},
            'kwargs': {'required': False, 'type': 'dict'},
        },
        supports_check_mode=False
    )
    module.exit_json(**_jenkins_api(**module.params))
