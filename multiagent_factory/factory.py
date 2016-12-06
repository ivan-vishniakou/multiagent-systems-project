# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:49:42 2016

@author: ivan
"""
from agents import *
from base import *


class Factory(object):
    
    STOCK = 'STOCK'
    DELIVER = 'DELIVERY'
    ROLLING_MACHINE = 'ROLLING_MACHINE'
    BIG_DRILLING_MACHINE = 'BIG_DRILLING_MACHINE'
    FINE_DRILLING_MACHINE = 'FINE_DRILLING_MACHINE'
    COLORING_MACHINE = 'COLORING_MACHINE'
    ASSEMBLY_MACHINE = 'ASSEMBLY_MACHINE'
        
    def __init__(self):
        self.time = 0
        self.agents = []
        self.pieces = []
        self.tasks = []
        self.time_step = 0.1
        
        
        #create agents:
        self.size = (30,30)
        self.agents.append(Stock(self, pos=(1,1)))
        self.agents.append(Delivery(self, pos=(29,1)))
        '''
        self.agents.append(Machine(self,
                                   operation=Factory.ASSEMBLY_MACHINE, 
                                   requires = ['assembly_tray'],
                                   removes = ['fine_drilled', 'big_drilled' ,'rolled', 'colored'],
                                   adds = ['final_product'],
                                   pos = (9,9)))
        '''
        self.agents.append(Machine(self,
                                   operation=Factory.COLORING_MACHINE,
                                   requires = [],
                                   removes = [],
                                   adds = ['colored'],
                                   pos = (5,2)))
        '''
        self.agents.append(Machine(self,
                                   operation=Factory.ROLLING_MACHINE,
                                   requires = ['blank'],
                                   removes = ['blank'],
                                   adds = ['rolled'],
                                   pos = (5,4)))
        self.agents.append(Machine(self,
                                   operation=Factory.FINE_DRILLING_MACHINE,
                                   requires = ['big_drilled'],
                                   removes = [],
                                   adds = ['fine_drilled'],
                                   pos = (20,3)))
        self.agents.append(Machine(self,
                                   operation=Factory.BIG_DRILLING_MACHINE,
                                   requires = ['blank'],
                                   removes = ['blank'],
                                   adds = ['big_drilled'],
                                   pos = (20,5)))
        '''
        for _ in range(1): self.agents.append(Transporter(self, pos=[10, 10]))
        #self.agents.append(Transporter(self, pos=[10, 20]))
        #self.agents.append(Transporter(self, pos=[10, 30]))
        print 'factory sim created'
    
    
    def tick(self):
        self.time += self.time_step
        for a in self.agents:
            a.tick()
        pass    
    
    def order_product(self, recipe, issue):
        """Places tasks onto the list to manufacture a product. Relies
        on valid recipe. Recipe is a list of tuples 
        ({attributes}, [operations])."""
        new_tasks = []
        for attr, op in recipe:
            task = Task(attr, op, timestamp=self.time)
            new_tasks.append(task)
        self.tasks.extend(new_tasks)
        stock = self.find_machine_by_operation(self.STOCK)[0]
        for i in issue:
            stock.issue_piece(i)
        print 'Placed order {}'.format(new_tasks)
    
    def find_machine_by_operation(self, operation):
        """returns list of machines capable of doing a requested operation"""
        idx = []
        for i, agent in enumerate(self.agents):
            if isinstance(agent, Machine):
                if agent.does_operation(operation): idx.append(i)
        return [self.agents[_] for _ in idx]
            
    def find_piece_by_attributes(self, attributes):
        found = []
        for p in self.pieces:
            if p.matches(attributes):
                found.append(p)
        return found

        
        
if __name__ == '__main__':
    #TEST
    f= Factory()
    f.order_product([ (['blank'],[Factory.COLORING_MACHINE]),
                  (['colored'],[Factory.DELIVER])
                ], 
                  [['blank']])
    f.find_piece_by_attributes(['blank'])