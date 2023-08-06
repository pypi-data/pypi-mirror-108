from datetime import datetime
from functools import lru_cache
from .conversor import Conversor
from sro_db.model import factories as factories_model

class ConversorUser(Conversor):

    def __init__(self, organization, data):
        self.organization = organization
    
    def convert(self, jira_user, ontology_user = None):

        print("--------- Conversor User -----------")
    
        if ontology_user is None:
            ontology_user = factories_model.PersonFactory()
        
        ontology_user.organization_id = self.organization.id
        ontology_user.name = jira_user.displayName
        if jira_user.emailAddress != '':
            ontology_user.email = jira_user.emailAddress

        print("--------- Conversor User End -----------")

        return ontology_user