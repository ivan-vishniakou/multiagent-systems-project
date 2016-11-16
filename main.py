# -*- coding: utf-8 -*-

from viusalizer import FactoryVisualizer
from multiagent_factory.factory import Factory

def main():
    """entry point to run the factory sim and visualizer"""
    fv = FactoryVisualizer(Factory())
    fv.run()
    
if __name__ == "__main__":
    main()