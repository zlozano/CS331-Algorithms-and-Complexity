#!/usr/bin/env python

# ----------
# LCA.py
# Zac Lozano
# 10.9.13
# ----------

import sys
import os
import re
from Node import *

# --------
# LCA_read
# --------

def LCA_read (r, al) :
	"""
	reads in the input of a tree structure into
	an adjacency list
	r is a reader
	al is a dictionary of lists 
	"""

	c1 = c2 = p = ""

	for l in r.readlines() :
		node_info = []            # the inner list of node info [c1, c2, p]
		s    = l.split()

		node = s[0]
		children = re.findall('\d', s[1])
		parent   = re.findall('\d', s[2])

		if len(children) > 0 :
			c1 = children[0]
		if len(children) > 1 :
			c2 = children[1]
		if len(parent) > 0 :
			p  = parent[0]

		node_info.append(c1)
		node_info.append(c2)
		node_info.append(p)
		al[node] = node_info

		c1 = c2 = p = ""

# --------------
# construct_tree
# --------------

def construct_tree(n, al, nodes, tree) :
	"""
	Takes in a node and an adjacency list and sets a node's children 
	and level.  Also takes in a dictionary to store groupings of level nodes
	n is the current node
	al is an adjacency list (dictionary of lists)
	nodes is a dictionary of lists
	tree will be the entire collection of nodes, indexible by their ID
	"""

	child1 = Node()
	child2 = Node()
	parent = Node()

	node_data = al[n.ID]			# [c1, c2, p]

	if node_data[0] != '' :			# has left child
		child1.ID     = node_data[0]
		child1.level  = n.level + 1
		child1.parent = n
		construct_tree(child1, al, nodes, tree)
		n.child1 = child1
	if node_data[1] != '' :			# has right child
		child2.ID     = node_data[1]
		child2.level  = n.level + 1
		child2.parent = n
		construct_tree(child2, al, nodes, tree)
		n.child2 = child2
	
	if n.level not in nodes :	# has not been added to yet, hence not created
		nodes[n.level] = []

	nodes[n.level].append(n)		# add node to its level
	tree[n.ID] = n
	return n

# ------
# leaves
# ------

def leaves(n) :
	"""
	This will compute the set of all leaves under node n
	n is a Node
	"""
	n.leaves.append(n)			# add itself to the set of leaves
	if n.child1 is not None :
		n.leaves.extend(n.child1.leaves)	# union
	if n.child2 is not None :
		n.leaves.extend(n.child2.leaves)	# union
		
# -----------
# compute_lca
# -----------

def compute_lca(lcam, nodes) :
	"""
	This function will compute the LCA matrix based off of the 
	computed leaves values
	lcam is the LCA matrix
	nodes is a dictionary of nodes
	"""
	for i in xrange(len(lcam)) :
		for j in xrange(len(lcam[i])) :

			if nodes[str(i+1)].is_root : 
				lcam[i][j] = nodes[str(i + 1)].ID
			elif nodes[str(j+1)].is_root : 
				lcam[i][j] = nodes[str(j + 1)].ID
			elif i == j :
				lcam[i][j] = nodes[str(i + 1)].ID		# LCA(x, x) = x
			else :
				tmp = Node()			# temporary node used to check leaf set of a node
				tmp = nodes[str(i+1)]
				while lcam[i][j] == '0'	:				# go thorugh leaves of parents until we find both nodes
					if nodes[str(i+1)].is_element_of(tmp.leaves) and \
					   nodes[str(j+1)].is_element_of(tmp.leaves) :
						lcam[i][j] = tmp.ID
					else :
						tmp = tmp.parent
			
# ----
# main
# ----

def main() :

	f = open('lca.out', 'w')

	adjacency_list = {} 				# read the file into this
	leaf_ordering  = {}					# this is how we will group together nodes of equal level
	tree           = {}					# a collection of the nodes
	lca_matrix     = []					# the lca matrix we eventually want to fill
	nodes          = 0					# number of nodes

	LCA_read(sys.stdin, adjacency_list)

	root = Node()
	root.level = 0
	root.is_root = True

	for n in adjacency_list :			# find our root so that we can mark depth
		if adjacency_list[n][2] == '' :
			root.ID = n
		nodes += 1

	construct_tree(root, adjacency_list, leaf_ordering, tree)	# link nodes together, and group level leaves

	for level in reversed(xrange(len(leaf_ordering))) :		# starting at the lowest level
		for node in leaf_ordering[level] :
			leaves(node)								# compute all leaves under node

	lca_matrix = [['0'] * nodes for i in range(nodes)]	
	compute_lca(lca_matrix, tree)

	for line in lca_matrix :
		for elem in line :
			f.write(elem + " ")
		f.seek(-1, os.SEEK_END)
		f.truncate()
		f.write("\n")

	f.close()
main()
