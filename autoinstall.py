from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "you git repository"

env.user = 'ubuntu'
env.password = '123456a.'

# ��д���Լ���������Ӧ������
env.hosts = ['yuanlongzeng.cn']

# һ�������Ϊ 22 �˿ڣ������ 22 �˿���鿴������������ṩ���ṩ����Ϣ
env.port = '22'


def deploy():
    source_folder = '/home/ubuntu/bog/myblog/test1'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('systemctl restart website')
    sudo('service nginx reload')