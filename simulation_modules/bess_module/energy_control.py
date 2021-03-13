from datetime import datetime, time, timezone
from simulation_modules.bess_module.custom_exceptions import ChargeRequestRejected

### Some helper Methods For Class ###

def validate_schedule(schedule):
    """
    Schedule Format:
    [{
        start: {
            hour: Number
            minute: Number
        },
        end: {
            hour: Number 
            minute: Number
        },
        mode: charge or discharge_ev or discharge_arbitrage or discharge_load_shedding
    }]
    """

    temp_schedule = [{
        "start": {
            "hour": 0,
            "minute": 0
        },
        "end": {
            "hour": 23,
            "minute": 59
        },
        "mode": "charge"
    }]

    return temp_schedule

def is_time_between(begin_time, end_time, check_time=None):
# If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

### Class Definition ###
class EnergyControl:
    def __init__(self, bess, schedule, sio):
        self.bess = bess
        self.schedule = validate_schedule(schedule)
        self.sio = sio

    def clock_update(self, new_datetime):
        bess = self.bess

        bess_status = bess.clock_update(new_datetime)
    
    def update_schedule(self, schedule):
        self.schedule = validate_schedule(schedule)
    
    def get_current_mode(self):
        current_time = datetime.now(timezone.utc)
        for schedule_dict in self.schedule:
            if ((schedule_dict["start"]["hour"] <= current_time.hour) and (schedule_dict["start"]["minute"] <= current_time.minute) and (schedule_dict["end"]["hour"] >= current_time.hour) and (schedule_dict["end"]["minute"] >= current_time.minute)):
                return schedule_dict["mode"]

        raise RuntimeError("Could not find current time in schedule, the schedule is invalid as it does not cover entire day")
    
    def charge_with_grid(self, charge_amount):
        print("charging with grid")
        pass # TODO make logic
    
    def request_charge(self, charge_amount):
        mode = self.get_current_mode()
        bess = self.bess

        if (mode == "discharge_ev"):
            try:
                bess.start_charging(-charge_amount)
            except ChargeRequestRejected:
                self.charge_with_grid(charge_amount)
        else:
            self.charge_with_grid(charge_amount)