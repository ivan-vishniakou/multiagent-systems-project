#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:28:29 2016

@author: elhe
"""
import spade
import time
from base import *
from math import copysign
import random
import abc

host = "127.0.0.1"
identification = spade.AID.aid(name="agent@127.0.0.1", addresses=["xmpp://agent@m127.0.0.1"])

class Agent(spade.Agent.Agent):
    
    def __init__(self, factory, pos = [0, 0], o_type = 'AGENT'):
        super(Agent, self).__init__(o_type = o_type)
        """Base class agent constructor, position x and y required"""
        self.pos = pos
        self.progress = 0.0
        self._factory = factory
        self._busy = False

    
    
class Machine(Agent):

    def __init__(self, factory, machine_type, 
                 requires=[], removes=[], adds=[], pos=[0,0], 
                 productivity = 1.0, name='', o_type='MACHINE'):
        super(Machine, self).__init__(factory, 
                                      pos=pos,
                                      o_type=o_type)
        self.requires=requires 
        self.removes=removes
        self.adds=adds

        self.machine_type = machine_type
        self.productivity = productivity
        self._busy = False
        self._progress = 0.0
        self.output = []
        self.input = []
    
        
    def can_provide(self, required_attribs):
        operation_match = [a in self.adds for a in required_attribs]
        if any(operation_match):
            return self.machine_type, self.requires, self.production_time()
        else:
            return None
    
    def does_operation(self, operation):
        return self.machine_type == operation
            
    def production_time(self):
        return 1.0/self.productivity
    
    def execute_order(self, order):
        if self.estimate_order(order)<INFINITY:
            request = (Factory.ORDER_MOVE, self._in_type, order[2]*1.2)
            self._factory.place_order(request)
    
    def __str__(self):
        return '{} {}'.format(self.machine_type, str(self.uid).zfill(2))    
    
class Stock(Machine):
    
    def __init__(self, factory, pos=[0,0], name=''):
        super(Stock, self).__init__(factory,
                                    machine_type='STOCK',
                                    pos=pos,
                                    name=name,
                                    o_type='STOCK')
    
    def issue_new_blank(self):
        blank = Piece()
        self.output.append(blank)
        return blank.uid
        
    
class Delivery(Machine):
    
    def __init__(self, factory, pos=[0,0], name=''):
        super(Delivery, self).__init__(factory,
                                       machine_type='DELIVERY',
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
        
    def tick(self):
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
    
    def _setup(self):
    
        template = spade.Behaviour.ACLTemplate()
        #template.setSender(spade.AID.aid("a@"+host,["xmpp://a@"+host]))
        template.setOntology("ururur")
        t = spade.Behaviour.MessageTemplate(template)
        
        template1 = spade.Behaviour.ACLTemplate()
        template1.setOntology("qqq")
        t1 = spade.Behaviour.MessageTemplate(template)
        
        # Add the EventBehaviour with its template
        self.addBehaviour(self.RecvMsgBehav(),t)
        self.addBehaviour(self.RecvMsgBehav1(),t1)
        
        # Add the sender behaviour
        self.addBehaviour(self.SendMsgBehav())

#if __name__ == "__main__":
#    a = Agent("rece...@127.0.0.1", "secret")
#    a.start()