# -*- coding: utf-8 -*-



# TODO - add base type to recipe
# TODO - add issue to recipe
# TODO - let stock look for issue in task list
# TODO - add machine types to agents.py so factory can be dynamically initialized
# TODO - Ivan doesn't like select task due to random nature and untyped tuples
# TODO - replace machines with actions in tasks so that machines in the end could do/choose multiple operations, say if a machine could drill large or small holes.
# TODO - add hooks for performance visualizer

from visualizer import FactoryVisualizer
from activity_visualizer import ActivityVisualizer
from multiagent_factory.factory import Factory
import multiagent_factory.recipes as recipes

def main():
    """entry point to run the factory sim and visualizer"""
    f = Factory()
    fv = FactoryVisualizer(f)
    '''
    for _ in range(2):
        f.order_product(recipes.COATED_BEARING_BOX, 
						issue=[['block']])
    '''
    fv.run()

if __name__ == "__main__":
    main()
