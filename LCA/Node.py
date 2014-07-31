#!/usr/bin/env python

# ----------
# Node.py
# Zac Lozano
# 10.9.13
# ----------

class Node :
	def __init__(self) :
		self.ID      = ""
		self.parent  = None
		self.child1  = None
		self.child2  = None
		self.is_root = False
		self.level   = -1
		self.leaves  = []

	def __str__(self) :
		return self.ID

	def is_element_of(self, collection) :
		for node in collection :
			if self.ID == node.ID :
				return True
		return False
		
