# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan
"""

INFINITY = float('inf')

class UObject(object):
    """Base class for objects in the simulation providing unique ids."""
    
    uid = 0 #Static counter of objects

    @staticmethod
    def get_new_uid():
        UObject.uid += 1
        return UObject.uid - 1
        
    def __init__(self, o_type = 'UOBJECT'):
        self.uid = UObject.get_new_uid()
        self.o_type = o_type
    
    def __str__(self):
        return '{} {}'.format(self.o_type, str(self.uid).zfill(2))
        
    def __repr__(self):
        return self.__str__()


class PhysicalObject(UObject):
    """Adds position and attributes to UObject to describe physical
    objects, like work pieces and agents.
    """
    
    def __init__(self, o_type = 'PHYS_OBJECT', pos = [0,0], attributes = []):
        super(PhysicalObject, self).__init__(o_type = o_type)
        self.attributes = set(attributes)
        self.pos = pos
        
    def matches(self, required):
        """Checks if instances' set has all the attributes of the required."""
        provided = self.attributes
        for attr in provided:
            if not attr in required:
                return False
        return True


class Piece(PhysicalObject):
    """Class representing a work piece in the factory"""
    
    def __init__(self, owner, attributes = []):
        super(Piece, self).__init__(o_type = 'PIECE',
                                    pos = owner.pos,
                                    attributes = attributes)


class Task(UObject):
    """Class representing a task performed by a mobile robot.
    Contains attributes of a part and operation type to perform
    on a matching part."""
    
    def __init__(self, attributes, operation, timestamp = 0.0):
        super(Task, self).__init__(o_type='TASK')
        self.timestamp = timestamp
        self.attributes = attributes
        self.operation = operation
    
    def __str__(self):
        return 'Task {}: {} to {}'.format(self.uid,
                                          self.attributes,
                                          self.operation)
        
    def __repr__(self):
        return self.__str__()