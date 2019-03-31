# main functions for either initializing a
# new project or Dockerizing an existing one.

import os
import file_handlers as handlers
from exceptions import (EntryPointNotAvailable,
                        RequirementsNotAvailable,
                        LinuxProgramNotInstalled)


# this function creates a Dockerfile.
# python version is the version specified for the Dockerfile and is required.
def create_Dockerfile(project_root, python_version, requirements_file=None,
                      entrypoint_file=None):
    # Dockerfile path
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    docker_path = os.path.join(managepy_abs_path, 'Dockerfile')

    # if the docker file already exists, then do nothing
    docker_file_check = handlers.get_absolute_path(project_root, 'Dockerfile')
    if docker_file_check:
        print(
            f"(!!) A Dockerfile already exists in {docker_file_check}"
        )
        print(f"If you continue, a new Docker file will be created in {docker_path}")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print("(!!) Avoiding creation of a new Dockerfile")
            return

    # creating Dockerfile
    try:
        with open(docker_path, 'w') as docker_file:
            docker_file.write("# This docker file is automatically created by 'no-headache-django' project.\n")
            docker_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            # including desired python version.
            docker_file.write(f"\nFROM {python_version}\n\n")
            # settings general env vars.
            docker_file.write("ENV PYTHONDONTWRITEBYTECODE 1\n")
            docker_file.write("ENV PYTHONUNBUFFERED 1\n\n")
            # creating project core folder.
            docker_file.write("WORKDIR /project_core\n")
            docker_file.write("COPY . /project_core\n\n")
            # managin staticfiles
            docker_file.write("RUN mkdir -p media\n")
            docker_file.write("RUN mkdir -p static\n\n")
            # opening port 8000 by default.
            docker_file.write("EXPOSE 8000\n\n")

            # finding requirements.txt or using the provided one.\
            if requirements_file:
                requirements_file = [requirements_file]
            else:
                requirements_file = handlers.get_absolute_path(project_root, 'requirements.txt')

            if not requirements_file:
                raise RequirementsNotAvailable(
                    f"""(!!) requirements file not found in {project_root}.
                    This file is required in order to install python dependencies using pip.
                    Either create one named "requirements.txt" or represent yours.
                    """
                )
            if len(requirements_file) != 1:
                raise FileExistsError(
                    f"""(!!) There are more than one requirements file in your project root: {project_root}
                    please specify one: {requirements_file}
                    """
                )
            requirements_file = requirements_file[0]
            docker_file.write(f"RUN pip install -r {handlers.get_relative_path(requirements_file, os.path.dirname(docker_path))}\n\n")

            # finding entrypoint.sh or using the provided one.
            if entrypoint_file:
                entrypoint_file = [entrypoint_file]
            else:
                entrypoint_file = handlers.get_absolute_path(project_root, 'entrypoint.sh')

            if not entrypoint_file:
                raise EntryPointNotAvailable(
                    f"""(!!) entrypoint file not found in {project_root}.
                    This file is required in order to be run when an instance of docker is initialized.
                    Either create one named "entrypoint.sh" or represent yours.
                    """
                )
            if len(entrypoint_file) != 1:
                raise FileExistsError(
                    f"""(!!) There are more than one requirements file in your project root: {project_root}
                    please specify one: {entrypoint_file}
                    """
                )
            entrypoint_file = entrypoint_file[0]
            # relative path to Dockerfile
            entrypoint_file = handlers.get_relative_path(entrypoint_file, os.path.dirname(docker_path))
            docker_file.write(f"RUN chmod +x {entrypoint_file}\n\n")
            docker_file.write(f"""CMD ["{os.path.join('./', entrypoint_file)}"]\n""")

        print(f"(++) Docker file created in {docker_path}")
    except Exception as e:
        print('(!!) An error occurred. rolling back ... ')
        os.system(f'rm {docker_path}')
        print('(!!) Docker file deleted. raising the exception ...')
        raise


def create_entrypoint(project_root):
    # Dockerfile path
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    entrypoint_path = os.path.join(managepy_abs_path, 'entrypoint.sh')

    # checking if there are no entrypoints available.
    entrypoint_check = handlers.get_absolute_path(project_root, 'entrypoint.sh')
    if entrypoint_check:
        print(
            f"(!!) An entrypoint.sh file already exists in {entrypoint_check}"
        )
        print(f"If you continue, a new entrypoint file will be created in {entrypoint_path}")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print("(!!) Avoiding creation of a new entrypoint.sh file")
            return

    # creating entrypoint.sh file
    try:
        with open(entrypoint_path, 'w') as entrypoint_file:
            entrypoint_file.write("# This file is automatically created by 'no-headache-django' project.\n")
            entrypoint_file.write("# Please star me on github: http://github.com/mrsaemir/no-headache-django\n")
            entrypoint_file.write("#!/bin/bash\n\n")
            managepy_relative_path = os.path.join(handlers.get_relative_path(managepy_abs_path,
                                                                             os.path.dirname(entrypoint_path)),
                                                  'manage.py'
                                                  )
            entrypoint_file.write(f"python {managepy_relative_path} migrate\n")
            entrypoint_file.write(f"python {managepy_relative_path} collectstatic --noinput\n")
            # setting wsgi file.
            wsgi_file = handlers.get_wsgi_file(project_root)
            wsgi_file_rel_path = handlers.get_relative_path(os.path.dirname(wsgi_file), managepy_abs_path)

            entrypoint_file.write(f"gunicorn {wsgi_file_rel_path}.wsgi:application -w 2 -b :8000\n")

            print(f"(++) entrypoints.sh file created in {entrypoint_path}")
    except Exception as e:
        print('(!!) An error occurred. rolling back ... ')
        os.system(f'rm {entrypoint_path}')
        print('(!!) Entrypoint.sh file deleted. raising the exception ...')
        raise
    return entrypoint_path


