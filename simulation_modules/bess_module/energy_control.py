from datetime import datetime, time, timezone, timedelta
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
            "hour": 12,
            "minute": 0
        },
        "mode": "charge"
    }, {
        "start": {
            "hour": 12,
            "minute": 0
        },
        "end": {
            "hour": 15,
            "minute": 0
        },
        "mode": "discharge_arbitrage"
    }, {
        "start": {
            "hour": 15,
            "minute": 0
        },
        "end": {
            "hour": 23,
            "minute": 59
        },
        "mode": "charge"
    }]

    return temp_schedule
    
### Class Definition ###
class EnergyControl:
    def __init__(self, bess, schedule, ev_parameters_dict, bess_parameters_dict, sio, historical_start_time):
        self.bess = bess
        self.schedule = validate_schedule(schedule)
        self.sio = sio
        self.internal_clock = historical_start_time

        self.ev_parameters = ev_parameters_dict
        self.bess_parameters = bess_parameters_dict

        self.hour_check = historical_start_time.replace(second=0, microsecond=0, minute=0, hour=historical_start_time.hour)

        self.grid_use = {
            'GridUsage': 0
        }
        self.bess_use = {
            'EvUsage': 0
        }
        self.bess_arbitrage = {
            'BessArbitrage':0
        }
        self.past_mode = self.get_current_mode()

    def clock_update(self, new_datetime):
        bess = self.bess
        self.internal_clock = new_datetime
        bess_status = bess.clock_update(new_datetime)
        
        
        
        self.energy_arbitrage()
        self.bess_status_update()
        self.hour_update()
        

    def hour_update(self):
        if self.internal_clock > self.hour_check+timedelta(hours=1):
           
            self.hour_check += timedelta(hours=1)
            
            self.emit_data()

    def update_schedule(self, schedule):
        self.schedule = validate_schedule(schedule)
    
    def get_current_mode(self):
        current_time = self.internal_clock
        #print(current_time)
        for schedule_dict in self.schedule:
            if schedule_dict['start']['hour'] < current_time.hour < schedule_dict['end']['hour']:
                return schedule_dict["mode"]
            elif schedule_dict['start']['hour'] == current_time.hour and current_time.minute >= schedule_dict["start"]["minute"]:
                return schedule_dict["mode"]
            elif schedule_dict['end']['hour'] == current_time.hour and current_time.minute <= schedule_dict["end"]["minute"]:
                return schedule_dict["mode"]

        raise RuntimeError("Could not find current time in schedule, the schedule is invalid as it does not cover entire day")
   
    def emit_data(self):
        
        if self.past_mode == 'discharge_arbitrage':
            print(self.past_mode, self.get_current_mode())
            self.bess_arbitrage['BessArbitrage'] -= self.bess.current_charge
        else:
            self.bess_arbitrage['BessArbitrage'] = 0

        self.sio.emit('New Energy', {
            'BessEVUsage':self.bess_use['EvUsage'],
            'GridEvUsage':self.grid_use["GridUsage"],
            'BessArbitrage':self.bess_arbitrage['BessArbitrage'],
            'Timestamp':self.hour_check.isoformat()
        })
        self.bess_use['EvUsage'] = 0
        self.grid_use["GridUsage"] = 0
        self.bess_arbitrage['BessArbitrage'] = 0

    def bess_status_update(self):
        mode  = self.get_current_mode()
        
        if self.past_mode != mode:
            self.past_mode = mode
            self.bess.reset_status()
            # print(self.past_mode, self.get_current_mode(),'fss')
        

        if mode == 'charge':
            self.charge_bess()

    def energy_arbitrage(self):
        
        mode = self.get_current_mode()
        bess = self.bess

        if mode == 'discharge_arbitrage' and bess.current_charge != 0 and bess.charging_status == 'idle':
            
            bess.start_charging(-bess.current_charge)
            self.bess_arbitrage['BessArbitrage'] = bess.current_charge
            # print(bess.current_charge,'pop')
            
        elif mode == 'discharge_arbitrage' and bess.charging_status == 'discharging':

            if self.bess_arbitrage['BessArbitrage'] < bess.current_charge:
                print('fs',bess.current_charge)
                self.bess_arbitrage['BessArbitrage'] += bess.current_charge
            pass

    def charge_with_grid(self, charge_amount):
        self.grid_use["GridUsage"] += charge_amount
        # print('charge with grid')

    def charge_bess(self):
        mode = self.get_current_mode()
        bess = self.bess
        if mode == 'charge' and bess.current_charge != bess.charge_capacity and bess.charging_status == 'idle':
            bess.charge_rate = float(self.bess_parameters['batteryPower'])
            bess.start_charging(bess.charge_capacity)
            # print('bess is charging')

    def bess_charge_rate(self, ev_charger_level):
        bess = self.bess

        charge_rate_level_2 = float(self.bess_parameters['batteryPower'])/float(self.ev_parameters['evLevel2ChargeRate'])
        charge_rate_level_3 = float(self.bess_parameters['batteryPower'])/float(self.ev_parameters['evLevel3ChargeRate'])
        
        if ev_charger_level == 2:
            self.charge_rate = charge_rate_level_2
            # print(ev_charger_level, self.charge_rate,'lvl2')
        else:
            self.charge_rate = charge_rate_level_3
            # print(ev_charger_level, self.charge_rate,'lvl3')
    
    def request_ev_charge(self, charge_amount,ev_charger_level):
        mode = self.get_current_mode()
        bess = self.bess
        #print(mode)
        if (mode == "discharge_ev"):
            try:
                self.bess_charge_rate(ev_charger_level)
                bess.start_charging(-charge_amount)
                self.bess_use['EvUsage'] += charge_amount
                # print('ev takes bess')

            except ChargeRequestRejected:
                self.charge_with_grid(charge_amount)
                

        else:
            self.charge_with_grid(charge_amount)
            
