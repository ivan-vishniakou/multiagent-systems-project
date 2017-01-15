# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:49:42 2016

@author: ivan, ben, eugenia
"""
from agents import *
from base import *
from activity_visualizer import ActivityVisualizer

class Factory(object):

	def __init__(self):
		self.activity_visualizer = ActivityVisualizer(self)
		self.time = 0
		self.agents = set()
		self.pieces = set()
		self.machine_tasks = set()
		self.transport_tasks = set()
		self.time_step = 0.1
		self.size = (30,30)
		self.saved = False
		self.started = False

	def add_agent(self, agent):
		self.agents.add(agent)

	def tick(self):
		self.time += self.time_step
		for a in self.agents:
			a.tick()
			a.visualize_activity()
		if (len(self.transport_tasks) == 0
		and len(self.machine_tasks) == 0):
			if (self.saved is False and self.started == True):
				self.saved = True
				self.activity_visualizer.save()
		else:
			self.started = True
		pass

	def order_product(self, order):
		"""Places tasks onto machine_task list to manufacture a product"""
		for task in order.task_list:
			self.machine_tasks.add(task)
			print '{} added'.format(task)

	def find_machine_by_operation(self, operation):
		"""returns list of machines capable of doing a requested operation"""
		idx = []
		for i, agent in enumerate(self.agents):
			if isinstance(agent, Machine):
				if agent.does_operation(operation): idx.append(i)
		return [self.agents[_] for _ in idx]

	def find_piece_with_attr(self, pc_type, attributes):
		"""returns list of pieces with the given attributes"""
		found = []
		for p in self.pieces:
			if p.reserved:
				continue
			if (p.piece_type == pc_type) and (p.attributes == attributes):
				if isinstance(p.owner, Machine):
					if p in p.owner.output:
						found.append(p)
		return found

	def debug_print(self):
		print '--- DEBUG ---'
		print 'tasks'
		for t in self.tasks:
			print t

		print '\npieces'
		for p in self.pieces:
			print '{} - {}'.format(p, p.attributes)

