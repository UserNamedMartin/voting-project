from dataclasses import dataclass
from ...data.constants import PARENT_URL

@dataclass
class VotingDay():
    '''
    Contains information related to a specific Voiting Day.

    Attributes:
    - date (str): The date of the voting in "day.month.year" format.
    - expected_votings (int): The number of expected votings for the day.
    - relative_url (str): The relative URL of the Voting Day webpage.
    - sejm_num (int | None): The serial number of the Sejm session.
    '''
    date: str
    expected_votings: int
    relative_url: str
    sejm_num: int | None

    _parent_url = PARENT_URL
    # In some of the cells we do not have a Sejm Number.
    # It means than we inherit it form the previous row, so we need to keep track of it.
    _cur_sejm_num = None

    def __post_init__(self) -> None:
        assert isinstance(self.date, str), "date must be of type str"
        assert isinstance(self.expected_votings, int), "date must be of type int"
        assert isinstance(self.relative_url, str), "url must be of type str"
        assert isinstance(self.sejm_num, (int, type(None))), "sejm_num must be of type int | None"

        if self.sejm_num is not None:
            VotingDay._cur_sejm_num = self.sejm_num
        else:
            self.sejm_num = VotingDay._cur_sejm_num
    
    @property
    def url(self):
        '''Return absolute URL of the Day Page'''
        return f'{VotingDay._parent_url}{self.relative_url}'
