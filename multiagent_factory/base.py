# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan, ben, eugenia
"""

#INFINITY = float('inf')

class UObjects():
	MACHINE = 'MACHINE'
	PIECE = 'PIECE'
	TASK = 'TASK'
	ORDER = 'ORDER'

class UObject(object):
	"""Base class for objects in the simulation providing unique ids."""
	uid = 0 #Static counter of objects
	
	@staticmethod
	def get_new_uid():
		UObject.uid += 1
		return UObject.uid - 1

	def __init__(self, o_type = 'UOBJECT'):
		self.uid = UObject.get_new_uid()
		self.o_type = o_type

	def __str__(self):
		return '{}[#{}]'.format(self.o_type, str(self.uid).zfill(3))

	def __repr__(self):
		return self.__str__()


class PhysicalObject(UObject):
	"""Adds position and attributes to UObject to describe physical
	objects, like work pieces and agents.
	"""

	def __init__(self, o_type = 'PHYS_OBJECT', pos = [0,0], attributes = []):
		super(PhysicalObject, self).__init__(o_type = o_type)
		'''attributes shouldn't be duplicated in the first place'''
		#self.attributes = set(attributes)
		self.attributes = attributes
		self.pos = pos

	def matches(self, required):
		"""Checks if instances' set has all the attributes of the required."""
		provided = self.attributes
		for attr in required:
			if not attr in provided:
				return False
		for attr in provided:
			if not attr in required:
				return False
		return True
        
	#def __str__(self):
	#	return '{} {}'.format(self.o_type, str(self.uid).zfill(2))
