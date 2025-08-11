from time import sleep
import epics

command_pv_root = 'ExecuteCommand.VAL'
IOC_prefix = '7bmbHXP:'
command_PV = IOC_prefix + command_pv_root
vert_motor = 'm3'
default_vert_offset = 350.0

def set_IOC_prefix(input_prefix):
    IOC_prefix = input_prefix
    command_PV = IOC_prefix + command_pv_root


def set_work_coordinates(x, y, z, a, b, c):
    '''Set the origin point and orientation of the work
    coordinate system.  
    This system does not move relative to the hexapod base.
    x, y, and z are linear translations.
    a, b, and c are rotations about these axes in degrees.
    Rotations are c first, then b, then a.
    Note that z is vertical in the Aerotech coordinate system.
    '''
    epics.caput(command_PV, f'SetBaseToWork({x}, {y}, {z}, {a}, {b}, {c})')


def enable_hexapod():
    '''Enable the hexapod in work coordinates and set
    default position and orientation of origin.
    '''
    epics.caput(command_PV, 'EnableWork()')
    sleep(2.0)
    set_work_coordinates(0, 0, 0, 0, 0, 0)
    

def set_rotation_point_height(tool_height, tool_name = "Tool1"):
    '''Sets the height of the tool above the moving platform.
    '''
    motor_high_limit_PV = IOC_prefix + vert_motor + '.HLM'
    motor_low_limit_PV = IOC_prefix + vert_motor + '.LLM'
    current_high_limit = epics.caget(motor_high_limit_PV)
    current_low_limit = epics.caget(motor_low_limit_PV)
    epics.caput(command_PV, f'SetToolPoint(1,"{tool_name}", 0, 0, {tool_height}, 0, 0, 0)')
    sleep(0.5)
    epics.caput(command_PV, f'ActivateTool("{tool_name}")')
    sleep(0.5)
    motor_offset_PV = IOC_prefix + vert_motor + '.OFF'
    epics.caput(motor_offset_PV, -(default_vert_offset + tool_height))
    sleep(0.1)
    epics.caput(motor_high_limit_PV, current_high_limit)
    epics.caput(motor_low_limit_PV, current_low_limit)
    sleep(0.5)
    #Set the VAL to the same as the RBV, since this doesn't update 
    #correctly automatically in the motor record.
    epics.caput(IOC_prefix + vert_motor + '.VAL',
                epics.caget(IOC_prefix + vert_motor + '.RBV'))

