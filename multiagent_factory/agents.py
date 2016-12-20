# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:55:08 2016

@author: ivan, ben, eugenia
"""
#import spade
from base import *
from actions import *
from math import copysign
import random
import abc

class Agents():
	STOCK_MACHINE = 'STOCK_MACHINE'
	DELIVERY_MACHINE = 'DELIVERY_MACHINE'
	ROLLING_MACHINE = 'ROLLING_MACHINE'
	BIG_DRILLING_MACHINE = 'BIG_DRILLING_MACHINE'
	FINE_DRILLING_MACHINE = 'FINE_DRILLING_MACHINE'
	COATING_MACHINE = 'COATING_MACHINE'
	PRESS_MACHINE = 'PRESS_MACHINE'

class Agent(PhysicalObject):
	"""Base class for agents in the factory"""

	def __init__(self, factory, pos = [0, 0], o_type = 'AGENT'):
		super(Agent, self).__init__(o_type = o_type, pos=pos)
		self.progress = 0.0
		self._factory = factory
		self._busy = False

	@abc.abstractmethod
	def tick(self, dt=1):
		"""Simulation step of an agent"""
		pass
        
class Transporter(Agent):

	def __init__(self, factory, pos=[0,0]):
		super(Transporter, self).__init__(factory, o_type='TRANSPORTER', pos=pos)
		self._busy = False
		self._progress = 0.0
		self._move_goal = None
		self._task = None
		self._carried_piece = None
		self._current_task = None
		self._max_vel = .1

	def _pick_piece(self, piece):
		self._current_task.piece.owner = self
		self._carried_piece = self._current_task.piece
		self._move_goal = self._current_task.dest_machine.pos
		print '{} picked {}'.format(self, self._carried_piece)

	def _drop_piece(self):
		piece = self._carried_piece
		piece.owner = None
		self._carried_piece = None
		self._task = None
		self._set_move_goal(None)
		return piece

		print '{} dropped {}'.format(self, self._carried_piece)

	def _move_to_goal(self):
		if self._move_goal is None:
			return
		else:
			for ax in [self._prim_axis, not self._prim_axis]:
				if (abs(self._move_goal[ax]-self.pos[ax])>self._max_vel):
					self.pos[ax] += copysign(self._max_vel, self._move_goal[ax]-self.pos[ax])
					return
				elif (abs(self._move_goal[ax]-self.pos[ax])>self._max_vel*0.1):
					self.pos[ax] = self._move_goal[ax]
					return
				pass
			pass
		pass

	def _at_goal(self):
		"""Checks if Transporter is within small proximity to goal."""
		return (abs(self._move_goal[0]-self.pos[0]) +
				abs(self._move_goal[1]-self.pos[1]) )<0.1*self._max_vel

	def _select_task(self):
		if len(self._factory.transport_tasks) > 0:
			self._current_task = self._factory.transport_tasks.pop(0)
			self._move_goal = self._current_task.piece.pos

	def tick(self, dt=1):
		if self._current_task is None:
			self._select_task()
		else:
			if self._at_goal():
					if self._carried_piece is None:
						self._pick_piece(machine.output_piece(
									self._current_task.piece))
					else:
						self._current_task.dest_machine.input_piece(
												self._drop_piece())
			else:
				self._move()

class Machine(Agent):
	"""Stationary machine able to perform one or more operations"""
	def __init__(self, factory, agent_type, operations,
				 pos, productivity = 0.005, name='',
				 o_type='MACHINE'):
		super(Machine, self).__init__(factory,
									  pos=pos,
									  o_type=o_type)

		self.agent_type = agent_type
		self.operations = operations # set of operations
		self.productivity = productivity
		self._busy = False
		self._progress = 0.0
		self._current_task = None
		self._tasks=[]
		self.input = []
		self._table = []
		self.output = []

	def input_piece(self, piece):
		print '{} INPUT PIECE {}'.format(self, piece)
		piece.owner = self
		piece.reserved = True
		self.input.append(piece)

	def output_piece(self, piece):
		if piece in self.output:
			self.output.remove(piece)
			piece.owner = None
			return piece
		else:
			return None

	# TODO - Add lookahead that selects task based on piece transport time
	#       and time left for current task
	def tick(self, dt=1):
		"""Time tick for the machine: increases progress if there is an
		item in work, """
		# instead of a look-ahead, always choose 1 task in advance
		if len(self._tasks) < 1:
			self._select_task()
		if self._current_task is None:
			if len(self._tasks)>0:
				self._start_task()
		else:
			if self._progress>1.0:
				self._perform_operation
				self._progress = 0.0
			else:
				self._progress += self.productivity*dt
			
	def _perform_operation(self):
		operation = self._current_task.operation[0]
		for i in range(len(task.pieces)):
			self._worktable[i].attributes.add(operation.adds_attr[i])
			self._worktable[i].attributes.remove(operation.removes_attr[i])
		if len(requires_pcs) > 0: # combination procedure
			attr = set()
			for index in combines_pcs[0]: # pass attributes to new piece
				attr.add(self._worktable[index].attributes)
			indexes = sorted(combines_pcs[0],reverse=True)
			for i in indexes:
				self._factory.remove(self._worktable[i])
				self._worktable[i].pop
			p = Piece(self, operation.combination[1], attributes = attr)
			self._factory.pieces.add(p)
			self.output.append(p)
		for piece in self._worktable:
			self.output.append(piece)
			piece.reserved = False
		self._worktable = []
		print '{} finished task {}'.format(self, self._current_task)
		self._current_task = None

	def _start_task(self):
		"""Look for pieces in input and if there, put in worktable"""
		for task in self._tasks:
			for i, piece in enumerate(task.pieces):
				found_piece = False
				for piece in self.input:
					if ((piece.piece_type is piece) and
							(task.req_attr[i] == piece.attributes)):
						found_piece = True
						# piece list is in order of task/recipe
						self._table.append(self.input.pop(piece))
						break
				if found_piece == False:
					self.input.append(self._table) # return all pieces
					self._table = []
					break
			if found_piece == True:
				self._current_task = self._tasks.pop(task)
				print '{} started task {}'.format(self, self._current_task)
				break

	# select the oldest task that the machine is able to do
	def _select_task(self):
		
		doable = []
		fulfillable = []

		for task in self._factory.machine_tasks:
			for operation in task.operations:
				if operation in self.operations:
					doable.append(task)
					
					#TODO - remove following debug line
					print '{}: doable add'.format(self.__str__())
		if len(doable)>0:
			for task in doable:
				pcs_available = True
				reserved_pcs = []
				# see if enough pieces exist with required attributes
				for i, piece_type in enumerate(task.pieces):
					suiting_pieces = self._find_suiting_pieces(piece_type,task.req_attr[i])
					if len(suiting_pieces)>0:
						# temporarily reserve piece to account for processes that require multiple of same type
						suiting_pieces[0].reserved = True
						reserved_pcs.append(suiting_pieces[0])
					else:
						pcs_available = False
						break
				if len(reserved_pcs) > 0:
					for pc in reserved_pcs:
						# remove temporary reservation
						pc.reserved = False
				if pcs_available == True:
					fulfillable.append(task)
					
					#TODO - remove following debug line
					print '{}: fulfillable add'.format(self.__str__())
		else:
			return
		selected_task = None
		selected_pcs = []
		if len(fulfillable)>0:
			selected_task = fulfillable[0]
			for task in fulfillable: # pick oldest task
				if (task.timestamp < selected_task.timestamp):
					selected_task = task
			# TODO - implement piece-choosing heuristic
			for i, piece in enumerate(task.pieces):
				suiting_pieces = self._factory.find_piece_with_attr(piece,task.req_attr[i])
				if len(suiting_pieces) > 0:
					selected_piece = random.choice(suiting_pieces)
					selected_piece.reserved = True
					selected_pcs.append(selected_piece)
				self._factory.transport_tasks.add(TransportTask(piece, self, self._factory.time)) # create transport tasks for all the reserved pieces
			if len(task.operations)>1: # task may contain multiple operations - select one the machine is capable of and modify task
				for op in selected_task.operations:
					if op in self.operations:
						operation = op
						break
				self._tasks.append(MachineTask(selected_task.pieces, selected_task.req_attr, set(operation)))
				# TODO - make this work for operations that are more complex than attr modification
				for i in len(selected_task.pieces):
					if selected_task.pieces[i] in operation.accepts_pcs:
						for attr in operation.adds_attr:
							selected_task.req_attr[i].add(attr)
						for attr in operation.removes_attr:
							selected_task.req_attr[i].remove(attr)
					else:
						print '{} operation not valid for type {}'.format(operation.name,selected_task.pieces[i])
				selected_task.operations.remove(operation)
			else:
				self._tasks.add(task)
				self._factory.tasks.remove(task)
		else:
			return

	def _find_suiting_pieces(self, piece_type, attrs):
		return self._factory.find_piece_with_attr(piece_type,attrs)

	def does_operation(self, operation):
		return self.operation == operation

	def production_time(self):
		return 1.0/self.productivity

	def __str__(self):
		return '{}:{}'.format(self.agent_type, str(self.uid).zfill(2))

class Stock(Machine):
	def __init__(self, factory, pos, name=''):
		super(Stock, self).__init__(factory,
									agent_type = Agents.STOCK_MACHINE,
									operations = Operations.PROCURE,
									pos=pos,
									productivity = 0.005,
									name=name)
	'''
	def __init__(self, factory, initial_stock, pos, name=''):
		super(Stock, self).__init__(factory,
									operations='STOCK',
									productivity = 0.05,
									pos=pos,
									name=name, o_type='STOCK')
		self.stock = []
		for issue in initial_stock:
			self.input_piece(Piece(self, issue[0], issue[1]))

	def tick(self, dt=1):
		"""Time tick for the machine: increases progress if there is an
		item in work, puts in the output when comlete and picks new
		from input."""
		if self._current_piece is None:
			if len(self.input)>0:
				self._current_piece = self.input.pop(0)
				print '{} fetched piece  {}'.format(self,self._current_piece)
				self._progress = 0.0
			pass
		else:
			if self._progress>1.0:
				piece = self._current_piece
				piece.reserved = False
				self.output.append(piece)
				self._factory.pieces.append(piece)
				self._current_piece = None
				self._progress = 0
				print '{} COMPLETE PROCESSING {}'.format(self, piece)
			else:
				self._progress += self.productivity*dt
			pass
	'''
	
	def _find_suiting_pieces(self, piece_type, attrs):
		pcs = []
		for pc in self.input:
			#print '({},{})   ({},{})'.format(pc.piece_type,piece_type,pc.attributes,attrs)
			if ((pc.piece_type == piece_type) and (pc.attributes == attrs)):
				pcs.append(pc) 
		print pcs
		return pcs
		
	def add_to_stock(self, piece):
		piece.owner = self
		self.input.append(piece)

class Delivery(Machine):

	def __init__(self, factory, pos, name=''):
		super(Delivery, self).__init__(factory,
									agent_type = Agents.DELIVERY_MACHINE,
									operations='DELIVERY',
									pos=pos,
									name=name)

	def can_provide(self, required_attribs):
		return self.agent_type, self.requires, 0

	def tick(self):
		if len(self.input)>0:
			piece = self.input.pop(0)
			self._factory.pieces.remove(piece)
			self.output.append(piece)
			print 'DELIVERED {} {}'.format(piece, piece.attributes)
		pass

class BigDrill(Machine):
	def __init__(self, factory, pos, name=''):
		super(BigDrill, self).__init__(factory,
									agent_type = Agents.BIG_DRILLING_MACHINE,
									operations=Operations.DRILL_BIG,
									pos=pos,
									productivity = 0.005,
									name=name)

class FineDrill(Machine):
	def __init__(self, factory, pos, name=''):
		super(FineDrill, self).__init__(factory,
									agent_type = Agents.FINE_DRILLING_MACHINE,
									operations=Operations.DRILL_FINE,
									pos=pos,
									productivity = 0.005,
									name=name)

class Coat(Machine):
	def __init__(self, factory, pos, name=''):
		super(Coat, self).__init__(factory,
									agent_type = Agents.COATING_MACHINE,
									operations=Operations.COAT,
									pos=pos,
									productivity = 0.005,
									name=name)

class Press(Machine):
	def __init__(self, factory, pos, name=''):
		super(Press, self).__init__(factory,
									agent_type = Agents.PRESS_MACHINE,
									operations=Operations.FORCE_FIT,
									pos=pos,
									productivity = 0.005,
									name=name)

