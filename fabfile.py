from fabric.api import local, cd, prefix, sudo, run, env
import os

from contextlib import contextmanager


current_dir = os.path.dirname(__file__)
virtual_env_name = 'venv'
requirements_file = 'requirements.txt'
run_server_command = 'run_server' # command from main.py


@contextmanager
def _source_virtualenv():
    """
    We need to activate virtual env in a context, as we will need to
    do a pip install or run the server after that. If not done in a context,
    the next command will loose the activation(default fabric behaviour)
    """
    activation_path = os.path.join(
        current_dir, virtual_env_name, 'bin', 'activate'
    )
    with prefix('source {0}'.format(activation_path)):
        yield


def setup_postgres():
    """
    This will create a postgres user and database, The settings for that
    come from config
    """
    import config
    db_username = config.db_username
    db_password = config.db_password
    database_name = config.database_name

    local(
        'createuser -h localhost -s %s' % (db_username)
    )

    local(
        'createdb -h localhost -O %s %s' % (db_username, database_name)
    )

    cmd = 'psql -h localhost -c "ALTER USER %s WITH PASSWORD \'%s\'" %s' % \
          (db_username, db_password, database_name)
    local(cmd)



def install_packages():
    """
    Creates a virtual environment and installs the required python modules in
    there
    """
    local('pip install virtualenv')
    local('pip install fabric')
    with cd(current_dir):
        local('virtualenv {0}'.format(virtual_env_name))
        with _source_virtualenv():
            local('pip install -r {0}'.format(requirements_file))


def clearup():
    local('rm -rf {0}'.format(virtual_env_name))

def run_server():
    with _source_virtualenv():
        local('python main.py {0}'.format(run_server_command))
