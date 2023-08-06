"""
    An easy(ier) python implementation of the TeamDynamix Rest APIs
    By Chris Garrett cmgarOK@gmail.com

    ---
    NOTES FOR DEVELOPERS AND CONTRIBUTERS:
    Class methods to retrieve data should begin with get_.

    Class methods to update data should begin with update_.

    Class methods to find data should begin with search_.

    Methods that aren't required to pass in JSON should use 
    the self._get_data function to return information.

    Any method that is marked in the documentation from TDX to 
    be rate-limited should use the sleep() function for the 
    appropriate amount of time to prevent HTTP 429 errors.

    Please follow the docstring commenting for documentation
    of any functions that are added.
"""

__version__ = "2021.06.03"

import datetime as dt
import json
from requests.sessions import Session
from typing import Any, List
from time import sleep

class EzTDXException(Exception):
    """The base class for EzTDX-specific problems"""
    pass

class EzTDX():
    def __init__(self, beid: str, web_services_key: str, app_id: int, sandbox: bool = True) -> None:
        """ initialization """
        self.beid = beid
        self.web_services_key = web_services_key
        self.app_id = app_id
        self.bearer_token = None

        self.session = Session()
        self.credentials = {'BEID': self.beid, 'WebServicesKey': self.web_services_key}

        self.sandbox_base_url = 'https://api.teamdynamix.com/SBTDWebApi/api'
        self.prod_base_url = 'https://api.teamdynamix.com/TDWebApi/api'
        self.sandbox = sandbox

        if self.sandbox:
            self.BASE_URL = self.sandbox_base_url
        else:
            self.BASE_URL = self.prod_base_url

        try:
            response = self.session.post(f'{self.BASE_URL}/auth/loginadmin', data=self.credentials)

            if response.status_code == 200:
                self.session.headers['Authorization'] = f'Bearer {response.text}'
            else:
                raise ConnectionError
        except Exception as ex:
            self.log(f'Error in init: {ex}')

    def _get_data(self, api: str) -> Any:
        """GET Request
        - API string
        """
        try:
            response = self.session.get(f'{self.BASE_URL}{api}')
            if response.status_code == 200:
                return json.loads(response.text)
            elif response.status_code == 429:
                raise Exception(f"You've hit the rate limit for this API call {api}.")
            else:
                raise Exception(f'Error: get_data(): {response.status_code} : {api}')
        except Exception as ex:
            raise Exception(f'Exception in generic_get: {ex}')
            
    def get_person(self, user_id: str) -> Any:
        """Get User by ID"""
        try:
            api = f'/people/{user_id}'
            return self._get_data(api)
        except Exception as ex:
            self.log(f'Error in get_person: {ex}')

    def get_people_groups(self, user_id: str) -> List[str]:
        """Return list of groups by person
        - User ID
        """
        try:
            api = f'/people/{user_id}/groups'
            return self._get_data(api)
        except Exception as ex:
            self.log(f'Error in get_people_groups: {ex}')

    def get_ticket_by_id(self, ticket_id: str) -> dict:
        """ Gets a single ticket by it's id
            - ticket_id: The ID of the ticket
        """
        try:
            api = f'/{self.app_id}/tickets/{ticket_id}'
            return self._get_data(api)
        except Exception as ex:
            self.log(f'Error in get_ticket_by_id: {ex}')

    def get_ticket_description(self, ticket_id: str) -> str:
        """ Get ticket description from ID
            - ticket_id: Ticket ID
        """
        try:
            api = f'/{self.app_id}/tickets/{ticket_id}'

            # prevents breaking rate limiting
            sleep(1.125)

            ticket = self._get_data(api)
            return ticket['Description']
        except Exception as ex:
            self.log(f'Error in get_ticket_description: {ex}')

    def get_ticket_status_id(self, txt_status: str) -> int:
        """ Return ticket status id from text name
            - txt_status: String status code
        """
        try:
            api = f'/{self.app_id}/tickets/statuses'

            ticket_statuses = self._get_data(api)

            for ticket_status in ticket_statuses:
                if ticket_status['Name'] == txt_status:
                    return int(ticket_status['ID'])
        except Exception as ex:
            self.log(f'Error in get_ticket_status: {ex}')

    def get_ticket_status_ids(self, ticket_statuses_text: List[str]) -> List[int]:
        """ Change list of ticket status text to list of status ids
            - ticket_status: List of text ticket statuses
        """

        try:
            api = f'/{self.app_id}/tickets/statuses'

            ticket_statuses = self._get_data(api)

            ticket_status_ids = []

            for ticket_status_text in ticket_statuses_text:
                for ticket_status in ticket_statuses:
                    if ticket_status['Name'] == ticket_status_text:
                        ticket_status_ids.append(ticket_status['ID'])

            return ticket_status_ids
        except Exception as ex:
            self.log(f'Error in get_ticket_status_ids: {ex}')

    def get_time_types(self) -> List[str]:
        """Get Time Types"""
        try:
            api = f'/time/types'

            # prevents breaking rate limiting
            sleep(1.125)

            return self._get_data(api)
        except Exception as ex:
            self.log(f'Error in get_time_types: {ex}')

    def get_time_type(self, time_type_id: int) -> str:
        """Get Time Type by ID"""
        try:
            api = f'/time/types/{time_type_id}'

            # prevents breaking rate limiting
            sleep(1.125)

            return self._get_data(api)
        except Exception as ex:
            self.log(f'Error in get_time_types: {ex}')

    def log(self, msg: str) -> None:
        """Log to file"""
        try:
            now = str(dt.datetime.now())

            print(f'{now} - {msg}')

            with open('last_run.log','a') as last_run:
                last_run.write(f'{now} - {msg}\n')
        except Exception as ex:
            print(f'Error writing to log: {ex}')

    def search_people(self, search_by: str, max_results: int = 10) -> List[dict]:
        """Search people
        - Search terms
        - Max results: default 10, max 100
        """
        try:
            api = f'/people/lookup?searchText={search_by}&maxResults={max_results}'
            return self._get_data(api)
        except Exception as ex:
            self.log(f'Error in get_people: {ex}')

    def search_tickets(self, search_str: str, ticket_status: List[str] = ['New'], max_results: int = 5) -> List[str]:
        """ Searches for tickets 
            - search_str: Search Text to filter tickets on
            - ticket_status: List of ticket statuses to filter on (default: New tickets)
            - max_results: How many tickets to return (default: 5 tickets)
        """

        try:
            # convert list of text status types into their IDs
            ticket_status_ids = self.get_ticket_status_ids(ticket_status)

            data = {
                'MaxResults': max_results,
                'StatusIDs': ticket_status_ids,
                'SearchText': search_str
            }
            response = self.session.post(f'{self.BASE_URL}/{self.app_id}/tickets/search', data=data)

            if response.status_code == 200:
                tickets = json.loads(response.text)

                return tickets
        except Exception as ex:
            self.log(f'Error in search_tickets: {ex}')

    def search_time_entries(self, entry_date_from: str, entry_date_to: str, person_ids: List[str]=[], max_results: int=1000) -> List[str]:
        """Search for time entered
        - Entry Date From: 2021-06-02T00:00:00Z format
        - Entry Date To: 2021-06-02T00:00:00Z format
        - Person IDs: List of GUIDS (default: empty list)
        - Max Results: (default: 1000 entries)
        """
        
        try:
            data = {
                'EntryDateFrom': entry_date_from,
                'EntryDateTo': entry_date_to,
                'PersonUIDs': person_ids,
                'MaxResults': max_results
            }

            response = self.session.post(f'{self.BASE_URL}/time/search', data=data)

            if response.status_code == 200:
                return json.loads(response.text)
        except Exception as ex:
            self.log(f'Error in search_time: {ex}')


    def update_ticket(self, ticket_id: int, comment: str, new_status: str = "None", is_private: bool = False) -> str:
        """ Update a ticket feed
            - ticket_id: ID of ticket to be updated
            - new_status: Change the status of the ticket (default: None for no change)
            - comment: Comment to add to the feed
            - is_private: Mark the comment as private
        """
        try:
            new_status_id = 0

            if new_status != 'None':
                new_status_id = self.get_ticket_status_id(new_status)

            data = {
                'NewStatusID': new_status_id,
                'Comments': comment,
                'IsPrivate': is_private
            }

            response = self.session.post(f'{self.BASE_URL}/{self.app_id}/tickets/{ticket_id}/feed', data=data)

            if response.status_code == 201:
                return f'Ticket {ticket_id} updated successfully!'
            else:
                return f'Ticket {ticket_id} could not be updated.'
        except Exception as ex:
            self.log(f'Error in update_ticket: {ex}')