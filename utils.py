import numpy as np
import pandas as pd

###################################################################
#                          Food Category                          #
###################################################################

POTATOES = ['D4', 'D5', 'D6', 'D7', 'D8', 'D27']
FRUITS_VEGETABLES = ['D22', 'D23', 'D24', 'D25', 'D26', 'D28', 'D29']
LPFEM = ['D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17']
BEANS = ['D18', 'D19', 'D20', 'D21']
OTHERS = ['D30']

FRESH_VEGETABLES = ['D22']
FRESH_FRUITS = ['D28']
DAIRY_PRODUCTS = ['D14','D15','D16']
CEREAL = ['D5','D6']
EGG = ['D17']
AQUATIC_PRODUCTS = ['D13']

HIGH_BAIJIU = 0.50
LOW_BAIJIU = 0.40
BEER = 0.04
GRAPE = 0.10
YELLOW_WINE = 0.15


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
        
    def __repr__(self):
        message = "id, birth, sex, nation, nation_name, edu, married, career"
        return f"{self.__class__.__name__}({message})"        
       
        
class SMOKE:
    def __init__(self, smoke, begin_smoke, smoke_days_per_week, smoke_nums_per_day,
                 passive_smoke, passive_smoke_days_per_week):
        self.smoke = smoke
        self.begin_smoke = begin_smoke
        self.smoke_days_per_week = smoke_days_per_week
        self.smoke_nums_per_day = smoke_nums_per_day
        self.passive_smoke = passive_smoke
        self.passive_smoke_days_per_week = passive_smoke_days_per_week
        
    def __repr__(self):
        message = "smoke, begin_smoke, smoke_days_per_week, smoke_nums_per_day, "
        message += "passive_smoke, passive_smoke_days_per_week"
        return f"{self.__class__.__name__}({message})"      


class WINE:
    def __init__(self, drink, num_per_week, drink_volume):
        self.drink = drink
        self.num_per_week = num_per_week
        self.drink_volume = drink_volume
        
    def get_alcohol_gram(self, degree):
        if self.num_per_week and self.drink_volume:
            return self.num_per_week * self.drink_volume * 50 * 0.8 * degree / 7 
        else:
            return 0 if self.drink == 2 else None
            
    def __repr__(self):
        message = "drink, num_per_week, drink_volume"
        return f"{self.__class__.__name__}({message})" 


class DRINK:
    def __init__(self, drink, drink_years: WINE, high_baijiu_info: WINE, low_baijiu_info: WINE, 
                 beer_info: WINE, yellow_info: WINE, grape_info: WINE):
        self.drink = drink
        self.drink_years = drink_years
        self.high_baijiu_info = high_baijiu_info
        self.low_baijiu_info = low_baijiu_info
        self.beer_info = beer_info
        self.yellow_info = yellow_info
        self.grape_info = grape_info
        self.data_process()
        
    def data_process(self):
        if self.drink == 2:
            self.drink_gram = 0
            self.light_wine = True
        else:
            self.high_baijiu_gram = self.high_baijiu_info.get_alcohol_gram(HIGH_BAIJIU)
            self.low_baijiu_gram = self.low_baijiu_info.get_alcohol_gram(LOW_BAIJIU)
            self.beer_gram = self.beer_info.get_alcohol_gram(BEER)
            self.yellow_gram = self.yellow_info.get_alcohol_gram(YELLOW_WINE)
            self.grape_gram = self.grape_info.get_alcohol_gram(GRAPE)
            if self.high_baijiu_gram is None or self.low_baijiu_gram is None or \
                self.beer_gram is None or self.yellow_gram is None or self.grape_gram is None:
                    self.light_wine = None
            else:
                self.drink_gram = self.high_baijiu_gram + self.low_baijiu_gram + \
                    self.beer_gram + self.yellow_gram + self.grape_gram
                self.light_wine = True if self.drink_gram < 15 else False
            
    def __repr__(self):
        message = "drink, drink_years, drink_gram, high_baijiu_info, low_baijiu_info, "  
        message += "beer_info, yellow_info, grape_info, light_wine"
        return f"{self.__class__.__name__}({message})"  


class MEALS:
    def __init__(self, breakfast, lunch, dinner) -> None:
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        
    def __repr__(self):
        message = "breakfast, lunch, dinner"
        return f"{self.__class__.__name__}({message})"         
    
    
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
        
    def __repr__(self):
        message = "no_eat, home, take, canteen, out, "
        message += "persons_of_weekdays, persons_of_weekends"
        return f"{self.__class__.__name__}({message})"    


