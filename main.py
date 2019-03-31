import helpers


# starting a new project
def startproject(project_name, project_root, db, python_version, django_version=None):
    if python_version >= 3:
        print(f"(++) Initializing project {project_name} with python{python_version}")
        # starting project
        helpers.init_dj_project(project_name, project_root, 3.7, django_version)
        helpers.design_settings_file(project_root, db)
        # checking dependencies
        requirements_path = helpers.get_or_create_requirements(project_root)
        helpers.inspect_gunicorn_dependency(requirements_path)
        helpers.inspect_django_dependency(requirements_path)

        if db == 'postgres':
            helpers.inspect_postgres_dependency(requirements_path)

        # creating Dockerfile
        helpers.create_entrypoint(project_root)
        helpers.create_Dockerfile(project_root, "python:3.7-alpine")
        # starting version control
        helpers.init_git(project_root)
    else:
        # starting project
        helpers.init_dj_project(project_name, project_root, 2.7, django_version)
        helpers.design_settings_file(project_root, db)
        # checking dependencies
        requirements_path = helpers.get_or_create_requirements(project_root, db)
        helpers.inspect_gunicorn_dependency(requirements_path)
        helpers.inspect_django_dependency(requirements_path)

        if db == 'postgres':
            helpers.inspect_postgres_dependency(requirements_path)

        # creating Dockerfile
        helpers.create_entrypoint(project_root)
        helpers.create_Dockerfile(project_root, "python:2.7-alpine")
        # starting version control
        helpers.init_git(project_root)


startproject('urlo', '/home/amir/Desktop/urlo', 'postgres', 3.7, '2.1.7')
