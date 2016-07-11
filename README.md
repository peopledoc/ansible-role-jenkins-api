novafloss.jenkins-api
=====================

Install jenkins-python + include ansible binding module.

Here is the exhaustive list of available api commands:

    - http://python-jenkins.readthedocs.io/en/latest/api.html

Requirements
------------

None

Dependencies
------------

None but we recommend to include `FGtatsuro.python-requirements` in your
playbook first to ensure `pip` is uptodate and `requests` install won't break
it.

Role Variables
--------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - hosts: slave
      roles:
        - FGtatsuro.python-requirements
        - novafloss.jenkins-api
      tasks:
        - jenkins_credentials:
            jenkins_url: https://jenkins.mycompany.com/
            name: github-https
            cls: com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl
            args:
              - Allow github https cloning
              - my github token
              - 816a8c3f0130e8b3a83ac65a5e4d1f26e121863e
        - jenkins_api:
            jenkins_url: https://jenkins.mycompany.com/
            command: node_exists
            args:
              - node-1
          register: result
        - debug:
            var: result.node_exists

*Note:* `jenkins-api` module put the api result dictionary with the command
name as key. For example, the previous task result is stored as
`result.node_exists`.

Copyright
---------

Licensed under BSD by @PeopleDoc and contributors.
