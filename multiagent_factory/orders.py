# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan, ben, eugenia
"""

from base import *
from actions import *

"""
Order creation methodology
	- Recipes should facilitate maximum parallelism
	- If 2 parts of the same type are needed and one requires more attributes it should be listed first
	- Recipes containing more than one part should be used for combination operations only
	- Combination operations need to list the parts in the same order as they are listed in the requires_pcs element of the operation definition
"""


class Orders():
	BEARING_BLOCK = 'BEARING_BLOCK'
	COATED_BEARING_BLOCK = 'COATED_BEARING_BLOCK'
	BEARING_BLOCK_ASSY = 'BEARING_BLOCK_ASSY'
	COATED_BEARING_BLOCK_ASSY = 'COATED_BEARING_BLOCK_ASSY'
	

class Order():
	name =  ''
	task_list = []
	
	def __str__(self):
		return '{}'.format(name)


class BEARING_BLOCK(Order):
	name = Orders.BEARING_BLOCK
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Operations.PROCURE])),
		MachineTask([Pieces.BLOCK], [set()], set([Operations.DRILL_BIG,Operations.DRILL_FINE])),
		MachineTask([Pieces.BLOCK], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED])], set(Operations.DELIVER))
		]

class COATED_BEARING_BLOCK(Order):
	name = Orders.COATED_BEARING_BLOCK
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Operations.PROCURE])),
		MachineTask([Pieces.BLOCK], [set()], set([Operations.DRILL_BIG,Operations.DRILL_FINE])),
		MachineTask([Pieces.BLOCK], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED, Attributes.COATED])], set(Operations.DELIVER))
		]

class BEARING_BLOCK_ASSY(Order):
	name = Orders.BEARING_BLOCK_ASSY
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Operations.PROCURE])),
		MachineTask([Pieces.BLOCK], [set()], set([Operations.DRILL_BIG, Operations.DRILL_FINE])),
		MachineTask([Pieces.BEARING], [set()], set([Operations.PROCURE])),
		MachineTask([Pieces.BEARING], [set()], set([Operations.ROLL])),
		MachineTask([Pieces.ASSY_TRAY], [set()], set([Operations.PROCURE])),
		MachineTask([Pieces.BLOCK, Pieces.BEARING,Pieces.ASSY_TRAY], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED]), set(Attributes.ROLLED),set()], set(Operations.FORCE_FIT)),
		MachineTask([Pieces.BEARING_BLOCK_ASSY], [set([Attributes.FINE_DRILLED, Attributes.ROLLED])], set(Operations.DELIVER))
		]

class COATED_BEARING_BLOCK_ASSY():
	name = Orders.COATED_BEARING_BLOCK_ASSY
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Operations.PROCURE])),
		MachineTask([Pieces.BLOCK], [set()], set([Operations.DRILL_BIG, Operations.DRILL_FINE])),
		MachineTask([Pieces.BLOCK], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED])], set(Operations.COAT)),
		MachineTask([Pieces.BEARING], [set()], set(Operations.PROCURE)),
		MachineTask([Pieces.BEARING], [set()], set(Operations.ROLL)),
		MachineTask([Pieces.ASSY_TRAY], [set()], set(Operations.PROCURE)),
		MachineTask([Pieces.BLOCK, Pieces.BEARING,Pieces.ASSY_TRAY], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED]), set(Attributes.ROLLED),set()], set(Operations.FORCE_FIT)),
		MachineTask([Pieces.BEARING_BLOCK_ASSY], [set([Attributes.FINE_DRILLED, Attributes.ROLLED])], set(Operations.DELIVER))
		]