def get_or_create_requirements(project_root):
    managepy_abs_path = os.path.dirname(handlers.get_managepy_path(project_root))
    requirements_file_path = os.path.join(managepy_abs_path, 'requirements.txt')
    if not os.path.exists(requirements_file_path):
        try:
            with open(requirements_file_path, 'w') as requirements_file:
                print(f"(++) Requirements.txt file created in {requirements_file_path}")
        except Exception as e:
            print('(!!) An error occurred. rolling back ... ')
            os.system(f'rm {requirements_file_path}')
            print('(!!) Requirements.txt file deleted. raising the exception ...')
            raise
    # inspecting requirements ...
    inspect_gunicorn_dependency(requirements_file_path)
    return requirements_file_path


# this function checks if a certain requirements file contains gunicorn.
def inspect_gunicorn_dependency(requirements_path):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'gunicorn' not in requirements.lower():
            print('(++) Adding Gunicorn to project requirements.')
            requirements_file.write('\ngunicorn==19.9.0')


def inspect_postgres_dependency(requirements_path):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'psycopg2-binary' not in requirements.lower():
            print('(++) Adding Postgres to project requirements.')
            requirements_file.write('\npsycopg2-binary==2.7.4')


def inspect_django_dependency(requirements_path, django_version=None):
    with open(requirements_path, 'r+') as requirements_file:
        requirements = requirements_file.read()
        if 'django' not in requirements.lower():
            print('(++) Adding Django to project requirements.')
            if django_version:
                requirements_file.write(f'\nDjango=={django_version}')
            else:
                requirements_file.write('\nDjango')


# for new projects only!
def design_settings_file(project_name, project_root, db):
    settings_module = handlers.get_settings_file(project_root)

    try:
        # replacing the new one.
        if db == 'postgres':
            settings_backup = os.path.join(settings_module, ".bu")
            os.system(f'mv {settings_module} {settings_backup}')
            os.system(f'cp ./dj/dj2/postgres/settings.py {settings_module}')
            inspect_postgres_dependency(get_or_create_requirements(project_root))
            os.system(f"rm {settings_backup}")

            with open(settings_module, 'a+') as settings:
                settings.write(f"\n\nROOT_URLCONF = '{project_name}.urls'")
                settings.write(f"\nWSGI_APPLICATION = '{project_name}.wsgi.application'")
        else:
            pass
    except Exception as e:
        print('(!!) An error occurred designing settings file. rolling back ... ')
        os.system(f"mv {settings_backup} {settings_module}")
        raise


# inspects if a program is installed in linux
def is_installed(program_name):
    from shutil import which
    return which(program_name) is not None


# python/django version are version numbers.
def init_dj_project(project_name, project_root, python_version, django_version=None):
    project_path = os.path.exists(os.path.join(project_root, project_name))
    if project_path:
        print('(!!) Project already exists. avoiding creation')
        return

    if not is_installed(f'python{python_version}'):
        raise LinuxProgramNotInstalled(f'python{python_version}')

    if not is_installed('virtualenv'):
        raise LinuxProgramNotInstalled('virtualenv')

    # creating virtuelenv
    venv_path = os.path.join('../', project_root, 'venv')
    if not os.path.exists(venv_path):
        os.system(f'virtualenv --python python{python_version} {venv_path}')
    # installing django
    if django_version:
        os.system(f'{os.path.join(venv_path, "bin/pip")} install django=={django_version}')
        # creating the project
        os.system(f'cd {project_root} && {os.path.join(venv_path, "bin/django-admin")} startproject {project_name}')
        inspect_django_dependency(get_or_create_requirements(project_root), django_version)
    else:
        os.system(f'{os.path.join(venv_path, "bin/pip")} install django')
        # creating the project
        os.system(f'cd {project_root} && {os.path.join(venv_path, "bin/django-admin")} startproject {project_name}')
        inspect_django_dependency(get_or_create_requirements(project_root))


def init_git(project_root):
    if not is_installed(f'git'):
        raise LinuxProgramNotInstalled(f'git')
    os.system(f'cd {project_root} && git init')

