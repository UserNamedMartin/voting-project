from src.data.constants import PDF_DATABASE_PATH_INPUT, MAIN_DATABASE_PATH_OUTPUT
import csv
from src.classes.pdf_processing.parsed_pdf import ParsedPDF
from tqdm import tqdm

pdfs_with_no_text = []

with open(PDF_DATABASE_PATH_INPUT) as pdf_database:
    reader = csv.reader(pdf_database)
    next(reader)

    with open(MAIN_DATABASE_PATH_OUTPUT, 'x') as main_database:
        writer = csv.writer(main_database)
        writer.writerow(('Voting ID','Voting Date','Voters ID','Voters Name','Voters Party','Voters Vote'))

        for row in tqdm(reader):

            voting_id = row[0]  # Unique combination of form: sejm_num-sejm_sub_num
            voting_date = row[1] # Date in form: day.month.year
            pdf_url = row[2]  # Absolute URL of PDF document with data about voting
            expected_votes = int(row[3]) # Expected number of "for" and "against" votes

            parsed_pdf_file = ParsedPDF(pdf_url)
            # If there is no text found, then we have a scan 
            if not parsed_pdf_file.lines:
                pdfs_with_no_text.append((voting_id, pdf_url))
                continue
            
            votes_and_voters = parsed_pdf_file.get_voters_by_vote_statuses(('za', 'pr.'))
                
            # We need to check if program found all people
            total_num_of_votes = sum(len(lst) for lst in votes_and_voters.values())
            if total_num_of_votes != expected_votes:
                raise Exception(f'Expected number of target votes: {expected_votes}. Actual number is {total_num_of_votes}')
                
            for vote_status, list_of_voters in votes_and_voters.items():

                for voter in list_of_voters:

                    writer.writerow((
                        voting_id,
                        voting_date,
                        voter.identifier,
                        voter.name, 
                        voter.party,
                        vote_status
                    ))

print('PDF documents with no text found inside:')
for id_and_url in pdfs_with_no_text:
    print(id_and_url)