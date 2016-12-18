# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan, ben, eugenia
"""

class Operations():
	"""Class listing the available operations"""
	@staticmethod
	PROCURE = 'PROCURE'
	DELIVER = 'DELIVER'
	ROLL = 'ROLL'
	DRILL_BIG = 'DRILL_BIG'
	DRILL_FINE = 'DRILL_FINE'
	COAT = 'COAT'
	FORCE_FIT = 'FORCE_FIT'
	

class Attributes():
	"""Class listing the available attributes"""
	@staticmethod
	 ROLLED = 'rolled'
	 BIG_DRILLED = 'big_drilled'
	 FINE_DRILLED = 'fine_drilled'
	 COATED = 'coated'
	
class Operation():
	def __init__(self, name, adds_attr, removes_attr, requires_attr, adds_pcs, removes_pcs, requires_pcs, accepts_pcs):
		self.name = name 					# Name of operation
		
        self.adds_attr = adds_attr 			# list of set of attributes added to pcs
        self.removes_attr = removes_attr 	# list of set of attributes removed from pcs
        self.requires_attr = requires_attr	# list of set of attributes required for operation
        
        self.adds_pcs = adds_pcs			# list of pcs added to pcs
        self.removes_pcs = removes_pcs 		# list of pcs removed from pcs
        self.requires_pcs = requires_pcs	# list of pcs required for operation - if defined, accepts_pcs is ignored
        
        self.accepts_pcs = accepts_pcs		# set of accepted components
        
        
    # TODO - fix this print function when arguments are finalized
    def __str__(self):
        return 'Operation {}: removes {}, adds {}, requires {}, combines \
				{}, creates {}, and can be performed on {}'.format(self.name, self.removes,
				self.adds, self.requires, self.piece_types)
		
class Procure(Operation):
	@staticmethod
	def __init__(self):
		super(Procure, self).__init__(Operation.PROCURE, 
		[set()], [set()], [set()], 
		[], [], [], 
		[Pieces.BLOCK, Pieces.BEARING, Pieces.ASSY_TRAY]):
		
class Deliver(Operation):
	@staticmethod
	def __init__(self):
		super(Deliver, self).__init__(Operation.DELIVER, 
		[set()], [set()], [set()], 
		[], [], [], 
		[Pieces.BLOCK, Pieces.BEARING, Pieces.ASSY]):
		
class Roll(Operation):
	@staticmethod
	def __init__(self):
		super(Roll, self).__init__(Operation.ROLL, 
		[[Attributes.ROLLED]], [set()], [set()],
		[], [], [], 
		[Pieces.BEARING]):
		
class DRILL_BIG(Operation):
	@staticmethod
	def __init__(self):
		super(DRILL_BIG, self).__init__(Operation.DRILL_BIG, 
		[set(Attributes.BIG_DRILLED)], [set()], [set()], 
		[], [], [], 
		[Pieces.BLOCK]):
		
class DRILL_FINE(Operation):
	@staticmethod
	def __init__(self):
		super(DRILL_FINE, self).__init__(Operation.DRILL_FINE, 
		[set(Attributes.FINE_DRILLED)], [set()], [set()], 
		[], [], [], 
		[Pieces.BLOCK]):
		
class COAT(Operation):
	@staticmethod
	def __init__(self):
		super(COAT, self).__init__(Operation.COAT, 
		[set(Attributes.COATED)], [set()], [set()], 
		[], [], [], 
		[Pieces.BLOCK]):
		
class FORCE_FIT(Operation):
	@staticmethod
	def __init__(self):
		super(FORCE_FIT, self).__init__(Operation.FORCE_FIT, 
		[set(),set(),set()], [set(),set(),set()], [set(Attributes.BIG_DRILLED),set(),set()], 
		[Pieces.BEARING_BLOCK_ASSY], [Pieces.BLOCK, Pieces.BEARING], [Pieces.BLOCK, Pieces.BEARING, Pieces.ASSY_TRAY], 
		[]):

class Pieces():
	@staticmethod
	BLOCK = 'block'
	BEARING = 'bearing'
	ASSY_TRAY = 'assy_tray'
	BEARING_BLOCK_ASSY = 'bearing_block_assy'

class Piece(PhysicalObject):
    
    def __init__(self, owner, piece_type, attributes = []):
        super(Piece, self).__init__(o_type = 'PIECE',
                                    pos = owner.pos,
                                    attributes = attributes)
        self.piece_type = piece_type
        self.owner = owner
        self.reserved = False
        
    def __str__(self):
        return '{} {}: {}'.format(self.o_type, 
                                  str(self.uid).zfill(2),
                                  str(list(self.attributes))
                                  )

         
class AssemblyTray(Piece):
    """Class representing a non-consumable assembly tool in the factory"""
    
    def __init__(self, owner):
        super(AssemblyTray, self).__init__(o_type = 'TRAY',
                                    owner = owner,
                                    attributes = ['assembly_tray', 'empty'])
                             

						
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
        '''attributes shouldn't be duplicated in the first place'''
        #self.attributes = set(attributes)
        self.attributes = attributes
        self.pos = pos
        
    def matches(self, required):
        """Checks if instances' set has all the attributes of the required."""
        provided = self.attributes
        for attr in required:
            if not attr in provided:
                return False
        for attr in provided:
            if not attr in required:
                return False
        return True

