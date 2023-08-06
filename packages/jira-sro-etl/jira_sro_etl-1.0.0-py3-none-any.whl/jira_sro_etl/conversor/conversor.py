from jiraX import factories as factory
from sro_db.application import factories
from sro_db.model import factories as factories_model
from datetime import datetime
from functools import lru_cache
from pprint import pprint

import abc

class Conversor(metaclass=abc.ABCMeta):

    def __init__(self, organization, data):
        self.organization = organization
        self.data = data
        self.issue_apl = factory.IssueFactory(user=data['user'], apikey=data['key'], server=data['url'])
        self.board_apl = factory.BoardFactory(user=data['user'], apikey=data['key'], server=data['url'])

    def date_formater(self, date_string):
        """Receive date in YYYY-MM-DD T HH:MM:SS and return datetime

        Can receive date with more details like hour, minute and second, but all info
        after day is ignored

		Args:
			date_string (str/NoneType): string YYYY-MM-DD T HH:MM:SS or None

		Returns:
			datetime/NoneType: Formated date or None if param was None
		"""
        if date_string:
            return datetime.strptime(date_string.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        return None

    @lru_cache(maxsize=20)
    def __find_status_from_boardId(self, board_id):
        raw = self.board_apl.get_config(board_id)
        columns_list = raw['columnConfig']['columns']
        status_ids_list = [_dict['statuses'][0]['id'] for _dict in columns_list] 
        return status_ids_list

    def __find_on_changelog_list(self, ids_list, _list):
        result = [(None,None),(None,None),(None,None)]
        try:
            for changelog in _list:
                for item in changelog['items']:
                    try:
                        if(item['field'] == 'status' and item['to'] in ids_list):
                            result[ids_list.index(item['to'])] = (self.date_formater(changelog['created']), changelog['author']['accountId'])
                    except Exception as e:
                        pass   
        except Exception as e:
            pass
        return result

    def __find_on_changelog(self, issue, ids_list):
        first_try = self.__find_on_changelog_list(ids_list, issue.raw['changelog']['histories'])
        if len([x for x,y in first_try if x is not None]) == len(ids_list):
            return first_try
        second_try = self.__find_on_changelog_list(ids_list, self.issue_apl.get_changelog(issue.key)['values'])
        return second_try

    def find_activated_resolved_closed(self, issue):
        try:
            board_id = issue.raw['fields']['customfield_10018'][-1]['boardId']
            status_ids = self.__find_status_from_boardId(board_id)
            actual_status_index = status_ids.index(issue.raw['fields']['status']['id'])
            len_status = len(status_ids)
            desired_ids = filter(lambda x: x <= actual_status_index, [1, len_status-2, len_status-1]) # Segundo, penúltimo e último
            result_list = self.__find_on_changelog(issue, [status_ids[i] for i in desired_ids])
            return result_list
        except Exception as e:
            # Caso não esteja em um board
            return [(None,None),(None,None),(None,None)]

    @abc.abstractmethod
    def convert(self):
        pass