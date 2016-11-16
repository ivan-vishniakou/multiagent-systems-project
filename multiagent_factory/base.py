# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan
"""

INFINITY = float('inf')

class UObject(object):
    
    PROP_ANY = 'ANY'
    uid = 0
    
    @staticmethod
    def matches(provided, required):
        """Checks if the dictionary of object properties match the required """
        for key in required.keys():
            if required[key] != UObject.PROP_ANY:
                if provided.has_key(key):
                    if provided[key] != required[key]:
                        return False
                else:
                    return False
        return True
    
    @staticmethod
    def get_new_uid():
        UObject.uid += 1
        return UObject.uid - 1
        
    def __init__(self, o_type = 'UOBJECT'):
        self.uid = UObject.uid
        self.o_type = o_type
        UObject.uid += 1
    
    def __str__(self):
        return '{} {}'.format(self.o_type, str(self.uid).zfill(2))    


class Piece(UObject):
    
    BLANK = 'BLANK'
    
    def __init__(self):
        super(Piece, self).__init__(o_type = 'PIECE')
        self.properties = {'pos':(0,0)}


class ProductRecipe(object):
    
    def __init__(self, *args):
        self.chain = list(args)

    def __str__(self):
        return ','.join([str(_) for _ in self.chain])
        
    def __repr__(self):
        return self.__str__()


class Order(object):
    
    def __init__(self, item_id, 
                 next_order=None, prev_order=None, 
                 operation = 'NONE', timestamp = 0.0):
        self.item_id = item_id
        self.next_order = next_order
        self.prev_order = prev_order
        self.timestamp = timestamp
        self.operation = operation
        self.priority = 1.0
    
    def __str__(self):
        return 'Order PID {} to {}'.format(self.item_id, self.operation)
        
    def __repr__(self):
        return self.__str__()