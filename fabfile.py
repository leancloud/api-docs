import os

from fabric.api import run, sudo, env, cd, local, prefix, put, lcd, settings
from fabric.contrib.files import exists, sed
from fabric.contrib.project import rsync_project

env.use_ssh_config = True

user = 'deploy'
remote_doc_dir = '/var/www/avoscloud-api-docs'

project_dir = "."
dist = 'debian'
host_count = len(env.hosts)

def _set_user_dir():
    global dist,user,remote_doc_dir
    with settings(warn_only=True):
        issue = run('id ubuntu').lower()
        if 'id: ubuntu' in issue:
            dist = 'debian'
        elif 'uid=' in issue:
            dist = 'ubuntu'
            user = 'ubuntu'
            remote_doc_dir = '/mnt/avos/avoscloud-api-docs'

def prepare_remote_dirs(remote_dir):
    _set_user_dir()
    if not exists(remote_dir):
        sudo('mkdir -p %s' % remote_dir)
    sudo('chown %s %s' % (user, remote_dir))

def deploy_docs():
    global host_count
    _set_user_dir()

    prepare_remote_dirs(remote_doc_dir)
    rsync_project(local_dir='api/',
                  remote_dir=remote_doc_dir,
                  delete=True)
    host_count -= 1
    if (host_count == 0):
        print("Finished to public api docs!")
