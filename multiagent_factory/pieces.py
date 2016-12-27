# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan, ben, eugenia
"""

from base import *

class Pieces():
	"""Class listing the available piece types"""
	BLOCK = 'block'
	BEARING = 'bearing'
	ASSY_TRAY = 'assy_tray'
	BEARING_BLOCK_ASSY = 'bearing_block_assy'
    
class Attributes():
	"""Class listing the available attributes"""
	ROLLED = 'rolled'
	BIG_DRILLED = 'big_drilled'
	FINE_DRILLED = 'fine_drilled'
	COATED = 'coated'
	NONCONSUMABLE = 'nonconsumable'
    
class Piece(PhysicalObject):

	def __init__(self, owner, piece_type, attributes = set()):
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
		super(AssemblyTray, self).__init__(owner = owner,
									piece_type = Pieces.ASSY_TRAY,
									attributes = set([Attributes.NONCONSUMABLE]))

class Block(Piece):
	"""Class representing a non-consumable assembly tool in the factory"""
	def __init__(self, owner):
		super(Block, self).__init__(owner = owner,
									piece_type = Pieces.BLOCK,
									attributes = set())

class Bearing(Piece):
	"""Class representing a non-consumable assembly tool in the factory"""
	def __init__(self, owner):
		super(Bearing, self).__init__(owner = owner,
									piece_type = Pieces.BEARING,
									attributes = set())

class BearingBlockAssy(Piece):
	"""Class representing a non-consumable assembly tool in the factory"""
	def __init__(self, owner):
		super(BearingBlockAssy, self).__init__(owner = owner,
									piece_type = Pieces.BEARING_BLOCK_ASSY,
									attributes = set())
