# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:55:08 2016

@author: ivan, ben, eugenia
"""
# TODO - add hooks for performance visualizer	
# TODO - add recipe/operation checker 
# TODO - clean up __str__ functions. Most are outdated
# TODO - remove mass commenting
# TODO - add functionality for dealing with out-of-stock situations ?

from factory_visualizer import FactoryVisualizer
from activity_visualizer import ActivityVisualizer
from multiagent_factory.factory import *
from multiagent_factory.orders import *
from multiagent_factory import *
from multiagent_factory import *
 
def main():
	f = Factory()
	
	s = StockMachine(f, pos=[1,5])
	f.add_agent(s)
	f.add_agent(BigDrillMachine(f, pos=[5,10]))
	f.add_agent(FineDrillMachine(f, pos=[15,10]))
	f.add_agent(CoatMachine(f, pos=[5,20]))
	f.add_agent(ForceFitMachine(f, pos=[15,20]))
	f.add_agent(DeliveryMachine(f, pos=[20,5]))
	
	for i in range(3):
		f.add_agent(Transporter(f,pos=[10, 2 * (i+2)]))
	
	for _ in range(5):
		s.add_to_stock(Block(s))
	
	for _ in range(3):
		f.order_product(BEARING_BLOCK(f.time))
	
	fv = FactoryVisualizer(f)

	fv.run()

if __name__ == "__main__":
	main()
