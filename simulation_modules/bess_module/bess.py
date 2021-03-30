from datetime import datetime, timedelta, timezone
from threading import Timer
from simulation_modules.bess_module.custom_exceptions import ChargeRequestRejected

class Bess:

    # 2 clock types - real_time (synced to system clock) and manual (must be manually updated)
    def __init__(self, bess_parameters, sio, clock_start=datetime.now(timezone.utc)):

        self.sio = sio

        self.charge_capacity = float(bess_parameters['batteryCapacity']) # measured in kWh

        self.current_charge = 0.0

        self.internal_clock = clock_start

        self.charging_status = 'idle' # possible values - idle, charging, discharging

        self.need_to_charge = 0 # positive value is charging, negative is discharging

        self.charge_rate = float(bess_parameters['batteryPower']) # measured in kW

        # Status returned in every clock_update call with some information represented as a dict
        self.clock_update_status = {
            ## Possible Values ##
            # finished_charge: Boolean
            # discharge_remaining: Number
        }

        # self.historic_clock()
    
    ### INTERNAL METHODS (Don't use outside class definition) ###

    def historic_clock(self):
        interval = timedelta(seconds=30)

        while(self.internal_clock < datetime.now(timezone.utc)):
            self.on_clock_update(self.internal_clock - interval, self.internal_clock)
            self.internal_clock += interval

        self.real_time_clock()

    def real_time_clock(self, prev_datetime=None):
        interval = 30.0 # in seconds, currently hard-coded but might need to change
        current_datetime = datetime.now(timezone.utc)

        if (prev_datetime is None):
            prev_datetime = current_datetime - timedelta(seconds=30.0)

        self.on_clock_update(prev_datetime, current_datetime)

        Timer(interval, self.real_time_clock, (current_datetime,)).start()

    def reset_status(self):
        self.need_to_charge = 0
        self.charging_status = 'idle'

    def on_clock_update(self, old_datetime, new_datetime):
        time_delta = new_datetime - old_datetime
        delta_hours = time_delta.seconds/3600

        if self.charging_status == 'idle':
            pass # TODO put in decay

        elif (self.charging_status == 'charging') or (self.charging_status == 'discharging'):
            self.charge(delta_hours)
        
        else:
            raise RuntimeError('charging_status must always have one of the following values - idle, charging, discharging')
        
        self.internal_clock = new_datetime

        # emit data every hour
        if (old_datetime.hour != new_datetime.hour):
            self.emit_data()
    
    def emit_data(self):
        self.sio.emit("New Bess", {
            "CurrentCharge": self.current_charge,
            "TimeStamp": self.internal_clock.isoformat(),
            "ChargingStatus": self.charging_status,
            "NeedToCharge": self.need_to_charge
        })

    def charge(self, delta_hours):

        charge_sign = 1 # Controls the charging value's sign. Positive for charging, negative for discharging.

        if (self.charging_status == 'discharging'):
            charge_sign = -1

        delta_charge_amount = (delta_hours*charge_sign*self.charge_rate) # max amount it can charge/discharge within this time delta
        
        if (abs(self.need_to_charge) > abs(delta_charge_amount)):
            updated_charge = self.current_charge + delta_charge_amount
            self.update_charge(updated_charge)
            self.need_to_charge -= delta_charge_amount

        else:
            updated_charge = self.current_charge + self.need_to_charge # add whatever is left in what it needs to charge
            self.update_charge(updated_charge)

            self.clock_update_status["finished_charge"] = True
            self.reset_status()

    def update_charge(self, updated_charge):
        # If the new charge is within the bounds of the battery's capacity
        if (0 < updated_charge < self.charge_capacity):
            self.current_charge = updated_charge

        else:
            if (self.charging_status == 'charging'):
                self.current_charge = self.charge_capacity
            elif (self.charging_status == 'discharging'):
                self.current_charge = 0
                self.clock_update_status["discharge_remaining"] = -updated_charge # Put in the status there is some discharge remaining

            self.reset_status() # fully charged/discharged so reset status

    ### PUBLIC METHODS (For use outside class definition) ###

    def clock_update(self, new_datetime):
        old_datetime = self.internal_clock
        self.clock_update_status = {} # Reset update status every run

        self.on_clock_update(old_datetime, new_datetime)
        return self.clock_update_status

    def start_charging(self, need_to_charge): # need_to_charge is positive for charging and negative for discharging
        if (self.charging_status == 'idle'):

            self.need_to_charge = need_to_charge

            if (need_to_charge > 0):
                self.charging_status = 'charging'
            elif (need_to_charge < 0):
                self.charging_status = 'discharging'
            else:
                raise RuntimeError('need_to_charge must be a positive or negative value')

        else:
            raise ChargeRequestRejected('Attempted to charge Bess while not in idle state, request to charge was ignored')