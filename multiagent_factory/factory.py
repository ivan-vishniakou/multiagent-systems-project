# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:49:42 2016

@author: ivan, ben, eugenia
"""
from agents import *
from base import *
import recipes


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
        self.agents.append(Stock(self, [recipes.BLOCK,
										recipes.BLOCK,
										recipes.BLOCK,
										recipes.BLOCK,
										recipes.BLOCK
										], pos=(5,5)))
        self.agents.append(Delivery(self, pos=(20,5)))
        '''
        self.agents.append(Machine(self,
                                   operation=Factory.ASSEMBLY_MACHINE, 
                                   requires = ['assembly_tray'],
                                   removes = ['fine_drilled', 'big_drilled' ,'rolled', 'colored'],
                                   adds = ['final_product'],
                                   pos = (9,9)))
        '''
        self.agents.append(Machine(self,
                                   operation=COATING_MACHINE,
                                   requires = [],
                                   removes = [],
                                   adds = ['coated'],
                                   pos = (10,20)))
        self.agents.append(Machine(self,
                                   operation=FINE_DRILLING_MACHINE,
                                   requires = [],
                                   removes = [],
                                   adds = ['fine_drilled'],
                                   pos = (8,10)))
        self.agents.append(Machine(self,
                                   operation=BIG_DRILLING_MACHINE,
                                   requires = [],
                                   removes = [],
                                   adds = ['big_drilled'],
                                   pos = (12,11)))
        
        for _ in range(5): self.agents.append(Transporter(self, pos=[10, 10]))
        #self.agents.append(Transporter(self, pos=[10, 20]))
        #self.agents.append(Transporter(self, pos=[10, 30]))
        print 'factory sim created'
    
    def tick(self):
        self.time += self.time_step
        for a in self.agents:
            a.tick()
        pass    
    
    def order_product(self, recipe, issue):
        """Places tasks onto machine_task list to manufacture a product"""
        new_tasks = []
        for issue_type, attr, op in recipe:
            task = Task(issue_type, attr, op, timestamp=self.time)
            new_tasks.append(task)
            print '{}: {}, {}'.format(issue_type, attr, op)

        self.tasks.extend(new_tasks)
        
        '''
        The issuing should be viewed as a normal task that is added to the task list
        and completed by stock
        '''
        #stock = self.find_machine_by_operation(self.STOCK)[0]
        #for i in issue:
        #    stock.issue_piece(i)
        #print 'Placed order {}'.format(new_tasks)
        #print self.tasks
  
    
    def find_machine_by_operation(self, operation):
        """returns list of machines capable of doing a requested operation"""
        idx = []
        for i, agent in enumerate(self.agents):
            if isinstance(agent, Machine):
                if agent.does_operation(operation): idx.append(i)
        return [self.agents[_] for _ in idx]
            
    def find_piece_with_attr(self, pc_type, attributes):
        found = []
        for p in self.pieces:
            if p.reserved:
                continue
            if p.matches(attributes):
                if isinstance(p.owner, Machine):
                    if p in p.owner.output:
                        found.append(p)
        return found
        
    def find_task_by_operation(self, operation):
        found = []
        for p in self.tasks:
            if p.reserved:
                continue
            if p.matches(operation):
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

        
        
if __name__ == '__main__':
    #TEST
    f= Factory()
    for _ in range(1):
        f.order_product([ (['a', 'b', 'c'],[Factory.COATING_MACHINE])
                ], 
                  [['a', 'b']])
    f.tick()
    #f.find_piece_by_attributes(['blank'])
