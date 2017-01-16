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
    f.add_agent(GreaseMachine(f, pos=[10,18]))
    f.add_agent(CoatMachine(f, pos=[3,20]))
    f.add_agent(ForceFitMachine(f, pos=[17,20]))
    f.add_agent(DeliveryMachine(f, pos=[20,5]))
 
    f.add_agent(BigDrillMachine(f, pos=[3,13]))
    f.add_agent(FineDrillMachine(f, pos=[17,13]))
    f.add_agent(GreaseMachine(f, pos=[10,21]))
    f.add_agent(CoatMachine(f, pos=[3,23]))
    f.add_agent(ForceFitMachine(f, pos=[17,23]))
    
    '''f.add_agent(BigDrillMachine(f, pos=[6,13]))
    f.add_agent(FineDrillMachine(f, pos=[20,13]))
    f.add_agent(GreaseMachine(f, pos=[13,21]))
    f.add_agent(CoatMachine(f, pos=[6,23]))
    f.add_agent(ForceFitMachine(f, pos=[20,23])) 
 
    f.add_agent(BigDrillMachine(f, pos=[6,10]))
    f.add_agent(FineDrillMachine(f, pos=[20,10]))
    f.add_agent(GreaseMachine(f, pos=[13,18]))
    f.add_agent(CoatMachine(f, pos=[6,20]))
    f.add_agent(ForceFitMachine(f, pos=[20,20]))'''
 
 

    #for i in range(10):
    for i in range(17):
        shift = 0
        if (2 * (i+2) > 20):
            shift = 3
        f.add_agent(Transporter(f,pos=[10 + shift, 2 * (i+2)%20]))

    s.add_to_stock(AssemblyTray(s))
    s.add_to_stock(AssemblyTray(s))
 
    for _ in range(50):
        s.add_to_stock(Block(s))
    for _ in range(50):
        s.add_to_stock(Bearing(s))

    for _ in range(4):
        f.order_product(BEARING_BLOCK(f.time))
        f.order_product(COATED_BEARING_BLOCK(f.time))
        f.order_product(BEARING_BLOCK_ASSY(f.time))
        f.order_product(COATED_BEARING_BLOCK_ASSY(f.time))
    
    fv = FactoryVisualizer(f)

    fv.run()

if __name__ == "__main__":
    main()
