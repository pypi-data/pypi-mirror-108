'''
Created on 11.06.2020

@author: JR
'''
from pyenzyme.enzymeml.core.functionalities import TypeChecker
import json

class Vessel(object):

    def __init__(self, name, id_, size, unit):
        
        '''
        Object describing an EnzymeML vessel.
        
        Args:
            String name: Name of Vessel
            String id: Internal Vessel identifier
            String constant: Volume is not chaning over time
            Float size: Numerical value of Vessel volume
            String unit: Unit of given size
        '''
        
        self.setName(name)
        self.setId(id_)
        self.setMetaid("METAID_" + id_.upper())
        self.setConstant(True)
        self.setSize(size)
        self.setUnit(unit)
        
    def toJSON(self, d=False, enzmldoc=False):
        
        def transformAttr(self):
            d = dict()
            for key, item in self.__dict__.items():
                
                if enzmldoc != False:
                        
                    if 'unit' in key:
                        if item: item = enzmldoc.getUnitDict()[item].getName()
                        if not item: item = "nan"
                            
                if str(item) != "nan": d[key.split('__')[-1]] = item
                
            return d
        
        if d: return transformAttr(self)
        
        return json.dumps(
            self, 
            default=transformAttr, 
            indent=4
            )
    
    def __str__(self):
        return self.toJSON()

    def getName(self):
        return self.__name


    def getId(self):
        return self.__id


    def getMetaid(self):
        return self.__metaid


    def getConstant(self):
        return self.__constant


    def getSize(self):
        return self.__size


    def getUnit(self):
        return self.__unit


    def setName(self, name):
        self.__name = TypeChecker(name, str)


    def setId(self, id_):
        self.__id = TypeChecker(id_, str)


    def setMetaid(self, metaid):
        self.__metaid = TypeChecker(metaid, str)


    def setConstant(self, constant):
        self.__constant = TypeChecker(constant, bool)


    def setSize(self, size):
        self.__size = TypeChecker(float(size), float)


    def setUnit(self, unit):
        self.__unit = TypeChecker(unit, str)


    def delName(self):
        del self.__name


    def delId(self):
        del self.__id


    def delMetaid(self):
        del self.__metaid


    def delConstant(self):
        del self.__constant


    def delSize(self):
        del self.__size


    def delUnit(self):
        del self.__unit

    _name = property(getName, setName, delName, "_name's docstring")
    _id = property(getId, setId, delId, "_id's docstring")
    _metaid = property(getMetaid, setMetaid, delMetaid, "_metaid's docstring")
    _constant = property(getConstant, setConstant, delConstant, "_constant's docstring")
    _size = property(getSize, setSize, delSize, "_size's docstring")
    _unit = property(getUnit, setUnit, delUnit, "_unit's docstring")

        
        