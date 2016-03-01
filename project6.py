"arkessler & irshusdock"
"Alexi Kessler & Ian Shusdock"
import sys

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
		self.status = ""

	def set_parent1(self, parent1):
		self.parent1 = parent1

	def set_parent2(self, parent2):
		self.parent2 = parent2

	def set_status(self, status):
		self.status = status

	def print_out(self):
		print ("Node", self.name)
		if (self.parent1 != None):
			print ("-parent1:", self.parent1)
		if (self.parent2 != None):
			print ("-parent2:", self.parent2)
		print ("-status:", self.status)

"Conditional probability table class"
"cpt_#_T/F correspond to the values of the cpt listed in the project specs"
class CPT:
	def __init__(self, list_of_cpt_values):
		self.cpt_1_F = list_of_cpt_values[0]
		self.cpt_1_T = list_of_cpt_values[1]

		if(len(list_of_cpt_values) == 2):
			return

		self.cpt_2_F = list_of_cpt_values[2]
		self.cpt_2_T = list_of_cpt_values[3]

		if(len(list_of_cpt_values) == 4):
			return	

		self.cpt_3_F = list_of_cpt_values[4]
		self.cpt_3_T = list_of_cpt_values[5]
		self.cpt_4_F = list_of_cpt_values[6]
		self.cpt_4_T = list_of_cpt_values[7]

	"Returns a value of true or false based on the CPT with no parents"
	def get_val_no_parents (self):
		return ((random.random<self.cpt_1_T))

	"Returns a value of true or false based on the CPT with one parent"
	def get_val_one_parent (self, parent_val):
		if (parent_val):
			return ((random.random < self.cpt_2_T))
		else:
			return ((random.random < self.cpt_1_T))

	"Returns a value of true or false based on the CPT with two parents"
	def get_val_two_parents (self, parent1_val, parent2_val):
		if ((parent1_val != True) and (parent2_val!=True)):
			return (random.random() < self.cpt_1_T)
		elif ((parent1_val != True) and parent2_val):
			return (random.random() < self.cpt_2_T)
		elif (pareant1_val and (parent2_val!=True)):
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

"Generate a sample from a given network"
def prior_sample(network):
	#TODO Implement this
	print ("prior_sample")

def project6_main():
	network = create_bayesian_network(sys.argv[1])
	assign_status(sys.argv[2], network)

	for node in network:
		node.print_out()

if __name__ == '__main__':
	project6_main()		