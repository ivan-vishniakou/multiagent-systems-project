# -*- coding: utf-8 -*-

from visualizer import FactoryVisualizer
from multiagent_factory.factory import Factory

def main():
    """entry point to run the factory sim and visualizer"""
    f = Factory()
    fv = FactoryVisualizer(f)
    for _ in range(10):
        f.order_product(
                        [ (['blank'],[Factory.BIG_DRILLING_MACHINE,
                                      Factory.FINE_DRILLING_MACHINE]),
                          (['big_drilled', 'fine_drilled'],[Factory.COATING_MACHINE]),
                          (['big_drilled', 'fine_drilled', 'coated'],[Factory.DELIVER])
                        ], 
                issue=[['blank']]
                        )
    fv.run()

if __name__ == "__main__":
    main()