#!/usr/bin/env python3
import rospy
from flexbe_core import EventState
from flexbe_core.proxy import ProxyServiceCaller
from hrwros_gazebo.srv import SetConveyorControl, SetConveyorControlRequest

class SetConveyorPowerState(EventState):
    '''

    -- stop     bool        if true the state instance stops the conveyor belt,
                            ignoring the speed inputkey
    ># speed    float       speed for the conveyor belt
    <= succeeded            the speed was successfully updated
    <= failed               there was a problem setting the speed

    '''

def __init__(self,stop):
    # declare outcomes, input_keys, and output_keys by calling the super
    # constructor with the corresponding arguments
    super(SetConveyorPowerState, self).__init__(outcomes = ['succeeded', 'failed'], input_keys = ['speed'])

    # store state parameter for later use
    self._stop = bool(stop)

    #initialize service proxy
    self._srv = ProxyServiceCaller({self._srv_topic: SetConveyorPower})

def on_enter(self, userdata):
    self.speed = userdata.speed
    # create service request depending on activation parameter and userdata 
    self._srv_req = ConveyorBeltControlRequest()

    if self._stop is True:
        self._srv_req.state.power = 0
    else:
        self._srv_req.state.power = self.speed
    try:
        self._srv_result = self._srv.call(self._srv_topic,self._srv_req)
    
    except Exception as e:
        rospy.logwarn(str(e))

def execute(self, userdata):
    #if no outcome is returned, the state will stay active
    if self._failed:
        return 'failed'
    if self._srv_result.success is True:
        return 'succeeded'
    else:
        return 'failed'
    
def on_start(self):
    pass

def on_exit(self, userdata):
    pass

def on_stop(self):
    pass