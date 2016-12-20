# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:55:08 2016

@author: ivan, ben, eugenia
"""
# TODO - add base type to recipe
# TODO - add issue to recipe
# TODO - let stock look for issue in task list
# TODO - add machine types to agents.py so factory can be dynamically initialized
# TODO - Ivan doesn't like select task due to random nature and untyped tuples
# TODO - replace machines with actions in tasks so that machines in the end could do/choose multiple operations, say if a machine could drill large or small holes.
# TODO - add hooks for performance visualizer
# TODO - add recipe/operation checker 
# TODO - Mod stock and delivery to be defined just like other machines
# TODO - clean up __str__ functions. Most are outdated
# TODO - remove mass commeting

from factory_visualizer import FactoryVisualizer
from activity_visualizer import ActivityVisualizer
from multiagent_factory.factory import *
from multiagent_factory.orders import *
from multiagent_factory import *
from multiagent_factory import *
 
def main():
	f = Factory()
	
	s = Stock(f, pos=(1,5))
	f.add_agent(s)
	f.add_agent(BigDrill(f, pos=(5,10)))
	f.add_agent(FineDrill(f, pos=(15,10)))
	f.add_agent(Coat(f, pos=(5,20)))
	f.add_agent(Press(f, pos=(15,20)))
	f.add_agent(Delivery(f, pos=(20,5)))
	
	for i in range(3):
		f.add_agent(Transporter(f,pos=(10, 2 * (i+2))))
	
	for _ in range(5):
		s.add_to_stock(Block(s))
	
	for _ in range(3):
		f.order_product(BEARING_BLOCK())
	
	fv = FactoryVisualizer(f)

	fv.run()

if __name__ == "__main__":
	main()