class ACTIVITY:
    def __init__(self, work, housework, exercise, intensity, seconds_per_day):
        self.work = work
        self.housework = housework
        self.exercise = exercise
        self.intensity = intensity
        self.seconds_per_day = seconds_per_day
        self.data_process()
        
    def data_process(self):
        if self.exercise != 1 and self.seconds_per_day is None:
            self.healthy_exercise = None
        elif self.exercise != 4 or (self.seconds_per_day * 7 < 150):
            self.healthy_exercise = False
        else:
            self.healthy_exercise = True
        
    def __repr__(self):
        message = "work, housework, exercise, intensity, seconds_per_day"
        message += "healthy_exercise"
        return f"{self.__class__.__name__}({message})"            


class FOODS:
    def __init__(self, *foods):
        for i, food in enumerate(foods, start=4):
            setattr(self, f"D{i}", food)
        self.data_process()
                     
    def data_process(self):
        self.num_day_foods = 0
        self.num_week_foods = 0
        self.count_num([(POTATOES, "num_potatoes"), (LPFEM, "num_lpfem"),
                        (FRUITS_VEGETABLES, "num_fruits_vegetables"),
                        (BEANS, "num_beans"), (OTHERS, "num_others")])
        self.count_quantity([(LPFEM, "quantity_lpfem"), (BEANS, "quantity_beans"),
                             (FRESH_VEGETABLES, "quantity_fresh_vegetables"),
                             (FRESH_FRUITS, "quantity_fresh_fruits"),
                             (DAIRY_PRODUCTS, "quantity_dairy_products"),
                             (CEREAL, "quantity_cereal"), (EGG, "quantity_egg")])
        self.balanced_diet = True if (self.num_potatoes>=1) and \
            (self.num_fruits_vegetables>=1) and (self.num_lpfem>=1) \
            and (self.num_beans>=1) else False
        self.food_diversity = True if (self.num_day_foods >= 12) and \
            (self.num_week_foods >= 25) else False
        self.fresh_vegetables = True if (self.quantity_fresh_vegetables >= 6) else False
        self.fresh_fruits = True if (self.quantity_fresh_fruits >= 4) and \
            (self.quantity_fresh_fruits <= 7) else False
        self.dairy_products = True if (self.quantity_dairy_products >= 4) and \
            (self.quantity_dairy_products <= 10) else False
        self.cereal = True if (self.quantity_cereal >= 3) else False
        self.lpfem = True if (self.quantity_lpfem >= 2.4) and (self.quantity_lpfem <= 4) else False
        self.egg = True if (self.quantity_egg >= 1) and (self.quantity_egg <=2) else False
        if self.D33 is None:
            self.light_salt = None
        else:
            self.light_salt = True if (self.D33 * 50 / 30 < 5) else False
    
    def count_num(self, count_list:list):
        for count_item in count_list:
            self._count_num(count_item[0], count_item[1])
            
    def _count_num(self, type, count):
        counter = 0
        for attr in type:
            food = getattr(self, attr)
            if food.per_day:
                self.num_day_foods += 1
                self.num_week_foods += 1
                counter += 1
            elif food.per_week:
                self.num_day_foods += food.per_week / 7
                self.num_week_foods += 1
                counter += food.per_week / 7
            elif food.per_month:
                self.num_day_foods += food.per_month / 30
                self.num_week_foods += food.per_month / 4
                counter += food.per_month / 30 
        setattr(self, count, counter)
    
    def count_quantity(self, count_list:list):
        for count_item in count_list:
            self._count_quantity(count_item[0], count_item[1])
            
    def _count_quantity(self, type, count):
        quantity = 0
        for attr in type:
            food = getattr(self, attr)
            if food.eat == 1 and food.consume != None:
                if food.per_day:
                    quantity += food.consume * food.per_day
                elif food.per_week:
                    quantity += food.consume * food.per_week / 7
                elif food.per_month:
                    quantity += food.consume * food.per_month / 30
        setattr(self, count, quantity)
                                                    
    def __repr__(self):
        message = "D4 to D30, num_day_foods, num_week_foods, num_potatoes, "
        message += "num_fruits_vegetables, num_lpfem, num_beans, num_others, "
        message += "balanced_diet, food_diversity, fresh_vegetables, fresh_fruits, "
        message += "dairy_products, cereal, lpfem, egg, aquatic_products"
        return f"{self.__class__.__name__}({message})"    
    
    
