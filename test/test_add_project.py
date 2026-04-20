import random
import string

from model.project import Project


def random_string(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_add_project(app):
    name = random_string("name_", 10)
    description = random_string("desc_", 10)
    username = app.config["webadmin"]["username"]
    password = app.config["webadmin"]["password"]
    old_projects_list = app.soap.get_projects_list(username, password)
    app.project.add(Project(name=name, description=description))
    new_projects_list = app.soap.get_projects_list(username, password)
    old_projects_list.append(Project(name=name))
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)
    app.session.logout()