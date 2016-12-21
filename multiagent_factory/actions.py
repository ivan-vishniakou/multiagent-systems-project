# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan, ben, eugenia
"""

from base import *
from pieces import *

class Tasks():
	MACHINETASK = 'MACHINETASK'
	TRANSPORTTASK = 'TRANSPORTTASK'
	
class Task(UObject):
	def __init__(self, o_type=UObjects.TASK, timestamp=0.0):
		super(Task, self).__init__(o_type=UObjects.TASK)

class MachineTask(Task):
	"""Class representing a task performed by a mobile robot.
	Contains attributes of a part and operation type to perform
	on a matching part."""

	def __init__(self, pieces, req_attr, operations, timestamp=0.0):
		super(MachineTask, self).__init__(o_type=Tasks.MACHINETASK, timestamp=0.0)
		self.timestamp = timestamp
		self.pieces = pieces # list
		self.req_attr = req_attr # list of sets
		self.operations = operations # set

	def __repr__(self):
		return self.__str__()

class TransportTask(Task):
	def __init__(self, piece, dest_machine, timestamp=0.0):
		super(TransportTask, self).__init__(o_type=Tasks.TRANSPORTTASK, timestamp=0.0)
		self.timestamp = timestamp
		self.piece = piece
		self.dest_machine = dest_machine

	def __repr__(self):
		return self.__str__()

class Operations():
	"""Class listing the available operations"""
	PROCURE = 'PROCURE'
	DELIVER = 'DELIVER'
	ROLL = 'ROLL'
	DRILL_BIG = 'DRILL_BIG'
	DRILL_FINE = 'DRILL_FINE'
	COAT = 'COAT'
	FORCE_FIT = 'FORCE_FIT'

class Operation():

	def __init__(self, name, accepts_pcs, requires_pcs, combines_pcs, adds_attr, removes_attr, requires_attr):
		self.name = name 					# Name of operation

		self.accepts_pcs = accepts_pcs		# set of accepted components
		self.requires_pcs = requires_pcs	# list of pcs required for operation - if populated, accepts_pcs is ignored
		self.combines_pcs = combines_pcs    # list of set and piece: destroyed indexes of requires_pcs and created pc

		self.adds_attr = adds_attr 			# list of set of attributes added to pcs
		self.removes_attr = removes_attr 	# list of set of attributes removed from pcs
		self.requires_attr = requires_attr	# list of set of attributes required for operation

class Procure(Operation):
	def __init__(self):
		super(Procure, self).__init__(Operations.PROCURE,
		[Pieces.BLOCK, Pieces.BEARING, Pieces.ASSY_TRAY],
		[], [],
		[set()], [set()], [set()])

class Deliver(Operation):
	def __init__(self):
		super(Deliver, self).__init__(Operations.DELIVER,
		[Pieces.BLOCK, Pieces.BEARING, Pieces.ASSY],
		[], [],
		[set()], [set()], [set()])

class Roll(Operation):
	def __init__(self):
		super(Roll, self).__init__(Operations.ROLL,
		[Pieces.BEARING],
		[], [],
		[[Attributes.ROLLED]], [set()], [set()])

class DRILL_BIG(Operation):
	def __init__(self):
		super(DRILL_BIG, self).__init__(Operations.DRILL_BIG,
		[Pieces.BLOCK],
		[], [],
		[set(Attributes.BIG_DRILLED)], [set()], [set()])

class DRILL_FINE(Operation):
	def __init__(self):
		super(DRILL_FINE, self).__init__(Operations.DRILL_FINE,
		[Pieces.BLOCK],
		[], [],
		[set(Attributes.FINE_DRILLED)], [set()], [set()],)

class COAT(Operation):
	def __init__(self):
		super(COAT, self).__init__(Operations.COAT,
		[Pieces.BLOCK],
		[], [],
		[set(Attributes.COATED)], [set()], [set()] )

class FORCE_FIT(Operation):
	def __init__(self):
		super(FORCE_FIT, self).__init__(Operations.FORCE_FIT,
		[],
		[Pieces.BLOCK, Pieces.BEARING, Pieces.ASSY_TRAY], [[0, 1],Pieces.BEARING_BLOCK_ASSY],
		[set(),set(),set()], [set(Attributes.BIG_DRILLED),set(),set()], [set(Attributes.BIG_DRILLED),set(),set()] )