class Recipes():
	@staticmethod
	"""
	Methodology:
	Recipes should facilitate maximum parallelism
	"""
	BEARING_BLOCK = [
						MachineTask([pieces.BLOCK], [set()], set(Operations.PROCURE)),
						MachineTask([pieces.BLOCK], [set()], set(Operations.DRILL_BIG,Operations.DRILL_FINE)),
						MachineTask([pieces.BLOCK], [set(Attributes.BIG_DRILLED, Attributes.FINE_DRILLED)], set(operation.DELIVER))]
						
	COATED_BEARING_BLOCK = [
						MachineTask([pieces.BLOCK], [set()], set(Operations.PROCURE)),
						MachineTask([pieces.BLOCK], [set()], set(Operations.DRILL_BIG,Operations.DRILL_FINE)),
						MachineTask([pieces.BLOCK], [set(Attributes.BIG_DRILLED, Attributes.FINE_DRILLED, Attributes.COATED)], set(operation.DELIVER))]
						
	BEARING_BLOCK_ASSY = [
						MachineTask([pieces.BLOCK], [set()], set(Operations.PROCURE)),
						MachineTask([pieces.BLOCK], [set()], set(Operations.DRILL_BIG, Operations.DRILL_FINE)),
						
						MachineTask([pieces.BEARING], [set()], set(Operations.PROCURE)),
						MachineTask([pieces.BEARING], [set()], set(operation.ROLL)),
						
						MachineTask([pieces.ASSY_TRAY], [set()], set(Operations.PROCURE)),
						
						MachineTask([pieces.BLOCK, pieces.BEARING,pieces.ASSY_TRAY], [set(Attributes.BIG_DRILLED, Attributes.FINE_DRILLED), set(Attributes.ROLLED),set()], set(Operations.FORCE_FIT)),
						MachineTask([pieces.BEARING_BLOCK_ASSY], [set(Attributes.FINE_DRILLED, Attributes.ROLLED)], set(operation.DELIVER))]
												
	COATED_BEARING_BLOCK_ASSY = [
						MachineTask([pieces.BLOCK], [set()], set(Operations.PROCURE)),
						MachineTask([pieces.BLOCK], [set()], set(Operations.DRILL_BIG, Operations.DRILL_FINE)),
						MachineTask([pieces.BLOCK], [set(Attributes.BIG_DRILLED, Attributes.FINE_DRILLED)], set(Operations.COAT)),
						
						MachineTask([pieces.BEARING], [set()], set(Operations.PROCURE)),
						MachineTask([pieces.BEARING], [set()], set(operation.ROLL)),
						
						MachineTask([pieces.ASSY_TRAY], [set()], set(Operations.PROCURE)),
						
						MachineTask([pieces.BLOCK, pieces.BEARING,pieces.ASSY_TRAY], [set(Attributes.BIG_DRILLED, Attributes.FINE_DRILLED), set(Attributes.ROLLED),set()], set(Operations.FORCE_FIT)),
						MachineTask([pieces.BEARING_BLOCK_ASSY], [set(Attributes.FINE_DRILLED, Attributes.ROLLED)], set(operation.DELIVER))]
						
class MachineTask(UObject):
    """Class representing a task performed by a mobile robot.
    Contains attributes of a part and operation type to perform
    on a matching part."""
    
    def __init__(self, pieces, req_attr, operations, timestamp=0.0):
        super(Task, self).__init__(o_type='TASK')
        self.timestamp = timestamp
        self.pieces = pieces
        self.req_attr = req_attr
        self.operations = operations
    
    def __str__(self):
        return 'Task {}: {} on {} to {}'.format(self.uid,
                                          self.attributes,
                                          self.piece_type,
                                          self.operation)
        
    def __repr__(self):
        return self.__str__()
        
class TransportTask(UObject):
	    def __init__(self, piece, machine, timestamp):
        super(Task, self).__init__(o_type='TASK')
        self.timestamp = timestamp
        self.piece = piece
        self.dest_machine = dest_machine
    
    def __str__(self):
        return 'Task {}: {} on {} to {}'.format(self.uid,
                                          self.attributes,
                                          self.piece_type,
                                          self.operation)
    
    def __repr__(self):
        return self.__str__()
