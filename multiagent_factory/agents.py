# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:55:08 2016

@author: ivan
"""
from base import *
from math import copysign
import random
import abc
    
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

    
class Machine(Agent):
    """Stationary machine performing operations the fields have
    prerequisite attiributes (requires), and added/removed attributes
    in removes/adds respectively.
    """
    def __init__(self, factory, operation,
                 requires=[], removes=[], adds=[], pos=[0,0],
                 productivity = 1.0, name='', o_type='MACHINE'):
        super(Machine, self).__init__(factory,
                                      pos=pos,
                                      o_type=o_type)
        self.requires=set(requires)
        self.removes=set(removes)
        self.adds=adds
        self.operation = operation
        self.productivity = productivity
        self._busy = False
        self._progress = 0.0
        self._current_piece = None
        self.output = []
        self.input = []
    
    def tick(self, dt=1):
        """Time tick for the machine: increases progress if there is an
        item in work, puts in the output when comlete and picks new
        from input."""
        if self._current_piece is None:
            if len(self.input)>0:
                self._current_piece = self.input.pop(0)
                self._progress = 0.0
            return
        else:
            if self._progress>1.0:
                self.output.append(self._current_piece)
                self._current_piece = None
            else:
                self.progress += self.productivity*dt
    
    '''
    def can_provide(self, required_attribs):
        operation_match = [a in self.adds for a in required_attribs]
        if any(operation_match):
            return self.machine_type, self.requires, self.production_time()
        else:
            return None
    '''
    
    def does_operation(self, operation):
        return self.operation == operation
            
    def production_time(self):
        return 1.0/self.productivity
        
    def __str__(self):
        return '{} {}'.format(self.operation, str(self.uid).zfill(2))    
    
        
class Stock(Machine):
    
    def __init__(self, factory, pos=[0,0], name=''):
        super(Stock, self).__init__(factory,
                                    operation='STOCK',
                                    pos=pos,
                                    name=name,
                                    o_type='STOCK')
    '''
    def issue_new_blank(self):
        blank = Piece()
        self.output.append(blank)
        return blank.uid
    ''' 
    
class Delivery(Machine):
    
    def __init__(self, factory, pos=[0,0], name=''):
        super(Delivery, self).__init__(factory,
                                       operation='DELIVERY',
                                       pos=pos,
                                       name=name,
                                       o_type='DELIVERY')
    
    def can_provide(self, required_attribs):
        return self.machine_type, self.requires, 0
    
    
class Transporter(Agent):
    
    def __init__(self, factory, pos=[0,0]):
        super(Transporter, self).__init__(factory, o_type='TRANSPORTER', pos=pos)
        self._busy = False
        self._progress = 0.0
        self._goal = None
        self._max_vel = .1
        
    def _move_to_goal():
        pass
        
    def tick(self, dt=1):
        if self._goal is None:
            self._goal = random.choice(self._factory.agents)
            self._prim_axis = random.choice([1,0])
            print 'goat a goal', self._goal
        else:
            for ax in [self._prim_axis, not self._prim_axis]:
                if (abs(self._goal.pos[ax]-self.pos[ax])>self._max_vel):
                    self.pos[ax] += copysign(self._max_vel, self._goal.pos[ax]-self.pos[ax])
                    return
                elif (abs(self._goal.pos[ax]-self.pos[ax])>self._max_vel*0.1):
                    self.pos[ax] = self._goal.pos[ax]
                    return

            #arrived to goal
            self._goal = None
        #self.pos = self.pos[0]+random.random()*0.1-0.05, self.pos[1]+random.random()*0.1-0.05
    
    