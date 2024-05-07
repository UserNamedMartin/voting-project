from bs4 import BeautifulSoup
import requests
import time
import re
from typing import Callable
from ...data.constants import USER_AGENTS
from itertools import cycle

class ParsedPage():
    """
    A class to parse HTML pages and extract data.

    Attributes:
    - url (str): The URL of the webpage to parse.
    - soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content of the webpage.
    """

    _user_agents_cycle = cycle(USER_AGENTS)

    def __init__(self, url: str) -> None:
        """
        Initializes a ParsedPage object with the given URL.

        Args:
        - url (str): The URL of the webpage to parse.
        """
        assert isinstance(url, str), 'url must be of type str'
        self.url = url
        self.soup = self._fetch_soup()
    
    def _fetch_soup(self) -> BeautifulSoup:
        """
        Fetches the HTML content of the webpage and returns a BeautifulSoup object.

        Returns:
        - BeautifulSoup: The BeautifulSoup object representing the parsed HTML content.
        """
        for _ in range(3):
            user_agent = next(self._user_agents_cycle)
            response = requests.get(self.url, headers={'User-Agent': user_agent})
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            
            time.sleep(5)

        raise Exception(f'Failed to fetch the webpage:\n{self.url}\nStatus code: {response.status_code}')
    
    def get_data_from_table(self, parse_row: Callable) -> list:
        """
        Extracts data from a table on the webpage.

        Args:
        - func (Callable): A function to process each row of the table.

        Returns:
        - list: A list of objects returned by provided function.
        """
        output_data = []
        table_body = self.soup.find('tbody')
        if not table_body:
            raise Exception((f'Table body was not found on a page:\n{self.url}'))
        
        for row in table_body.find_all('tr'):
            tds = row.find_all('td')
            output_data.append(parse_row(tds))

        return output_data
        
    def get_data_from_subtitle(self, match_re: str):
        """
        Applies given regular expression on a sub-title text on Voting Page and returns the result.

        Args:
        - vote (str): The regular expression for extracting data.

        Returns:
        - Any: output of the first match of given regunal expression.
        """
        text = self._get_subtitle_text()
        num_of_votes = re.search(match_re, text)
        if not num_of_votes:
            return None
        return int(num_of_votes.group(1))

    def _get_subtitle_text(self) -> str:
        """
        Extracts the text from subtitle (with numbers of specific votes) from Voting Page.

        Returns:
        - str: The text with numbers of specific votes.
        """
        subtitle_div = self.soup.find('div', class_='sub-title')
        if not subtitle_div:
            raise Exception(f'Subtitle was not found on page:\n{self.url}')
        
        p_tag = subtitle_div.find('p')
        if not p_tag:
            raise Exception(f'Subtitle text was not found on page:\{self.url}')
        
        return p_tag.get_text()
    
    def get_pdf_url(self) -> str:
        """
        Extracts absolute URL of the PDF file related to particular voting from Voting Page.

        Returns:
        - str: The URL of PDF file.
        """
        a_pdf_tag = self.soup.find('a', class_='pdf')
        if not a_pdf_tag:
            raise Exception(f'<a class="pdf"> was not found on page:\n{self.url}')
        
        pdf_url = a_pdf_tag['href']
        if not pdf_url:
            raise Exception(f'URL of PDF file was not found of page:\n{self.url}')
        
        return pdf_url