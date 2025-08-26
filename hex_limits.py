import re

from time import sleep
from epics import PV

def find_limit(motor_pvname, direction):

    pv_desc, pv_dval, pv_rbv, pv_hl, pv_ll = epics_pvs(motor_pvname)

    start_pos = pv_dval.get()
    step = 0.5
    tolerance = 0.001
    wait_time = 0.3

    if direction == 'up':
        end_pos = pv_hl.get()
        limit_pv = pv_hl
        condition = lambda pos: pos <= end_pos
        step_sign = step
        error_check = lambda err: err > tolerance
        limit_name = "high"
    elif direction == 'down':
        end_pos = pv_ll.get()
        limit_pv = pv_ll
        condition = lambda pos: pos >= end_pos
        step_sign = -step
        error_check = lambda err: err < -tolerance
        limit_name = "low"
    else:
        raise ValueError("Direction must be 'up' or 'down'")

    pos = start_pos
    while condition(pos):
        pv_dval.put(pos, wait=True)
        sleep(wait_time)
        pos_error = pv_dval.get() - pv_rbv.get()
        print(pos, pos_error)

        if error_check(pos_error):
            print(f"Reached {limit_name} limit")
            pv_dval.put(start_pos, wait=True)
            limit_pv.put(pos - step_sign, wait=True)
            exit()
        pos += step_sign


def main():

    # m1_hign_limit = find_limit('2bmHXP:m1', 'up')
    m1_low_limit  = find_limit('2bmHXP:m1', 'down')

if __name__ == '__main__':
    main()


