# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:56:02 2016

@author: ivan, ben, eugenia
"""

from base import *
from actions import *

"""
Order creation rules
	- Only combination operations should have more than one item per task
	- If 2 parts of the same type are needed and one requires more attributes it should be listed first
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
		MachineTask([Pieces.BLOCK], [set()], set([Procure()])),
		MachineTask([Pieces.BLOCK], [set()], set([DrillBig(),DrillFine()])),
		MachineTask([Pieces.BLOCK], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED])], set([Deliver()]))
		]

class COATED_BEARING_BLOCK(Order):
	name = Orders.COATED_BEARING_BLOCK
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Procure()])),
		MachineTask([Pieces.BLOCK], [set()], set([DrillBig(),DrillFine()])),
		MachineTask([Pieces.BLOCK], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED, Attributes.COATED])], set([Deliver()]))
		]

class BEARING_BLOCK_ASSY(Order):
	name = Orders.BEARING_BLOCK_ASSY
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Procure()])),
		MachineTask([Pieces.BLOCK], [set()], set([DrillBig(), DrillFine()])),
		MachineTask([Pieces.BEARING], [set()], set([Procure()])),
		MachineTask([Pieces.BEARING], [set()], set([Roll()])),
		MachineTask([Pieces.ASSY_TRAY], [set()], set([Procure()])),
		MachineTask([Pieces.BLOCK, Pieces.BEARING,Pieces.ASSY_TRAY], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED]), set([Attributes.ROLLED]),set()], set([ForceFit()])),
		MachineTask([Pieces.BEARING_BLOCK_ASSY], [set([Attributes.FINE_DRILLED, Attributes.ROLLED])], set([Deliver()]))
		]

class COATED_BEARING_BLOCK_ASSY():
	name = Orders.COATED_BEARING_BLOCK_ASSY
	task_list = [
		MachineTask([Pieces.BLOCK], [set()], set([Procure()])),
		MachineTask([Pieces.BLOCK], [set()], set([DrillBig(), DrillFine()])),
		MachineTask([Pieces.BLOCK], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED])], set([Coat()])),
		MachineTask([Pieces.BEARING], [set()], set([Procure()])),
		MachineTask([Pieces.BEARING], [set()], set([Roll()])),
		MachineTask([Pieces.ASSY_TRAY], [set()], set([Procure()])),
		MachineTask([Pieces.BLOCK, Pieces.BEARING,Pieces.ASSY_TRAY], [set([Attributes.BIG_DRILLED, Attributes.FINE_DRILLED]), set([Attributes.ROLLED]),set()], set([ForceFit()])),
		MachineTask([Pieces.BEARING_BLOCK_ASSY], [set([Attributes.FINE_DRILLED, Attributes.ROLLED])], set([Deliver()]))
		]
