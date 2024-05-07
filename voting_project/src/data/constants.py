USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.38",
    # Opera
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    # Internet Explorer
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    # Android
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36",
    # iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]
'''A list of different User Agents for several platforsm and browsers.'''

PARENT_URL = 'https://www.sejm.gov.pl/Sejm9.nsf/'
'''Parent URL of all the relative links used in the program.'''

_main_url_relative = 'agent.xsp?symbol=posglos&NrKadencji=9'
'''Relative URL of the main (initial) page.'''

MAIN_URL = f'{PARENT_URL}{_main_url_relative}'
'''Absolute URL of the main (initial) page.'''

MONTH_TO_INT = {
        'stycznia': '01',
        'lutego': '02',
        'marca': '03',
        'kwietnia': '04',
        'maja': '05',
        'czerwca': '06',
        'lipca': '07',
        'sierpnia': '08',
        'września': '09',
        'października': '10',
        'listopada': '11',
        'grudnia': '12'
    }
'''Dictionary with months names in Polish as keys and their integer values form 01 to 12 as values.'''

PDF_DATABASE_PATH_OUTPUT = 'voting_project/src/data/pdf_database.csv'
'''Relative path to a csv file with database of PDF files, used for OUTPUT OF THE WEB SCRAPER.'''

PDF_DATABASE_PATH_INPUT = 'voting_project/src/data/pdf_database.csv'
'''Relative path to a csv file with database of PDF files, used for INPUT OF PDF PROCESSING.'''

MAIN_DATABASE_PATH_OUTPUT = 'voting_project/src/data/main_database.csv'
'''Relative path to a csv file with main database, used for OUTPUT OF PDF PROCESSING.'''

MAIN_DATABASE_PATH_INPUT = 'voting_project/src/data/main_database.csv'
'''Relative path to a csv file with main database, used for INPUT OF NETWORK CREATION.'''

EDGES_DATABASE_PATH_OUTPUT = 'voting_project/src/data/edges_database.csv'
'''Relative path to a csv file with edges database, USED FOR OUTPUT OF NETWORK CREATION.'''

NODES_DATABASE_PATH_OUTPUT = 'voting_project/src/data/nodes_database.csv'
'''Relative path to a csv file with nodes database, USED FOR OUTPUT OF NETWORK CREATION.'''