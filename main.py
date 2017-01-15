# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:55:08 2016

@author: ivan, ben, eugenia
"""

# TODO make performance visualizer show full text
# TODO add recipe/operation checker 
# TODO add functionality for dealing with out-of-stock situations (?)

from factory_visualizer import FactoryVisualizer
from multiagent_factory.activity_visualizer import ActivityVisualizer
from multiagent_factory.factory import *
from multiagent_factory.orders import *
from multiagent_factory.pieces import *

 
def main():
	f = Factory()
	
	s = StockMachine(f, pos=[1,5])
	f.add_agent(s)
	f.add_agent(BigDrillMachine(f, pos=[3,10]))
	f.add_agent(FineDrillMachine(f, pos=[17,10]))
	f.add_agent(GreaseMachine(f, pos=[10,15]))
	f.add_agent(CoatMachine(f, pos=[3,20]))
	f.add_agent(ForceFitMachine(f, pos=[17,20]))
	f.add_agent(DeliveryMachine(f, pos=[20,5]))

	for i in range(3):
		f.add_agent(Transporter(f,pos=[10, 2 * (i+2)]))

	s.add_to_stock(AssemblyTray(s))
	for _ in range(9):
		s.add_to_stock(Block(s))
	for _ in range(5):
		s.add_to_stock(Bearing(s))

	for _ in range(2):
		f.order_product(BEARING_BLOCK(f.time))
		f.order_product(COATED_BEARING_BLOCK(f.time))
		f.order_product(BEARING_BLOCK_ASSY(f.time))
		f.order_product(COATED_BEARING_BLOCK_ASSY(f.time))
	
	fv = FactoryVisualizer(f)

	fv.run()

if __name__ == "__main__":
	main()
