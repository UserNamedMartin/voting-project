from dataclasses import dataclass

@dataclass
class Person():
    '''
    Represents Polish Sejm member and data related to him.

    Attributes:
    - name (str): Name and Surname of a person.
    - party (str): Political party of a person.
    - identifier (int): Unique identifier of a person based on his full name and party.
    '''
    name: str
    party: str
    
    # For people IDs inspection and generation
    _people_ids = {}
    _next_id = 1000

    def __post_init__(self) -> None:
        assert isinstance(self.name, str), "name must be of type str"
        assert isinstance(self.party, str), "party must be of type str"
        
        name_and_party = self.name + ' ' + self.party
        if name_and_party in Person._people_ids:
            self.identifier = Person._people_ids[name_and_party]
        else:
            Person._people_ids[name_and_party] = Person._next_id
            self.identifier = Person._next_id
            Person._next_id += 1