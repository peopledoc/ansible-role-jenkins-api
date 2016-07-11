#!/usr/bin/python
from ansible.module_utils.basic import *
import jenkins


create_credential_groovy = u"""
import jenkins.*;
import jenkins.model.*;
import hudson.*;
import hudson.model.*;

import com.cloudbees.plugins.credentials.domains.Domain;
import com.cloudbees.plugins.credentials.CredentialsScope;

domain = Domain.global()
store = Jenkins.instance.getExtensionList(
  'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
)[0].getStore()

credentials_new = new {cls}(
  CredentialsScope.GLOBAL, "{name}",
  {args}
)

creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
      {cls}.class, Jenkins.instance
);
updated = false;

for (credentials_current in creds) {{
  // Comparison does not compare passwords but identity.
  if (credentials_new == credentials_current) {{
    store.removeCredentials(domain, credentials_current);
    ret = store.addCredentials(domain, credentials_new)
    updated = true;
    println("OVERWRITTEN");
    break;
  }}
}}

if (!updated) {{
  ret = store.addCredentials(domain, credentials_new)
  if (ret) {{
    println("CREATED");
  }} else {{
    println("FAILED");
  }}
}}
"""  # noqa


def render_create_credentials_script(name=None,
                                     cls=None,
                                     args=None):
    return create_credential_groovy.format(
        args=', '.join([a if a.startswith('new ') else '"{}"'.format(a)
                        for a in args]),
        cls=cls,
        name=name,
    )


def _jenkins_credentials(jenkins_url=None, **kwargs):

    result = {
        'cmd': jenkins_url,
        'changed': False,
        'failed': True,
        'msg': '',
        'rc': 1
    }

    server = jenkins.Jenkins(jenkins_url)

    groovy = render_create_credentials_script(**kwargs)
    result['cmd'] += ' {}'.format(groovy)

    try:
        output = server.run_script(groovy)
        if 'Error' in output or 'Exception' in output:
            result['msg'] = output
            return result

    except jenkins.JenkinsException as e:
        result['msg'] = e.message
        return result

    result['jenkins_credentials'] = output
    result['changed'] = True
    result['failed'] = False
    result['rc'] = 0

    return result

if __name__ == '__main__':
    global module
    module = AnsibleModule(
        argument_spec={
            'jenkins_url': {'required': True},
            'cls': {'required': True},
            'name': {'required': True},
            'args': {'required': False, 'type': 'list'},
        },
        supports_check_mode=False
    )
    module.exit_json(**_jenkins_credentials(**module.params))