class FOOD:
    def __init__(self, eat, per_day, per_week, per_month, consume):
        self.eat = eat
        self.per_day = per_day
        self.per_week = per_week
        self.per_month = per_month
        self.consume = consume
        
    def __repr__(self):
        message = "eat, per_day, per_week, per_month, consume"
        return f"{self.__class__.__name__}({message})"           
        
        
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
        
    def __repr__(self):
        message = "hypertension, diabetes, D1, D2, D3, D4, D5, D6 ,D7, D8"
        return f"{self.__class__.__name__}({message})"        
    
    
class DISEASE:
    def __init__(self, last, ill, methods, medication, control_diet, exercise, others):
        self.last = last
        self.ill = ill
        self.methods = methods
        self.medication = medication
        self.control_diet = control_diet
        self.exercise = exercise
        self.others = others
        
    def __repr__(self):
        message = "last, ill, methods, medication, control_diet, exercise, others"
        return f"{self.__class__.__name__}({message})"  
    
              
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
        self.data_process()
        
    def data_process(self):
        if self.weight and self.height:
            self.BMI = self.weight / (self.height * self.height) * 10000
            self.healthy_weight = True if (self.BMI < 24 and self.BMI >= 18.5) else False
        else:
            self.BMI = None
            self.healthy_weight = None
        
    def __repr__(self):
        message = "height, weight, waist, hip, systolic, diastolic, pulse, cholesterol, "
        message += "blood_sugar, high_lipoprotein, low_lipoprotein, triglycerides, uric_acid, "
        message += "BMI, healthy_weight"
        return f"{self.__class__.__name__}({message})"        


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
        self.cal_guideline()
        
    def cal_guideline(self):
        self.evaluate_info = EVALUATE()
        self.evaluate_info.add_evaluate(
            [("balanced_diet", self.foods_info.balanced_diet),
             ("food_diversity", self.foods_info.food_diversity),
             ("fresh_vegetables", self.foods_info.fresh_vegetables),
             ("fresh_fruits", self.foods_info.fresh_fruits),
             ("dairy_products", self.foods_info.dairy_products),
             ("cereal", self.foods_info.cereal),
             ("lpfem", self.foods_info.lpfem),
             ("healthy_weight", self.body_info.healthy_weight),
             ("healthy_exercise", self.activity_info.healthy_exercise),
             ("light_salt", self.foods_info.light_salt),
             ("light_wine", self.drink_info.light_wine)])
                
    def __repr__(self):
        message = "basic_info, smoke_info, drink_info, meals_info, foods_info, " 
        message += "activity_info, health_info, body_info, evaluate_info"
        return f"{self.__class__.__name__}({message})"         


class Persons:
    def __init__(self):
        self.person_dict = dict()
        self.message = "person_dict"
        
    def add_person(self, person: Person):
        self.person_dict[person.basic_info.id] = person
    
    def statistics(self, name="balanced_diet"):
        total = len(self.person_dict)
        effective = 0
        meet = 0
        for person in self.person_dict.values():
            evaluate_info = getattr(person, "evaluate_info")
            evaluate_dict = getattr(evaluate_info, "evaluate_dict")
            if evaluate_dict[name] is not None:
                effective += 1
                meet += int(evaluate_dict[name])
        setattr(self, "stat_"+name, STATISTICS(name, total, effective, meet))         
        self.message += (", stat_" + name)
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.message})" 


class EVALUATE:
    def __init__(self):
        self.evaluate_dict = dict()
    
    def add_evaluate(self, add_list:list):
        for add_item in add_list:
            self._add_evaluate(add_item[0], add_item[1])
            
    def _add_evaluate(self, name, value):
        self.evaluate_dict[name] = value
        
    def __repr__(self):
        message = "evaluate_dict"
        return f"{self.__class__.__name__}({message})"       


class STATISTICS:
    def __init__(self, name, total, effective, meet):
        self.name = name
        self.total = total
        self.effective = effective
        self.meet = meet

    def draw(self):
        pass
    
    def __repr__(self):
        message = "name, total, effective, meet" 
        return f"{self.__class__.__name__}({message})" 
           
           
###################################################################
#                     Data-Processed Function                     #
###################################################################

def replace_nan_with_none(arr):
    result = list()
    for row in arr:
        new_row = list()
        for value in row:
            try:
                # replace nan with none
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
    

def get_data(filename="data/processed_data.npy"):
    data = np.load(filename, allow_pickle=True)
    persons = Persons()
    for person_data in data:
        persons.add_person(Person(person_data))
    return persons
