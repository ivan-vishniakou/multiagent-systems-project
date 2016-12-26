# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:49:42 2016

@author: ivan, ben, eugenia
"""
from agents import *
from base import *

class Factory(object):
		
	def __init__(self):
		self.time = 0
		self.agents = set()
		self.pieces = set()
		self.machine_tasks = set()
		self.transport_tasks = set()
		self.time_step = 0.1
		
		
		#create agents:
		self.size = (30,30)

		print 'factory sim created'
		
		
		
	def add_agent(self, agent):
		self.agents.add(agent)
	
	
	def tick(self):
		self.time += self.time_step
		for a in self.agents:
			a.tick()
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
		found = []
		#print self.pieces
		for p in self.pieces:
			if p.reserved:
				continue
			if (p.attributes == attributes) and (p.piece_type == pc_type):
				if isinstance(p.owner, Machine):
					if p in p.owner.output:
						found.append(p)
		return found
	"""
	def find_task_by_operation(self, operation):
		found = []
		for p in self.tasks:
			if p.matches(operation):
				if isinstance(p.owner, Machine):
					if p in p.owner.output:
						found.append(p)
		return found
	"""
	 
	def debug_print(self):
		print '--- DEBUG ---'
		print 'tasks'
		for t in self.tasks:
			print t
			
		print '\npieces'
		for p in self.pieces:
			print '{} - {}'.format(p, p.attributes)

		
		
if __name__ == '__main__':
	#TEST
	f= Factory()
	for _ in range(1):
		f.order_product([ (['a', 'b', 'c'],[Factory.COATING_MACHINE])
				], 
				  [['a', 'b']])
	f.tick()
	#f.find_piece_by_attributes(['blank'])
