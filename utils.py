import numpy as np
import pandas as pd

###################################################################
#                        Information Class                        #
###################################################################

class BASIC:
    def __init__(self, id, birth, sex, nation, nation_name, edu, married, career):
        self.id = id
        self.birth = birth
        self.sex = sex
        self.nation = nation
        self.nation_name = nation_name
        self.edu = edu
        self.married = married
        self.career = career
        
        
class SMOKE:
    def __init__(self, smoke, begin_smoke, smoke_days_per_week, smoke_nums_per_day,
                 passive_smoke, passive_smoke_days_per_week):
        self.smoke = smoke
        self.begin_smoke = begin_smoke
        self.smoke_days_per_week = smoke_days_per_week
        self.smoke_nums_per_day = smoke_nums_per_day
        self.passive_smoke = passive_smoke
        self.passive_smoke_days_per_week = passive_smoke_days_per_week


class DRINK:
    def __init__(self, drink, drink_years, high_baijiu_info, low_baijiu_info, 
                 beer_info, yellow_wine_info, wine_info):
        self.drink = drink
        self.drink_years = drink_years
        self.high_baijiu_info = high_baijiu_info
        self.low_baijiu_info = low_baijiu_info
        self.beer_info = beer_info
        self.yellow_wine_info = yellow_wine_info
        self.wine_info = wine_info
        
    
class WINE:
    def __init__(self, drink, drink_days_per_week, drink_volume) -> None:
        self.drink = drink
        self.drink_days_per_week = drink_days_per_week
        self.drink_volume = drink_volume


class MEALS:
    def __init__(self, breakfast, lunch, dinner) -> None:
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        
    
class MEAL:
    def __init__(self, no_eat, home, take, canteen, out, 
                 persons_of_weekdays, persons_of_weekends):
        self.no_eat = no_eat
        self.home = home
        self.take = take
        self.canteen = canteen
        self.out = out
        self.persons_of_weekdays = persons_of_weekdays
        self.persons_of_weekends = persons_of_weekends


class ACTIVITY:
    def __init__(self, work, housework, exercise, intensity, seconds_per_day):
        self.work = work
        self.housework = housework
        self.exercise = exercise
        self.intensity = intensity
        self.seconds_per_day = seconds_per_day
        

class FOODS:
    def __init__(self, *foods):
        for i, food in enumerate(foods, start=4):
            setattr(self, f"D{i}", food)

class FOOD:
    def __init__(self, eat, per_day, per_week, per_month, consume):
        self.eat = eat
        self.per_day = per_day
        self.per_week = per_week
        self.per_month = per_month
        self.consume = consume
       
        
class HEALTH:
    def __init__(self, hypertension, diabetes, D1, D2, D3, D4, D5, D6 ,D7, D8) -> None:
        self.hypertension = hypertension
        self.diabetes = diabetes
        self.D1 = D1
        self.D2 = D2
        self.D3 = D3
        self.D4 = D4
        self.D5 = D5
        self.D6 = D6
        self.D7 = D7
        self.D8 = D8
    
    
class DISEASE:
    def __init__(self, last, ill, methods, medication, control_diet, exercise, others):
        self.last = last
        self.ill = ill
        self.methods = methods
        self.medication = medication
        self.control_diet = control_diet
        self.exercise = exercise
        self.others = others
        
class BODY:
    def __init__(self, height, weight, waist, hip, systolic, diastolic, pulse, cholesterol, 
                 blood_sugar, high_lipoprotein, low_lipoprotein, triglycerides, uric_acid):
        self.height = height
        self.weight = weight
        self.waist = waist
        self.hip = hip
        self.systolic = systolic
        self.diastolic = diastolic
        self.pulse = pulse
        self.cholesterol = cholesterol
        self.blood_sugar = blood_sugar
        self.high_lipoprotein = high_lipoprotein
        self.low_lipoprotein = low_lipoprotein
        self.triglycerides = triglycerides
        self.uric_acid = uric_acid


class Person:
    def __init__(self, data):
        self.basic_info = BASIC(*data[0:8])
        self.smoke_info = SMOKE(*data[8:14])
        self.drink_info = DRINK(data[14], data[15], *[WINE(data[i], data[i+1], data[i+2]) 
                                                      for i in range(16, 31, 3)])
        self.meals_info = MEALS(*[MEAL(data[i], data[i+1], data[i+2], data[i+3], data[i+4], 
                                       data[i+5], data[i+6]) for i in range(31, 52, 7)])
        self.foods_info = FOODS(*[FOOD(data[i], data[i+1], data[i+2], data[i+3], data[i+4]) 
                                  for i in range(52, 187, 5)], *data[187:194])
        self.activity_info = ACTIVITY(*data[194:199])
        self.health_info = HEALTH(*[DISEASE(data[i], data[i+1], data[i+2], data[i+3], data[i+4],
                                            data[i+5], data[i+6]) for i in range(199, 213, 7)], 
                                  *data[213:221])
        self.body_info = BODY(*data[221:234])
        

###################################################################
#                     Data-Processed Function                     #
###################################################################

def replace_nan_with_none(arr):
    result = list()
    for row in arr:
        new_row = list()
        for value in row:
            try:
                # replace nan with None
                new_row.append(None if np.isnan(value) else value)
            except:
                # chinese language
                new_row.append(value)
        result.append(new_row)
    return np.array(result)

def read_data(filename, save_path="data/processed_data.npy"):
    data = np.array(pd.read_excel(filename))
    data = replace_nan_with_none(data[1:])
    np.save(save_path, data)
    
    
if __name__ == '__main__':
    filename = 'data/附件2 慢性病及相关因素流调数据.xlsx'
    read_data(filename)