#!/usr/bin/env python

# ----------
# Node.py
# Zac Lozano
# 10.i9.13
# ----------

class Node :
	def __init__(self) :
		self.ID         = ""
		self.neighbors  = []		# list of adjacent node IDs
		self.weights    = []		# list of corresponding weights

	def __str__(self) :
		return self.ID

	def is_element_of(self, collection) :
		for node in collection :
			if self.ID == node.ID :
				return True
		return False
		
