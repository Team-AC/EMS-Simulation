from datetime import datetime, timedelta, timezone
from threading import Timer

class Bess:

    # 2 clock types - real_time (synced to system clock) and manual (must be manually updated)
    def __init__(self, bess_parameters, clock_start=datetime.now(timezone.utc)):

        self.charge_capacity = float(bess_parameters['batteryCapacity']) # measured in kWh

        self.current_charge = 0.0

        self.internal_clock = clock_start

        self.charging_status = 'idle' # possible values - idle, charging, discharging

        self.need_to_charge = 0 # positive value is charging, negative is discharging

        self.charge_rate = float(bess_parameters['batteryPower']) # measured in kW

        self.historic_clock()
    
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
        
        print(self.__dict__)


    def charge(self, delta_hours):

        charge_sign = 1 # Controls the charging value's sign. Positive for charging, negative for discharging.

        if (self.charging_status == 'discharging'):
            charge_sign = -1

        delta_charge_amount = (delta_hours*charge_sign*self.charge_rate) # max amount it can charge/discharge within this time delta
        
        if (abs(self.need_to_charge) > abs(delta_charge_amount)):

            updated_charge = self.current_charge + delta_charge_amount

            if (0 < updated_charge < self.charge_capacity):
                self.current_charge = updated_charge

            else:
                if (self.charging_status == 'charging'):
                    self.current_charge = self.charge_capacity
                elif (self.charging_status == 'discharging'):
                    self.current_charge = 0

                self.reset_status() # fully charged/discharged so reset status
        
        else:
            updated_charge += self.need_to_charge # add whatever is left in what it needs to charge
            self.reset_status()

    ### PUBLIC METHODS (for use outside class definition) ###

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
            raise RuntimeWarning('Attempted to charge Bess while not in idle state, request to charge was ignored')