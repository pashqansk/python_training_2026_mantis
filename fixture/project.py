import re
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cache = None

    def get_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            for row in wd.find_elements_by_xpath("//table[@class='width100']/tbody/tr[starts-with(@class,'row-')]"):
                cells = row.find_elements_by_xpath("td")
                if cells[2].text != 'Enabled':
                    href_text = cells[0].find_element_by_css_selector("a").get_attribute("href")
                    id = re.search("\d+$", href_text).group(0)
                    name = cells[0].text
                    status = cells[1].text
                    self.project_cache.append(
                        Project(name=name, status=status, id=id))
        return list(self.project_cache)

    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()

    def add(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_css_selector('input[value="Create New Project"]').click()
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(project.name)
        wd.find_element_by_name("description").click()
        wd.find_element_by_name("description").clear()
        wd.find_element_by_name("description").send_keys(project.description)
        wd.find_element_by_css_selector('input[value="Add Project"]').click()
        wd.find_element_by_link_text("Proceed").click()
        self.project_cache = None

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        self.select_project_by_id(id)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath(
            "//table[@class='width100']/tbody/tr[starts-with(@class,'row-')]/td/a[@href='manage_proj_edit_page.php?project_id=" + id + "']").click()