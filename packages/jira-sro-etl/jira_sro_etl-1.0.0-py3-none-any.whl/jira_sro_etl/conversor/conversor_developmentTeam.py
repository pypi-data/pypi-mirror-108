from datetime import datetime
from functools import lru_cache
from .conversor import Conversor

from jiraX import factories as factory
from sro_db.application import factories
from sro_db.model import factories as factories_model

class ConversorDevelopmentTeam(Conversor):
    def __init__(self, organization, data):
        super().__init__(organization, data)

    def convert(self, etl_scrum_project_team,
        jira_project,
        ontology_scrum_development_team = None):
        
        print("--------- Conversor development team -----------")

        scrum_team_application = factories.ScrumTeamFactory()

        # Organization and name
        if ontology_scrum_development_team is None:
            ontology_scrum_development_team = factories_model.DevelopmentTeamFactory()
        ontology_scrum_development_team.organization = self.organization
        ontology_scrum_development_team.name = f"{jira_project.key}_scrum_development_team"
        
        # Scrum team id
        project_id = jira_project.id
        ontology_scrum_team = scrum_team_application.retrive_by_external_uuid(jira_project.id)
        if ontology_scrum_team == None:
            scrum_project_team = etl_scrum_project_team()
            scrum_project_team.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            ontology_scrum_development_team.scrum_team_id = scrum_project_team.create(data_to_create).id
        else:
            ontology_scrum_development_team.scrum_team_id = ontology_scrum_team.id
            

        print("--------- Conversor development team end -----------")

        return ontology_scrum_development_team

            