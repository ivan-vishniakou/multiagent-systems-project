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
                 productivity = 0.005, name='', o_type='MACHINE'):
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

    def modify_attributes(self, attributes):
        """Modifies attributes of a piece to describe the operation.
        removes self.removes and adds self.adds to a given set
        """
        for attr in self.removes:
            if attr in attributes:
                attributes.remove(attr)
        for attr in self.adds:
            attributes.add(attr)
        return attributes

    def tick(self, dt=1):
        """Time tick for the machine: increases progress if there is an
        item in work, puts in the output when comlete and picks new
        from input."""
        if self._current_piece is None:
            if len(self.input)>0:
                self._current_piece = self.input.pop(0)
                print '{} ACCEPTED PIECE {}'.format(self,
                                                          self._current_piece)
                self._progress = 0.0
            pass
        else:
            if self._progress>1.0:
                piece = self._current_piece
                piece.attributes = self.modify_attributes(piece.attributes)
                piece.reserved = False
                self.output.append(piece)
                self._current_piece = None
                self._progress = 0
                print '{} COMPLETE PROCESSING {}'.format(self, piece)
            else:
                self._progress += self.productivity*dt
            pass
    
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
    
    def issue_piece(self, attributes):
        """Places a piece with given attributes in the stock"""
        p = Piece(self, attributes)
        self.output.append(p)
        self._factory.pieces.append(p)
        pass
    
class Delivery(Machine):
    
    def __init__(self, factory, pos=[0,0], name=''):
        super(Delivery, self).__init__(factory,
                                       operation='DELIVERY',
                                       pos=pos,
                                       name=name,
                                       o_type='DELIVERY')
    
    def can_provide(self, required_attribs):
        return self.machine_type, self.requires, 0
        
    def tick(self):
        if len(self.input)>0:
            piece = self.input.pop(0)
            self._factory.pieces.remove(piece)
            self.output.append(piece)
            print 'DELIVERED {} {}'.format(piece, piece.attributes)
        pass
    
    
class Transporter(Agent):
    
    def __init__(self, factory, pos=[0,0]):
        super(Transporter, self).__init__(factory, o_type='TRANSPORTER', pos=pos)
        self._busy = False
        self._progress = 0.0
        self._move_goal = None
        self._task = None
        self._carried_piece = None
        self._max_vel = .1

    def _pick_piece(self, piece):
        piece.owner = self
        self._carried_piece = piece
        
    def _drop_piece(self):
        piece = self._carried_piece
        piece.owner = None
        self._carried_piece = None
        return piece
        
    def _set_move_goal(self, new_goal=None):
        """Sets a goal to move to. New goal is an instance of PhysicalObject
        having a pos property. Default None stops motion.
        """
        if new_goal is None:
            self._move_goal = None
        else:
            self._move_goal = new_goal.pos
            self._prim_axis = random.choice([1,0])
        
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
        fulfillable = []
        for t in self._factory.tasks:
            suiting_pieces = self._factory.find_piece_by_attributes(t.attributes)
            if len(suiting_pieces)>0:
                fulfillable.append((t, suiting_pieces))
        if len(fulfillable)>0:
            #first task, first fitting piece
            task, suiting_pieces = random.choice(fulfillable)
            #print '---- {}:\nTASK: {}\nPIECES:{}'.format(self, task, suiting_pieces)
            piece = random.choice(suiting_pieces)
            operation = random.choice(task.operation)
            to_machine = random.choice(self._factory.find_machine_by_operation(operation))
            #print '----\nTASK: {} {} {}'.format(piece, operation, to_machine)
            if len(task.operation)>1:
                task.operation.remove(operation)
                task.attributes = list(
                        to_machine.modify_attributes(
                            set(task.attributes)
                        )
                    )
                print '----\nTASK: {}\nPIECES:{}'.format(task, suiting_pieces)
            else:
                self._factory.tasks.remove(task)
            piece.reserved = True
            return piece, to_machine
        else:
            return None
        
    def tick(self, dt=1):
        if self._task is None:
            self._task = self._select_task()
            return            
        if self._move_goal is None:
            if self._carried_piece is None:
                self._set_move_goal(new_goal=self._task[0].owner)
            else:
                self._set_move_goal(new_goal=self._task[1])
        else:
            if self._at_goal():
                if self._carried_piece is None:
                    #PICK
                    piece = self._task[0]
                    machine = piece.owner
                    self._pick_piece(
                        machine.output_piece(piece)
                                     )
                    self._set_move_goal(None)
                    print '{} PICKED {}'.format(self, self._carried_piece)
                    pass
                else:
                    #PLACE
                    piece, machine = self._task
                    machine.input_piece(self._drop_piece())
                    #self._task[1].input.append(self._carried_piece)
                    #self._carried_piece.owner = self._task[1]
                    #self._carried_piece = None
                    #self._move_goal = None
                    print '{} COMPLETED TASK {}'.format(self, self._task)
                    self._task = None
                    self._set_move_goal(None)
                pass
            else:
                self._move_to_goal()
            pass
        pass    