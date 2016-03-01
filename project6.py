"arkessler & irshusdock"
"Alexi Kessler & Ian Shusdock"
import sys
import random

LOG = False

"Node class for bayesian network"
"name is the name of the Node"
"parent1 is the first parent node"
"parent2 is the second parent node"
"cpt is the conditional prob table"
"status is the status of node(query, evidence, etc)"
class Node:
	def __init__(self, name, cpt):
		self.name = name
		self.parent1 = None
		self.parent2 = None
		self.cpt = cpt
		self.status = None
		self.value = None

	def set_parent1(self, parent1):
		self.parent1 = parent1

	def set_parent2(self, parent2):
		self.parent2 = parent2

	def set_status(self, status):
		self.status = status

	def print_out(self):
		print ("Node", self.name)
		if (self.parent1 != None):
			print ("-parent1:", self.name)
		if (self.parent2 != None):
			print ("-parent2:", self.parent2.name)
		print ("-status:", self.status)
		print ("-value:", self.value)

"Conditional probability table class"
"cpt_#_T/F correspond to the values of the cpt listed in the project specs"
class CPT:
	def __init__(self, list_of_cpt_values):
		self.cpt_1_F = (float)(list_of_cpt_values[0])
		self.cpt_1_T = (float)(list_of_cpt_values[1])

		if(len(list_of_cpt_values) == 2):
			return

		self.cpt_2_F = (float)(list_of_cpt_values[2])
		self.cpt_2_T = (float)(list_of_cpt_values[3])

		if(len(list_of_cpt_values) == 4):
			return	

		self.cpt_3_F = (float)(list_of_cpt_values[4])
		self.cpt_3_T = (float)(list_of_cpt_values[5])
		self.cpt_4_F = (float)(list_of_cpt_values[6])
		self.cpt_4_T = (float)(list_of_cpt_values[7])

	"Returns a value of true or false based on the CPT with no parents"
	def get_val_no_parents (self):
		return ((random.random()<self.cpt_1_T))

	"Returns a value of true or false based on the CPT with one parent"
	def get_val_one_parent (self, parent_val):
		if (parent_val):
			return ((random.random() < self.cpt_2_T))
		else:
			return ((random.random() < self.cpt_1_T))

	"Returns a value of true or false based on the CPT with two parents"
	def get_val_two_parents (self, parent1_val, parent2_val):
		if ((parent1_val != True) and (parent2_val!=True)):
			return (random.random() < self.cpt_1_T)
		elif ((parent1_val != True) and parent2_val):
			return (random.random() < self.cpt_2_T)
		elif (parent1_val and (parent2_val!=True)):
			return (random.random() < self.cpt_3_T)
		else:
			return (random.random() < self.cpt_4_T)

"Create a bayesian network using input from the passed file"
"filename is the name of the file to read from"
def create_bayesian_network(filename):
	
	f = open(filename)
	file_content = f.readlines()
	f.close()

	network = []

	"Initialize all nodes"
	for line in file_content:
		
		temp = line.split(" ")
		name = temp[0][:-1]
		cpt_values = parse_cpt_values(temp)

		network.append(Node(name, CPT(cpt_values)))

	"Set parents"
	for line in file_content:

		temp = line.split(" ")
		name = temp[0][:-1]

		if(temp[1] == "[]"):
			continue

		for node in network:
			if(node.name == name):
				parents = parse_parents(temp, network)
				node.set_parent1(parents[0])
				node.set_parent2(parents[1])

	return network

"Get the list of cpt values from the passed line"
"line_list is the list of strings in a line seperated by spaces"
def parse_cpt_values(line_list):
	if(line_list[1][-1] == "]"):
		line_list[2] = line_list[2][1:]
		line_list[-1] = line_list[-1][:-2]
		return line_list[2:]
	else:
		line_list[3] = line_list[3][1:]
		line_list[-1] = line_list[-1][:-2]
		return line_list[3:]

"Get the list of parent nodes from the passed line and network"
"line_list is the list of strings in a line seperated by spaces"
"node_network is the list of nodes"
def parse_parents(line_list, node_network):
	parents = []

	if(line_list[1][-1] == "]"):
		parents.append(line_list[1][1:-1])
		parents.append(None)
	else:
		parents.append(line_list[1][1:])
		parents.append(line_list[2][:-1])

	return parents

"Assign status to each node in a network based on input from a file"
"filename is the name of the file to read from"
"network is the bayesian network to set the status for"
def assign_status(filename, network):

	f = open(filename)
	file_content = f.readlines()
	f.close()

	file_content = file_content[0].split(",")
	file_content[-1] = file_content[-1][:-1]

	index = 0
	for node in network:
		node.set_status(file_content[index])
		index = index + 1

"Goes through the nodes in a network and updates all their parent assignments from strings"
"to actual nodes"
def change_parent_assigments_to_nodes(network):
	for node in network:
		if (node.parent1 != None):
			node.parent1 = find_node_by_name(network, node.parent1)
		if (node.parent2 != None):
			node.parent2 = find_node_by_name(network, node.parent2)

