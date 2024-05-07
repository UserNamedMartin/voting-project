from dataclasses import dataclass
from ...data.constants import PARENT_URL

@dataclass
class Voting():
    '''
    Contains information related to particular Voting.

    Attributes:
    - relative_url (str): The relative URL of the Voting Page
    - number (int): Voting serial number 
    '''
    relative_url: str
    sejm_sub_num: int

    _parent_url = PARENT_URL

    def __post_init__(self):
        assert isinstance(self.relative_url, str), "relative_url must be of type str"
        assert isinstance(self.sejm_sub_num, int), "number must be of type int"

    @property
    def url(self):
        '''Returns absolute URL of Voting Page'''
        return f'{Voting._parent_url}{self.relative_url}'