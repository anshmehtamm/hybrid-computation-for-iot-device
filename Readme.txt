Code for project titled Collaborative Deployment Strategy for Hybrid Computation in the Internet of Things Environment.

Prequisites for running on local setup

	1. Python 3.8 or newer
	2. pip (for installing dependent libraries)
	3. openpyxl library (for exporting results to MS Excel)
	4. matplotlib (for plotting)
	5. sklearn (implementing the distance based clustering) 


Project Structure and Files

1. node.py - Class definition of a node object
2. setupNodes.py- Methods for setting up deployment and initialization of nodes.
3. graph_clustering.py -Implementation and Visualization of Graph Based Clustering.
4. heurisitic_clustering.py - Implementation and Visualization of Heurisitic Based Clustering.
5. distance_clustering.py - Implementation and Visualization of Distance Based Clustering.
6. Token.py - Class definition of a token object used for communication.
7. server.py - Server implementation for a node using client-server mode of communication.
8. client.py - Client implementation for a node using client-server mode of communication.
9. distributed_client.py - Distributed Server implementation distributed mode of communication.
10. distributed_server.py - Distributed Client client-server mode of communication.
11. event.py - Class definition of an Event object for simulating event driven scenario.
12. generateEvents.py - Implementation to generate events in the terrain.
13. clustering.py - Script used for testing and simulating the implemented clustering techniques.
14. connectivity.py - Script used for testing the connectivity in the depsloyment.
15. coverage.py - Script used for testing the coverage in the deployment.
16. test_clustering.py - Master Script to generate and report an integrated test for comparing different strategies proposed. (name of the file may be confusing.)