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
        self.orders = []
        self.time_step = 0.1
        
        
        #create agents:
            
        self.size = (30,30)
        self.agents.append(Stock(self, pos=(1,1)))
        self.agents.append(Delivery(self, pos=(29,1)))
        self.agents.append(Machine(self,
                                   operation=Factory.ASSEMBLY_MACHINE, 
                                   requires = ['assembly_tray'],
                                   removes = ['fine_drilled', 'big_drilled' ,'rolled', 'colored'],
                                   adds = ['final_product'],
                                   pos = (9,9)))
        self.agents.append(Machine(self,
                                   operation=Factory.COLORING_MACHINE,
                                   requires = ['rolled'],
                                   removes = [],
                                   adds = ['colored'],
                                   pos = (5,2)))
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
        
        for _ in range(7): self.agents.append(Transporter(self, pos=[10, 10]))
        #self.agents.append(Transporter(self, pos=[10, 20]))
        #self.agents.append(Transporter(self, pos=[10, 30]))
        print 'factory sim created'
    
    
    def tick(self):
        self.time += self.time_step
        for a in self.agents:
            a.tick()
        pass
    
    
    def plan_production(self, order):
        print order
        pass
    
    
    def order_product(self, recipe):
        """Uwraps the recipe into orders binded to part uid and adds 
        them to the list. For now totally relies on valid recipes."""
        print 'Placed order {}'.format(recipe)
        chain = recipe.chain[:]
        next_order = None
        oid = UObject.get_new_uid()
        while len(chain)>0:
            operations = chain.pop()
            order = Order(oid, next_order, operation=operations)
            if not next_order is None:
                next_order.prev_order = order
            self.orders.append(order)
            next_order = order
    
    
    def pick_agent_by_operation(self, operation):
        """returns list of agents capable of doing a requested operation"""
        idx = []
        for i, agent in enumerate(self.agents):
            if agent.does_operation(operation): idx.append(i)
        return [self.agents[_] for _ in idx]
    
    '''
    def place_order(self, order):
        """
        Creates a sequence of operations on a part
        """
        print 'placed order{}'.format(order)
        time = INFINITY
        operations_to_do = []
        times_for_operation = []
        for a in self.agents:
            op = a.can_provide(order)
            if op is None:
                continue
            operation, requires, production_time = a
            operations_to_do.append(operation, requires)
        print operations_to_do
       '''     
            
