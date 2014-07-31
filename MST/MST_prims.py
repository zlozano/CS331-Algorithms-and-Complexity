# --------------
# Zachary Lozano
# 10.19.13
# CS331
# --------------

import sys
import os
import re
import collections
from Queue import PriorityQueue
from Node import *
from Edge import *

"""
This Algorithm is Prim's algorithm
"""

# --------
# MST_read
# --------

def MST_read (r, al, nodes) :
	"""
	reads in the input of a tree structure into
	an adjacency list
	r is a reader
	al is a dictionary of lists
	nodes is a dictionary of all nodes
	"""

	c1 = c2 = p = ""

	for l in r.readlines() :
		node = Node()
		node_info = re.findall('\d+', l)
		for i in xrange(0, len(node_info) + 1, 2):
			if i == 0 :														# if element is the node id
				node.ID = node_info[0]
				nodes.update({node.ID : node})								# create entry in the node list
				al.update({node.ID : []})									# create entry in adjeceny list
			else :
				al[node_info[0]].append([node_info[i-1], node_info[i]])		# adding (b, w) to list

# ----------
# build_tree
# ----------

def build_tree (al, nodes) :
	"""
	Takes in an adjacency list, set of all nodes, and the edge set
	and builds a tree, and contructs edges.
	al is an adjacency list
	nodes dictionary of all nodes
	edges will be the Priority Queue of all edges
	"""

	for n in al :
		for node_info in al[n] :
			e = Edge()
			e.weight    = int(node_info[1])
			e.next_node = nodes[node_info[0]]
			e.src_node  = nodes[n]
			nodes[n].neighbors.append(nodes[node_info[0]])		# append adjacent node...
			nodes[n].weights.append(e)							# and its corresponding weight
		
# --------
# find_MST
# --------

def find_MST(nodes, MST) :
	"""
	This function will find the MST within the tree givin by nodes
	nodes is a dictionary of nodes where the key is the node ID
	MST is a dictionary where the MST will be stored
	"""

	frontier = PriorityQueue()				# PQ of available edges
	visited  = dict()						# dictionary of nodes that have already made it into the MST
	current_node = next(nodes.itervalues())	# get an arbitrary node to start
	visited.update({current_node.ID : current_node})
	skip = True

	for edge in current_node.weights :		# initial fill for start node
		frontier.put(edge)

	while not frontier.empty() :
		if not skip :
			for edge in current_node.weights :
				frontier.put(edge)
		
		edge = frontier.get()				# get the cheapest node
		current_node = edge.src_node
		
		if edge.next_node.ID in visited :	# if we have created a cycle
			skip = True
			pass
		else :								# add to MST
			if current_node.ID not in MST :
				MST.update({current_node.ID : [edge.next_node.ID]})
				# Becasue the output is reflexive, if we say a is conntected to
				# b, we should also say b is connected to a. This is what the 
				# following statement accomplishes.
				if edge.next_node.ID not in MST :
					MST.update({edge.next_node.ID : [current_node.ID]})
				else :
					MST[edge.next_node.ID].append(current_node.ID)
			else :
				MST[current_node.ID].append(edge.next_node.ID)
				# Becasue the output is reflexive, if we say a is conntected to
				# b, we should also say b is connected to a. This is what the 
				# following statement accomplishes.
				if edge.next_node.ID not in MST :
					MST.update({edge.next_node.ID : [current_node.ID]})
				else :
					MST[edge.next_node.ID].append(current_node.ID)

			current_node = edge.next_node
			visited.update({current_node.ID : current_node})
			skip = False				
			

# ----
# main
# ----

def main() :
	nodes    = dict()					# All nodes
	al	     = dict()					# store the input data
	MST      = dict()					# the minimum spanning tree
	f        = open('mst.out', 'w')		# output file

	MST_read(sys.stdin, al, nodes)		# read input into adjacency list
	build_tree(al, nodes)				# build tree from adjacency list
	find_MST(nodes, MST)

	ordered_MST = collections.OrderedDict(sorted(MST.items()))

	for i in ordered_MST :				# write out to file
		ordered_MST[i].sort()
		f.write(i + " (")
		for j in ordered_MST[i] :
			f.write(j + ",")
		f.seek(-1, os.SEEK_END)
		f.truncate()
		f.write(")\n")
	f.close()

main()