"Returns the node named"
def find_node_by_name(network, name):
	for node in network:
		if node.name == name:
			return node

"Generates a value of true or false for a node. Takes into account the cpt"
def gen_val(node, network):
	if (node.parent1 != None):
		if (node.parent1.value == None):
			node.parent1.value = gen_val(node.parent1, network)
		if (node.parent2 != None):
			if (node.parent2.value == None):
				node.parent2.value = gen_val(node.parent2, network)
			return node.cpt.get_val_two_parents(node.parent1.value, node.parent2.value)
		else:
			return node.cpt.get_val_one_parent(node.parent1.value)
	else:
		return (node.cpt.get_val_no_parents())

"Generate a sample from a given network"
def prior_sample(network):
	#TODO Implement this
	for node in network:
		if (node.value == None):
			node.value = gen_val(node, network)

"Checks the value of the query variable in a network"
def check_query_variable(network):
	for node in network:
		if (node.status == "q"):
			return node.value

"Check that a created net is consistent with the provided evidence variables"
def check_consistency(network):
	validity = True
	for node in network:
		if (node.status == "t"):
			if node.value != True:
				validity = False 
		if (node.status == "f"):
			if node.value != False:
				validity = False
	return validity

"Performs rejection sampling on the network for the given number of samples"
def rejection_sampling(network, sample_number):
	true_count = 0
	false_count = 0
	consistent_count = 0
	clear_network_values(network)
	for x in range(sample_number):
		prior_sample(network)
		if (check_consistency(network)):
			consistent_count+=1
			if (check_query_variable(network)):
				true_count+=1
			else:
				false_count+=1
		clear_network_values(network)
	if ((false_count+true_count)!=0):
		print ("Rejection Sampling probability:", (true_count)/(false_count+true_count))
		return (true_count/(false_count+true_count))
	else:
		print("Rejection Sampling probability: Not enough samples")
		return -1

"Both generates a consistent network, and finds the likelihood of this set of evidence variables occuring. Returns this as weight"
def weighted_sample (network):
	weight = 1
	"Make network consistent"
	for node in network:
		if (node.status == "t"):
			node.value = True
		if (node.status == "f"):
			node.value = False
	"Find weight of network"
	for node in network:
		if (node.status == "t" or node.status=="f"):
			gen_val(node, network)
			"If no parents"
			if (node.parent1 == None):
				if (node.value == True):
					weight = weight * node.cpt.cpt_1_T
				else:
					weight = weight * node.cpt.cpt_1_F
			"If one parent"
			if (node.parent1 != None and node.parent2 == None):
				if (node.parent1.value == True):
					if (node.value == True):
						weight = weight * node.cpt.cpt_2_T
					else:
						weight = weight * node.cpt.cpt_2_F
				else:
					if (node.value == True):
						weight = weight * node.cpt.cpt_1_T
					else:
						weight = weight * node.cpt.cpt_1_F
			"If two parents"
			if (node.parent1 != None and node.parent2!=None):
				if (node.parent1.value == False and node.parent2.value == False):
					if (node.value == True):
						weight = weight * node.cpt.cpt_1_T
					else:
						weight = weight * node.cpt.cpt_1_F
				if (node.parent1.value == False and node.parent2.value == True):
					if (node.value == True):
						weight = weight * node.cpt.cpt_2_T
					else:
						weight = weight * node.cpt.cpt_2_F
				if (node.parent1.value == True and node.parent2.value == False):
					if (node.value == True):
						weight = weight * node.cpt.cpt_3_T
					else:
						weight = weight * node.cpt.cpt_3_F
				if (node.parent1.value == True and node.parent2.value == True):
					if (node.value == True):
						weight = weight * node.cpt.cpt_4_T
					else:
						weight = weight * node.cpt.cpt_4_F
		else:
			node.value = gen_val(node, network)

	return weight

"Performs likelihood weighting on the network for the given number of samples"
def likelihood_weighting(network, sample_number):
	true_count = 0;
	false_count = 0;
	for x in range(sample_number):
		weight = weighted_sample(network)
		if (check_query_variable(network)):
			true_count+=weight 
		else:
			false_count+=weight 
	if ((true_count+false_count) != 0):
		print ("Likelihood weighting probability:", (true_count/(false_count+true_count)))
		return (true_count/(true_count+false_count))
	else:
		print ("Likelihood Weighting probability: Not enough samples")
		return -1

"Resets the values of nodes within a network"
def clear_network_values (network):
	for node in network:
		node.value = None

def project6_main():
	random.seed()
	if (LOG):
		f = open('output2.txt', 'a')
	network = create_bayesian_network(sys.argv[1])
	assign_status(sys.argv[2], network)
	change_parent_assigments_to_nodes(network)

	rejection_probability = str(rejection_sampling(network, int(sys.argv[3])))
	likelihood_probability = str(likelihood_weighting(network, int(sys.argv[3])))

	if (LOG):
		write_line = sys.argv[2] + "," + sys.argv[3] + "," + rejection_probability + "," + likelihood_probability + "\n"
		f.write(write_line)
if __name__ == '__main__':
	project6_main()		