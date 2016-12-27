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
from operator import attrgetter
from copy import deepcopy

class Agents():
	STOCK_MACHINE = 'STOCK_MACHINE'
	DELIVERY_MACHINE = 'DELIVERY_MACHINE'
	ROLLING_MACHINE = 'ROLLING_MACHINE'
	BIG_DRILLING_MACHINE = 'BIG_DRILLING_MACHINE'
	FINE_DRILLING_MACHINE = 'FINE_DRILLING_MACHINE'
	ROLLING_MACHINE = 'ROLLING_MACHINE'
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
		#self._task = None
		self._carried_piece = None
		self._current_task = None
		self._max_vel = .1

	def _pick_piece(self, piece):
		self._current_task.piece.owner = self
		self._carried_piece = self._current_task.piece
		self._move_goal = self._current_task.dest_machine.pos

	def _drop_piece(self):
		piece = self._carried_piece
		print '\n{} finished {} '.format(self, self._current_task)
		piece.owner = None
		self._current_task.dest_machine.input_piece(piece)
		self._carried_piece = None
		self._move_goal = None
		self._current_task = None

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
			self._current_task = min(self._factory.transport_tasks, key=attrgetter('timestamp'))
			self._factory.transport_tasks.remove(self._current_task)
			self._move_goal = self._current_task.piece.owner.pos
			self._prim_axis = random.choice([1,0])

	def tick(self, dt=1):
		if self._current_task is None:
			self._select_task()
		else:
			if self._at_goal():
					if self._carried_piece is None:
						self._pick_piece(self._current_task.piece.owner.output_piece(
									self._current_task.piece))
					else:
						self._drop_piece()
			else:
				self._move_to_goal()

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
		self._worktable = []
		self.output = []
		
	def __str__(self):
		return '{}[#{}]'.format(self.agent_type, str(self.uid).zfill(3))

	def input_piece(self, piece):
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
		# TODO uncomment this block and remove it from the later portion of code
		#if len(self._tasks) < 1:
		#	self._select_task()
		if self._current_task is None:
			# TODO remove these debug print lines
			print "\nContents of input: {} \n{}".format(self, [[x.piece_type,x.attributes] for x in self.input])
			for task in self._factory.machine_tasks:
				if len(self.operations.intersection(set([op.name for op in task.operations])))>0:
					print task
			for task in self._factory.transport_tasks:
				print task
			
			if len(self._tasks)>0:
				self._start_task()
			else:
				#if len(self._tasks) < 1:
				self._select_task()
		else:
			if self._progress>1.0:
				self._perform_operation()
				self._progress = 0.0
			else:
				self._progress += self.productivity*dt
		

	def _perform_operation(self):
		print '\n{} finished {} '.format(self, self._current_task)
		operation = self._current_task.operations.pop()
		for i, piece in enumerate(self._current_task.pieces):
			self._worktable[i].attributes = self._worktable[i].attributes.union(operation.adds_attr[i])
			self._worktable[i].attributes = self._worktable[i].attributes.difference(operation.removes_attr[i])
		if len(operation.requires_pcs) > 0: # combination procedure
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
		self._current_task = None
		
	def _start_task(self):
		"""Look for pieces in input and if there, put in worktable"""
		for t, task in enumerate(self._tasks):
			for i, piece_type in enumerate(task.pieces):
				found_piece = False
				for j, piece in enumerate(self.input):
					if ((piece_type == piece.piece_type) and
							(task.req_attr[i] == piece.attributes)):
						found_piece = True
						# piece list is in order of task/recipe
						self._worktable.append(self.input.pop(j))
						break
				if found_piece == False:
					for i, piece in self._worktable:
						self.input.append(piece)
					self._worktable = []
					break
			if found_piece == True:
				self._current_task = self._tasks.pop(t)
				break

	# select the oldest task that the machine is able to do
	def _select_task(self):
		doable = []
		fulfillable = []

		for task in self._factory.machine_tasks:
			for operation in task.operations:
				if operation.name in self.operations:
					doable.append(task)
		if len(doable)>0:
			#print "{} can do {}".format(self,[x for x in doable])
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
		else:
			return
		selected_task = None
		if len(fulfillable)>0:
			#print "\n{} can complete {}".format(self,[x for x in fulfillable])
			selected_task = fulfillable[0]
			for task in fulfillable: # pick oldest task
				if (task.timestamp < selected_task.timestamp):
					selected_task = task
			for i, piece in enumerate(task.pieces):
				suiting_pieces = self._factory.find_piece_with_attr(piece,task.req_attr[i])
				if len(suiting_pieces) > 0:
					# TODO - implement piece-choosing heuristic
					selected_piece = random.choice(suiting_pieces)
					self._retrieve_piece(selected_piece)
			if len(selected_task.operations)>1: # task may contain multiple operations - select one the machine is capable of and modify task
				for op in selected_task.operations:
					if op.name in self.operations:
						operation = op
						break
				self._tasks.append(MachineTask(selected_task.pieces, deepcopy(selected_task.req_attr), set([operation])))
				# TODO - make this work for operations that are more complex than attr modification
				for i, piece in enumerate(selected_task.pieces):
					if piece in operation.accepts_pcs:
						selected_task.req_attr[i]=selected_task.req_attr[i].union(operation.adds_attr[i])
						selected_task.req_attr[i]=selected_task.req_attr[i].difference(operation.removes_attr[i])
					else:
						print '{} operation not valid for type {}'.format(operation.name,piece)
				selected_task.operations.remove(operation)
			else:
				self._tasks.append(selected_task)
				self._factory.machine_tasks.remove(selected_task)
		else:
			#print "\nCan't fulfill {} \n_tasks:{} \ndoable:{} \ninput:{}".format(self, self._tasks, doable, self.input)
			return

	def _retrieve_piece(self, piece):
		piece.reserved = True
		if piece in self.output:
			print "\nOutput to input {}:{}".format(self, [piece.piece_type, piece.attributes] )
			self.output.remove(piece)
			self.input_piece(piece)
		else:
			t_task = TransportTask(piece, self, self._factory.time)
			self._factory.transport_tasks.add(t_task)
			print '\n{} added'.format(t_task)

	def _find_suiting_pieces(self, piece_type, attrs):
		p = self._find_pieces_in_output(piece_type, attrs)
		if p is None:
			return self._factory.find_piece_with_attr(piece_type,attrs)
		else:
			return [p]

	def _find_pieces_in_output(self, piece_type, attrs):
		for piece in self.output:
			if piece.piece_type == piece_type and  \
			attrs == piece.attributes and \
			piece.reserved == False:
				return piece
		return None

	def does_operation(self, operation):
		return self.operation == operation

	def production_time(self):
		return 1.0/self.productivity

class StockMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(StockMachine, self).__init__(factory,
									agent_type = Agents.STOCK_MACHINE,
									operations = set([Operations.PROCURE]),
									pos=pos,
									productivity = 0.05,
									name=name)
	
	def _find_suiting_pieces(self, piece_type, attrs):
		pcs = []
		for pc in self.input:
			if ((pc.piece_type == piece_type) and (pc.attributes == attrs)):
				pcs.append(pc)
		return pcs
	
	def _retrieve_piece(self, piece):
		pass
		
	def add_to_stock(self, piece):
		piece.owner = self
		if Attributes.NONCONSUMABLE in piece.attributes:
			self.output.append(piece)
			piece.reserved = False
		else:
			self.input.append(piece)
		self._factory.pieces.add(piece)

class DeliveryMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(DeliveryMachine, self).__init__(factory,
									agent_type = Agents.DELIVERY_MACHINE,
									operations=set([Operations.DELIVER]),
									pos=pos,
									productivity = 0.005,
									name=name)

class BigDrillMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(BigDrillMachine, self).__init__(factory,
									agent_type = Agents.BIG_DRILLING_MACHINE,
									operations=set([Operations.DRILL_BIG]),
									pos=pos,
									productivity = 0.005,
									name=name)

class FineDrillMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(FineDrillMachine, self).__init__(factory,
									agent_type = Agents.FINE_DRILLING_MACHINE,
									operations=set([Operations.DRILL_FINE]),
									pos=pos,
									productivity = 0.005,
									name=name)

class RollerMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(RollerMachine, self).__init__(factory,
									agent_type = Agents.ROLLING_MACHINE,
									operations=set([Operations.ROLL]),
									pos=pos,
									productivity = 0.005,
									name=name)

class CoatMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(CoatMachine, self).__init__(factory,
									agent_type = Agents.COATING_MACHINE,
									operations=set([Operations.COAT]),
									pos=pos,
									productivity = 0.005,
									name=name)

class ForceFitMachine(Machine):
	def __init__(self, factory, pos, name=''):
		super(ForceFitMachine, self).__init__(factory,
									agent_type = Agents.PRESS_MACHINE,
									operations=set([Operations.FORCE_FIT]),
									pos=pos,
									productivity = 0.005,
									name=name)

