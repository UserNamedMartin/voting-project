from src.classes.scraper.parsed_page import ParsedPage
from src.classes.scraper.voting_day import VotingDay
from src.classes.scraper.voting import Voting
import csv
from tqdm import tqdm
from src.data.constants import MAIN_URL, MONTH_TO_INT, PDF_DATABASE_PATH_OUTPUT


def parse_main_page_row(row: list) -> VotingDay:
    """
    Extracts data from a row of an Main Page table on the Sejm website.

    This function takes a list representing a row of data from the Initial Page table on the Sejm website,
    extracts relevant information and puts in into the Day dataclass object.

    Args:
    - row (list): A list containing the elements of a row from the Initial Page table.

    Returns:
    - Day: A dataclass object that contains information extracted from the Main Page and related to particular Voting Day.
    """
    sejm_num = None if not row[0].text.isdigit() else int(row[0].text)
    day, month, year = row[1].text.split()[:-1]
    date = f'{day}.{MONTH_TO_INT[month]}.{year}'
    expected_votings = int(row[2].text)
    relative_url = row[1].find('a')['href']

    return VotingDay(date, expected_votings, relative_url, sejm_num)

def parse_day_page_row(row: list) -> Voting:
    """
    Extracts data from a row of a Day Page table on the Sejm website.

    This function takes a list representing a row of data from the Day Page table on the Sejm website, 
    extracts relevant information and puts in into the Voting dataclass object.

    Args:
    - row (list): A list containing the elements of a row from the Day Page table.

    Returns:
    - Voting: A dataclass object that contains information extracted from the Day Page and related to particular Voting.
    """
    relative_url = row[2].find('a')['href']
    sejm_sub_num = int(row[0].text)
    return Voting(relative_url, sejm_sub_num)

if __name__ == '__main__':
    
    unprocessed = []
    main_page = ParsedPage(MAIN_URL)

    with open(PDF_DATABASE_PATH_OUTPUT, 'w') as database:
        writer = csv.writer(database)
        writer.writerow(('Voting ID', 'Voting Date', 'Voting PDF URL', 'Expected number of Target Votes'))

        for day in tqdm(main_page.get_data_from_table(parse_main_page_row)):

            day_page = ParsedPage(day.url)
            votings = day_page.get_data_from_table(parse_day_page_row)

            # Meaning that out program did not find all the necessary votings
            if len(votings) != day.expected_votings:
                raise Exception(f'On page:\n{day.url}\nExpected number of votings: {day.expected_votings}\nActual number of votings: {len(votings)}')
            
            for voting in votings:
                
                voting_page = ParsedPage(voting.url)

                pdf_url = voting_page.get_pdf_url()
                for_num = voting_page.get_data_from_subtitle(r"Za - (\d+)")
                against_num = voting_page.get_data_from_subtitle(r"Przeciw - (\d+)")
                
                # Pages with votings related to Elections, not initiatives have no "Za" and "Przeciw"
                if for_num is None or against_num is None:
                    unprocessed.append((f'{day.sejm_num}-{voting.sejm_sub_num}', voting.url))
                else:
                    writer.writerow((
                        f'{day.sejm_num}-{voting.sejm_sub_num}',
                        day.date,
                        pdf_url,
                        int(for_num) + int(against_num)
                    ))

    print('URL of Voting Pages that were not processed:')
    for id_and_url in unprocessed:
        print(id_and_url)
