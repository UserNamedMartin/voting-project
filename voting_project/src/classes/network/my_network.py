class Network():
    '''
    Represents simplified version of Undirected Graph data structure designed to meet specific needs.

    Stores Nodes in form of a dictionary, where key is an unique ID of a Node
    and value is a data related to it. Both specified by a user.
    Stores Edges in form of a dictionary, where key is a tuple with sorted IDs of two Nodes
    and value is a weight between them.

    Attributes:
    - nodes (dict[int, any]): A dictionary where each key is unique ID of a Node and value is data related to it.
    - edges (dict[tuple[int], int]): A dictionary where each key is a sorted tuple with two Nodes IDs and value is weight of connection between them.
    '''
    def __init__(self) -> None:
        '''
        Creates a new instance of Network class.
        '''
        self._nodes = {}
        self._edges = {}
    
    def add_edges_for_all(self, nodes_to_connect: list[tuple]) -> None:
        '''
        Adds Undirected Edges between all the Nodes in the list (increase weight on 1 if Edge exist).

        Arguments:
        - nodes (list[tuple]): A list of tuples, where each tuple represents a Node and contains exactly two elements: ID (int) and Data (any).

        Returns:
        - None: Adds Edges.
        '''
        self._add_nodes(nodes_to_connect)

        for i in range(len(nodes_to_connect)):
            for j in range(i + 1, len(nodes_to_connect)):
                self._add_edge(nodes_to_connect[i][0], nodes_to_connect[j][0])

        
    def _add_nodes(self, nodes_to_add: list[tuple]) -> None:
        '''
        Adds all the nodes from the list to self.nodes.

        Arguments:
        - nodes (list[tuple]): A list of tuples, where each tuple represents a Node and contains exactly two elements: ID (int) and Data (any).

        Returns:
        - None: Adds Nodes to self.nodes
        '''
        for node_id, node_data in nodes_to_add:
            # If this is new node, we need to add it to nodes
            if not node_id in self._nodes:
                self._nodes[node_id] = node_data
            # If existing ID is given but with incorrect data
            elif self._nodes[node_id] != node_data:
                raise Exception(f'Node with ID {node_id} already exists with following data:\n{self._nodes[node_id]}\nProvided data:\n{node_data}')
    
    def _add_edge(self, sourse_id: int, target_id: int) -> None:
        '''
        Adds an undirected edge between two Nodes.
        '''
        key_tuple = tuple(sorted((sourse_id, target_id)))
        self._edges[key_tuple] = self._edges.get(key_tuple, 0) + 1

    @property
    def nodes(self) -> dict[int, any]:
        return self._nodes
    
    @property
    def edges(self) -> dict[tuple, int]:
        return self._edges
    
