#!/usr/bin/python3
# Fabric script that does the full deployment to both servers using deploy()

from fabric.api import local, put, env, run
from datetime import datetime
import os.path

env.user = 'ubuntu'
env.hosts = ['3.84.255.71', '54.236.48.24']

date = datetime.now().strftime("%Y%m%d%H%M%S")
file_path = "versions/web_static_{}.tgz".format(date)


def do_pack():
    """generates .tgz archive from a folder"""
    if os.path.isdir('versions') is False:
        local('mkdir versions')

    local('tar -cvzf ' + file_path + ' web_static')

    if os.path.exists(file_path):
        return file_path
    return None


def do_deploy(archive_path):
    """Distribute archive to servers"""
    if os.path.exists(archive_path) is False:
        return False

    name = archive_path.split('/')
    n_name = name[1]
    m_name = n_name.split('.')
    new_name = m_name[0]

    upload = "/tmp/" + n_name
    arch_fold = "/data/web_static/release/" + new_name

    put(archive_path, upload)

    run('mkdir -p ' + arch_fold)
    run('tar -xzf /tmp/{} -C {}/'.format(n_name, arch_fold))
    run('rm {}'.format(upload))

    move = 'mv ' + arch_fold + '/web_static/* ' + arch_fold + '/'
    run(move)

    run('rm -fr ' + arch_fold + '/web_static')
    run('rm -fr /data/web_static/current')
    run('ln -s ' + arch_fold + ' /data/web_static/current')
    return True


def deploy():
    """Does the full deploy by calling the above functions"""
    path = do_pack()
    if path is None:
        return False

    deploy = do_deploy(path)
    if deploy is False:
        return False

    return deploy


def do_clean(number=0):
    """
    clean arch
    """
    try:
        number = int(number)
    except Exception:
        return False
    nb_of_arch = local('ls -ltr versions | wc -l', capture=True).stdout
    nb_of_arch = int(nb_of_arch) - 1
    if nb_of_arch <= 0 or nb_of_arch == 1:
        return True
    if number == 0 or number == 1:
        arch_to_rm = nb_of_arch - 1
    else:
        arch_to_rm = arch_to_rm - number
        if arch_to_rm <= 0:
            return True
    archives = local("ls -ltr versions | tail -n " + str(nb_of_arch) + "\
            | head -n \
            " + str(arch_to_rm) + "\
            | awk '{print $9}'", capture=True)
    archives_list = archives.rsplit('\n')
    if len(archives_list) >= 1:
        for arch in archives_list:
            if (arch != ''):
                local("rm versions/" + arch)
                run('rm -rf /data/web_static/releases/\
                    ' + arch.split('.')[0])
