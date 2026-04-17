import random
import string

from model.project import Project


def random_string(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_add_project(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")
    name = random_string("name_", 10)
    description = random_string("desc_", 10)
    old_projects_list = app.project.get_list()
    app.project.add(Project(name=name, description=description))
    new_projects_list = app.project.get_list()
    old_projects_list.append(Project(name=name))
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)
    app.session.logout()