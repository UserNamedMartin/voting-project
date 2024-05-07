# Voting Project

## Short Description
The aim of this project is to gather, organize, and process data from the Polish Sejm website for further analysis.

The project focuses on votings that occurred between **21st November 2019** and **16th August 2023**, accessible through the following link: [Polish Sejm Website](https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=posglos&NrKadencji=9).

## Structure
The project is divided into three main components:

### Web Scraper
The web scraper navigates through the Polish Sejm website, following this hierarchy:
- **Main Page**: This initial page contains a table with information regarding "Głosowania na posiedzeniach Sejmu." Each row corresponds to a specific Voting Day in the Polish Sejm and contains data related to it, along with a relative URL linking to the page for that particular Voting Day.
- **Voting Day Page**: This page contains table with details of the votings held on a specific Voting Day. Each row in the table corresponds to a particular voting and contains data related to it, along with a relative URL linking to the page for that specific voting.
- **Voting Page**: Here, detailed information about a particular voting is provided, along with an absolute URL linking to the PDF file containing the voting results.

The web scraping program extracts the following data for each voting and puts in in the CSV file where each row contains:
- Voting ID: A combination of the Sejm Number and the Voting Number within this Sejm.
- Voting Date: The date when the voting took place.
- Voting PDF URL: The absolute URL of the PDF file containing the voting results.
- Expected Number of Target Votes: In this project I was focused on votes "for" ("za") and "against" ("pr.").

### PDF Processing
This part extracts data from each PDF document. For each target vote, it retrieves all individuals with that vote (full name and party). The input for this component is the output of the web scraper. It processes each row of the input CSV file, loads the PDF document containing the voting results, and extracts relevant data. The output is a CSV file containing the following data for each individual (with vote "za" or "pr.") in a particular voting:
- Voting ID (from the input table)
- Voting Date (from the input table)
- Voter ID: A unique identifier based on the combination of the voter's full name and party. Thus, an individual belonging to two different parties at different time will have two distinct IDs.
- Voter's Name: Full name of the voter.
- Voter's Party: Name of the voter's party.
- Voter's Vote: Either "for" ("za") or "against" ("pr.") based on the scope of the project.

### Network Creation
This component creates a network based on the output CSV file from the previous component. Each voting is treated as a separate event, and an edge between two individuals (IDs) is established if they voted in the same way. The component then aggregates all edges to create a comprehensive network. So, the weight of the connection between two individuals (IDs) is basically a number of votings where they voted in the same way (both "za" or both "pr.") Subsequently, it utilizes network data to generate two output CSV files: one for nodes and one for edges.

The Nodes CSV file contains the following data:
- ID: From the input table, used for creating edges.
- Full Name
- Party

The Edges CSV file contains the following data:
- Source: Sourse node (individual) ID
- Target: Target node (individual) ID
- Type: All edges are considered undirected.
- ID: Unique identifier for an edge.
- Weight

## Usage
The output of the program can be found in the `voting_project/src/data` directory.

- **"pdf_database.csv"**: Output of the Web Scraping component, structured as follows:
  | Voting ID | Voting Date | Voting PDF URL | Expected Number of Target Votes |
  | --------- | ----------- | -------------- | ------------------------------- |
- **"main_database.csv"**: Output of the PDF Processing component. **IMPORTANT!!!** Due to the GitHub file size limitations, main database is devided in two parts: "main_database.csv" and "main_database_2.csv". Before any opetaions with the program it is crucial to merge "main_database_2.csv" into "main_database.csv" and delete "main_database_2.csv". The output "main_database.csv" will be structured as follows:
  | Voting ID | Voting Date | Voter ID | Voter's Name | Voter's Party | Voter's Vote |
  | --------- | ----------- | -------- | ------------ | ------------- | ------------ |
- **"nodes_database.csv"**: Output of the Network Creation component, structured as follows:
  | ID | Full Name | Party |
  | -- | --------- | ----- |
- **"edges_database.csv"**: Output of the Network Creation component, structured as follows:
  | Source | Target | Type | ID | Weight |
  | ------ | ------ | ---- | -- | ------ |

All of the CSV files mentioned in this README are outputs of the following three executable scripts, located in the `voting_project` directory:
### create_pdf_database.py

This script, along with classes from `voting_project/src/classes/scraper`, performs web scraping. The `ParsedPage` class is used for sending requests, parsing pages, and extracting data from them. The main logic of the program is contained within the executable file itself. At the top of the file, you'll find functions responsible for extracting specific data from table rows and returning it in the form of dataclass objects. If you wish to modify the information collected during web scraping, this is where you should make changes.

**Input**: The script uses URL of the initial page provided in `constants.MAIN_URL` as input and saves the output CSV file to the location specified in `constants.PDF_DATABASE_PATH_OUTPUT`.

**Usage**: As the program has already been executed and the output stored in the `voting_project/src/data` directory, running the script again will overwrite the existing file. Before execution, it's recommended to change the path to the output file.

**Exceptions**: While most of the votings follow a standard format where individuals vote for or against a particular topic, there were six instances where Sejm members voted for a candidate. As these votings constitute less than 0.01% of the total amount, they are not included in the analysis. However, their URLs will be printed in the console after the program's execution for reference:
- https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=glosowaniaL&NrKadencji=9&NrPosiedzenia=63&NrGlosowania=60
- https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=glosowaniaL&NrKadencji=9&NrPosiedzenia=61&NrGlosowania=141
- https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=glosowaniaL&NrKadencji=9&NrPosiedzenia=47&NrGlosowania=126
- https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=glosowaniaL&NrKadencji=9&NrPosiedzenia=34&NrGlosowania=1
- https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=glosowaniaL&NrKadencji=9&NrPosiedzenia=31&NrGlosowania=18
- https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=glosowaniaL&NrKadencji=9&NrPosiedzenia=1&NrGlosowania=53

### create_main_database.py

This script, along with classes from `voting_project/src/classes/pdf_processing`, extracts data from PDF documents. The main logic of the program is contained within the executable file itself, where the target votes and data are specified and added to the output database, along with the structure of the output database.

**Input**: The script takes the output of the previous part of the program, the path to which is specified in `constants.PDF_DATABASE_PATH_INPUT`.

**Output**: The output CSV file is saved in `constants.MAIN_DATABASE_PATH_OUTPUT`.

**Exceptions**: While most of the votings have ordinary PDF documents, there were 15 instances where scans (no text to extract) were provided. As these votings constitute less than 0.02% of the total amount, they are not included in the analysis. However, their URLs will be printed in the console after the program's execution for reference.

### create_network.py

This script, along with a class from `voting_project/src/classes/network`, restructures the main database into a network. The `Network` class is used for storing data related to nodes and edges. The logic behind the network is explained in the project's Structure part of this README. 

**Input**: The script takes the output of the previous part of the program, located at `constants.MAIN_DATABASE_PATH_INPUT`.

**Output**: Nodes and edges CSV files are saved in `constants.EDGES_DATABASE_PATH_OUTPUT` and `constants.NODES_DATABASE_PATH_OUTPUT`, respectively.


# OUTRO
If you have any additional questions related to the project feel free to contact me:
- Email: martin.murzenkov@gmail.com 
- Telegram: @Martin554
