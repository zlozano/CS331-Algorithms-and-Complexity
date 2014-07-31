#!/usr/bin/env python

# ----------
# Edge.py
# Zac Lozano
# 10.19.13
# ----------

from Node import *

class Edge :
	def __init__(self) :
		self.weight	   = 0
		self.next_node = Node()
		self.src_node  = Node()

	def __lt__(self, other) :
		return int(self.weight) < int(other.weight)

	def __str__(self) :
		return str(self.weight)
		"""
		return "[" + str(self.node_a) + \
				"," + str(self.weight) + \
				"," + str(self.node_b) + "]"
		"""
