import requests
import io
import time
import fitz
from ...data.constants import USER_AGENTS
from .person import Person
import re
from unidecode import unidecode
from itertools import cycle

class ParsedPDF():
    """
    A class to parse PDF files and extract data.

    Attributes:
    - url (str): The URL of the PDF document.
    - lines (tuple[str]): A tuple with non-empty lines found in the PDF document
    """
    
    _user_agents_cycle = cycle(USER_AGENTS)

    def __init__(self, url: str) -> None:
        """
        Initializes a ParsedPDF object with the given URL.

        Args:
        - url (str): The URL of the PDF document to parse.
        """
        self.url = url
        self.lines = self._get_lines()
    
    def _get_lines(self) -> tuple[str]:
        '''
        Creates a tuple of non-empty lines from PDF document.

        Returns:
        - tuple[str]: A tuple of strings, where each string is a non-empty line from PDF document.
        '''
        text = self._get_text()
        lines = text.split('\n')
        non_empty_lines = tuple(line.strip() for line in lines if line.strip())

        return non_empty_lines
        
    def _get_text(self) -> str:
        '''
        Fetches text from PDF file.

        Returns:
        - str: string with all text form PDF document
        '''
        for _ in range(3):

            user_agent = next(self._user_agents_cycle)
            response = requests.get(self.url, headers={'User-Agent': user_agent})

            if response.status_code == 200:

                pdf_file = io.BytesIO(response.content)
                pdf_doc = fitz.open(stream=pdf_file)

                output = ''
                for page in pdf_doc:
                    output += page.get_text()
                return output
            
            time.sleep(5)

        raise Exception(f'Failed to fetch the webpage:\n{self.url}\nStatus code: {response.status_code}')

    def get_voters_by_vote_statuses(self, vote_statuses: tuple[str]) -> dict[str, list[Person]]:
        '''
        Filters people from the PDF file by their vote status.

        For each vote status returns a list of People obejcts representing members of Polish Sejm
        with particuler vote in this Voting.

        Arguments:
        - vote_statuses (tuple[str]): Statuses of the vote to filter the voters by.

        Returns:
        - dict[str, list[Person]]: A dictionary with keys are vote statuses provided in vote_status and values are lists of People objects with corresponding votes.
        '''
        assert isinstance(vote_statuses, tuple)

        output = {vote_status : [] for vote_status in vote_statuses}
        cur_party = None
        cur_name = ''

        for line in self.lines:

            if self._is_party(line):
                cur_party = line.split('(')[0].strip()
            
            elif cur_party:

                # Line can be a name only:
                # VASUA PUPKIN
                # or
                # DED PIHTO
                if self._is_name(line):

                    if cur_name and not cur_name.endswith('-'):
                        cur_name += ' '
                    cur_name += line
                
                # Line can be a voting status:
                # za
                # or
                # pr.
                elif self._is_target_vote_status(line, vote_statuses):
                    output[line].append(Person(cur_name, cur_party))
                    cur_name = ''
                
                # Due to the mistakes in the PDF documents, line can be both name and voting status
                # VASUA PUPKINza
                # or
                # DED PIHTO pr.
                elif self._is_name_and_target_vote_status(line, vote_statuses):
                    name, vote_status = self._split_name_and_target_vote_status(line, vote_statuses)

                    if cur_name and not cur_name.endswith('-'):
                        cur_name += ' '
                    cur_name += name
                    
                    output[vote_status].append(Person(cur_name, cur_party))
                    cur_name = ''
                
                # If line is none of the above, we do not need it
                else:
                    cur_name = ''

        return output
    
    def _is_party(self, line: str) -> bool:
        """
        Returns True if input string is a party title string.
        """
        match = re.search(r'\(\d+\)$', line)
        return match is not None

    def _is_name(self, line: str) -> bool:
        """
        Returns True if input string is a name.
        """
        line_ascii = unidecode(line).replace('-', '').strip()
        return all(char.isupper() or char.isspace() for char in line_ascii)

    def _is_target_vote_status(self, line: str, vote_statuses: tuple[str]) -> bool:
        '''
        Returns True if the stirng is one of the target vote statuses.
        '''
        return line in vote_statuses

    def _is_name_and_target_vote_status(self, line: str, vote_statuses: tuple[str]) -> bool:
        '''
        Returns True if input string is concatenated version of name and vote status:
        - MARTIN MOURZENKOVagainst
        - VASYA PUPKIN for
        '''
        for vote_status in vote_statuses:
            if line.endswith(vote_status):
                vote_status_idx = line.rfind(vote_status)
                return self._is_name(line[:vote_status_idx].strip())
    
    def _split_name_and_target_vote_status(self, line: str, vote_statuses: tuple[str]) -> tuple[str]:
        '''
        Assumes that string is a concatenated version of name and vote vote status. Returns separated name and vote status
        '''
        for vote_status in vote_statuses:
            if line.endswith(vote_status):
                vote_status_idx = line.rfind(vote_status)
                return line[:vote_status_idx].strip(), line[vote_status_idx:]
    