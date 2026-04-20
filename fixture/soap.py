from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False


    def get_projects_list(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            soap_projects = client.service.mc_projects_get_user_accessible(username, password)
            web_projects = self.app.project.get_list()
            projects = []
            # находим соответствие из SOAP (name и description проекта) к id проекта полученного с UI и объединяем их
            for soap_project in soap_projects:
                web_project = next(
                    (p for p in web_projects if p.name == soap_project.name), None)
                project_id = web_project.id if web_project else None
                projects.append(Project(
                    id=project_id,
                    name=soap_project.name,
                    description=soap_project.description
                ))
            return projects
        except WebFault:
            return []