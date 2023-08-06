from datetime import datetime
from functools import lru_cache
from .conversor import Conversor

from jiraX import factories as factory
from sro_db.application import factories
from sro_db.model import factories as factories_model

class ConversorTeam(Conversor):
    def __init__(self, organization, data):
        super().__init__(organization, data)

    def convert(self, etl_scrum_project,
        jira_project,
        ontology_scrum_team = None):
        print("--------- Conversor team -----------")

        scrum_project_application = factories.ScrumAtomicProjectFactory()

        # Ontology_scrum_team
        if ontology_scrum_team is None:
            ontology_scrum_team = factories_model.ScrumTeamFactory()
        ontology_scrum_team.name = f"{jira_project.key}_scrum_team"
        ontology_scrum_team.organization_id = self.organization.id
        
        # Ontology_scrum_project
        project_id = jira_project.id
        ontology_scrum_project = scrum_project_application.retrive_by_external_uuid(jira_project.id)
        if ontology_scrum_project is None:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            scrum_project, _, _, _ = scrum_project.create(data_to_create)
            ontology_scrum_team.scrum_project_id = scrum_project.id
        else:
            ontology_scrum_team.scrum_project_id = ontology_scrum_project.id
        
        print("--------- Conversor team end -----------")

        return ontology_scrum_team