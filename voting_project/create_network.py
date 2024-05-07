import csv
from src.data.constants import MAIN_DATABASE_PATH_INPUT, NODES_DATABASE_PATH_OUTPUT, EDGES_DATABASE_PATH_OUTPUT
from src.classes.network.my_network import Network
from tqdm import tqdm

# Database starts with voting 81-1
cur_voting_id = '81-1'
network = Network()
voters_for = []
voters_against = []

with open(MAIN_DATABASE_PATH_INPUT) as main_database:
    reader = csv.reader(main_database)
    next(reader)

    for row in tqdm(reader):

        voting_id = row[0]
        voter_id = int(row[2])
        voter_name = row[3] 
        voter_party = row[4] 
        voter_vote = row[5]
        
        # Need to update Edges for each voting
        if cur_voting_id != voting_id:
            network.add_edges_for_all(voters_for)
            network.add_edges_for_all(voters_against)
            voters_for = []
            voters_against = []
            cur_voting_id = voting_id
        
        # ID must be provided as a first item, data as a second
        if voter_vote == 'za':
            voters_for.append((
                voter_id,
                (voter_name, voter_party)
            ))
        if voter_vote == 'pr.':
            voters_against.append((
                voter_id,
                (voter_name, voter_party)
            ))
    network.add_edges_for_all(voters_for)
    network.add_edges_for_all(voters_against)
    


# Create Nodes .csv database
with open(NODES_DATABASE_PATH_OUTPUT, 'w') as nodes_database:
    writer = csv.writer(nodes_database)
    writer.writerow(('ID', 'Full Name', 'Party'))

    for voter_id, voter_data in network.nodes.items():
        voter_name, voter_party = voter_data
        writer.writerow((
            voter_id,
            voter_name,
            voter_party
        ))

# Create Edges .csv database
with open(EDGES_DATABASE_PATH_OUTPUT, 'w') as edges_database:
    writer = csv.writer(edges_database)
    writer.writerow(('Sourse', 'Target', 'Type', 'ID', 'Weight'))
    edge_id = 1

    for sourse_and_target, weight in network.edges.items():
        sourse, target = sourse_and_target
        writer.writerow((
            sourse,
            target,
            'Undirected',
            edge_id,
            weight
        ))
        edge_id += 1
