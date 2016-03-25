"""This file implements the parent class for a simulator."""


import numpy as np
import scipy.integrate as spi



class Simulator():


    __GRAVITY = 9.81
    __E3_VERSOR = np.array([0.0, 0.0, 1.0])


    @classmethod
    def description(cls):
        return "Abstract Simulator"
        
        
    @classmethod
    def get_gravity(cls):
        return float(cls.__GRAVITY)
        
        
    @classmethod
    def get_e3(cls):
        return np.array(cls.__E3_VERSOR)
        
       
    @classmethod
    def get_state_size(cls):
        raise NotImplementedError()
        
        
    @classmethod
    def get_control_size(cls):
        raise NotImplementedError()


    def __init__(self, initial_time=0.0,
            initial_state=None,
            initial_control=None):
        
        if initial_state==None:
            initial_state = np.zeros(self.get_state_size())
            
        if initial_control==None:
            initial_control = np.zeros(self.get_control_size())
            
        self.__time = initial_time
       
        assert len(initial_state) == self.get_state_size()
        self.__state = np.array(initial_state)
        
        assert len(initial_control) == self.get_control_size()
        self.__control = np.array(initial_control)
        
        #TODO This is not very nice stylistically.
        # We should change f into a descriptive name
        # or use a lambda function.
        def f(t,x):
            return self.vector_field(t, x, self.__control)
        self.__solver = spi.ode(f).set_integrator('dopri5')
                
        self.__time_record = []
        self.__state_record = [[] for index in range(self.get_state_size())]
        self.__control_record = [[] for index in range(self.get_control_size())]
                
                
    def __str__(self):
        string = self.description()
        string += "\nTime: " + str(self.__time)
        string += "\nState: " + str(self.__state)
        string += "\nControl: " + str(self.__control)
        return string
        
        
    def get_time(self):
        return float(self.__time)
        
    
    def get_state(self):
        return np.array(self.__state)
        
        
    def get_control(self):
        return self.__control
        
        
    def get_time_record(self):
        return list(self.__time_record)
        
    
    def get_state_record(self):
        return list(self.__state_record)
        
        
    def get_control_record(self):
        return list(self.__control_record)
        
        
    def get_parameters(self):
        raise NotImplementedError()
        
        
    def set_control(self, control):
        assert len(control) == get_control_size
        self.__control = np.array(control) 
    
    
    def set_parameters(self, parameters):
        raise NotImplementedError()
    
        
    def reset(self, initial_time=0.0,
            initial_state=None,
            initial_control=None):
        
        if initial_state==None:
            initial_state = np.zeros(self.get_state_size())
            
        if initial_control==None:
            initial_control = np.zeros(self.get_control_size())
        
        self.__time = initial_time
        
        assert len(initial_state) == self.get_state_size()
        self.__state = np.array(initial_state)
        
        assert len(initial_control) == self.get_control_size()
        self.__control = np.array(initial_control)
        
        self.__solver.set_initial_value(initial_time, initial_state)
                
                
    def vector_field(self, time, state, control):
        raise NotImplementedError()
        
        
    def run(self, time_step):
        self.__time_record.append(self.__time)
        for index in range(self.get_state_size()):
            self.__state_record[index].append(self.__state[index])
        for index in range(self.get_control_size()):
            self.__control_record[index].append(self.__control[index])
        self.__solver.set_initial_value(np.array(self.__state), self.__time)
        self.__solver.integrate(self.__time + time_step)
        self.__time = self.__solver.t
        self.__state = np.array(self.__solver.y)
        
        
        
        
#"""Test"""
#my_sim = Simulator()
#print my_sim