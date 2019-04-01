import os
import helpers


# starting a new project
def startproject(project_name, project_root, db, python_version, django_version=None):
    project_path = os.path.join(project_root, project_name)
    if os.path.exists(project_path):
        print(f"(!!) A project named {project_name} already exists in {project_root}.")
        print(f"If you Continue there may be bad consequences!")
        choice = input("(!!) to continue press c/C or anything else to cancel: ")
        if not choice.lower() == 'c':
            print(f"(!!) Avoiding creation of of project {project_name} in {project_root}")
            return
    try:
        if python_version >= 3:
            print(f"(++) Initializing project {project_name} with python{python_version}")
            # starting project
            helpers.init_dj_project(project_name, project_path, 3.7, django_version)
            helpers.design_settings_file(project_name, project_path, db)
            # checking dependencies
            requirements_path = helpers.get_or_create_requirements(project_path)
            helpers.inspect_gunicorn_dependency(requirements_path)
            helpers.inspect_django_dependency(requirements_path, '2.1.7')

            if db == 'postgres':
                helpers.inspect_postgres_dependency(requirements_path)

            # creating Dockerfile
            helpers.create_entrypoint(project_path)
            helpers.create_Dockerfile(project_path, "python:3.7", db=db)
            # creating docker-compose file
            helpers.create_docker_compose(project_path, db)
            # starting version control
            helpers.init_git(project_path)
        else:
            # starting project
            helpers.init_dj_project(project_path, project_root, 2.7, django_version)
            helpers.design_settings_file(project_path, project_root, db)
            # checking dependencies
            requirements_path = helpers.get_or_create_requirements(project_path)
            helpers.inspect_gunicorn_dependency(requirements_path)
            helpers.inspect_django_dependency(requirements_path, '2.1.7')

            if db == 'postgres':
                helpers.inspect_postgres_dependency(requirements_path)

            # creating Dockerfile
            helpers.create_entrypoint(project_path)
            helpers.create_Dockerfile(project_path, "python:2.7", db=db)
            # creating docker-compose file
            helpers.create_docker_compose(project_path, db)
            # starting version control
            helpers.init_git(project_path)
    except Exception as e:
        raise


startproject('urloa', '/home/amir/Desktop/', 'postgres', 3.7)