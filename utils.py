import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns

###################################################################
#                  Constant Variable Assumption                   #
###################################################################

POTATOES = ['D4', 'D5', 'D6', 'D7', 'D8', 'D27']
FRUITS_VEGETABLES = ['D22', 'D23', 'D24', 'D25', 'D26', 'D28', 'D29']
LPFEM = ['D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17']
BEANS = ['D18', 'D19', 'D20', 'D21']
BEVERAGE = ['D30']

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

FAMILY_PERSONS = 2.62


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
        self.age = 2023-self.birth
        
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
        self.drink_gram = 0
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


class MEAL:
    def __init__(self, no_eat, home, take, canteen, out, 
                 persons_of_weekdays, persons_of_weekends):
        self.no_eat = no_eat
        self.home = home
        self.take = take
        self.canteen = canteen
        self.out = out
        self.persons_of_weekdays = None if persons_of_weekdays \
            is None else persons_of_weekdays
        self.persons_of_weekends = None if persons_of_weekends \
            is None else persons_of_weekends
            
        self.avg_persons = None if (self.persons_of_weekdays is None or \
            self.persons_of_weekends is None) else \
            self.persons_of_weekdays * 5 / 7 + self.persons_of_weekends * 2 / 7
            
    def __repr__(self):
        message = "no_eat, home, take, canteen, out, persons_of_weekdays, "
        message += "persons_of_weekends, avg_persons"
        return f"{self.__class__.__name__}({message})"  


class MEALS:
    def __init__(self, breakfast: MEAL, lunch: MEAL, dinner: MEAL) -> None:
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        if self.breakfast.avg_persons is None or self.lunch.avg_persons \
            is None or self.dinner.avg_persons is None:
            self.meals_avg_persons = FAMILY_PERSONS 
        else:
            self.meals_avg_persons = (self.breakfast.avg_persons * 0.2 + \
            self.lunch.avg_persons * 0.4 + self.dinner.avg_persons * 0.4)
        
    def __repr__(self):
        message = "breakfast, lunch, dinner, meals_avg_persons"
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
                         (BEANS, "num_beans"), (AQUATIC_PRODUCTS,"frequency_aquatic_products")])
        self.count_qty([(LPFEM, "qty_lpfem"), (BEANS, "qty_beans"),
                             (FRESH_VEGETABLES, "qty_fresh_vegetables"),
                             (FRESH_FRUITS, "qty_fresh_fruits"),
                             (DAIRY_PRODUCTS, "qty_dairy_products"),
                             (CEREAL, "qty_cereal"), (EGG, "qty_egg"),
                             (BEVERAGE, "qty_beverage")])
        self.balanced_diet = True if (self.num_potatoes>=1) and \
            (self.num_fruits_vegetables>=1) and (self.num_lpfem>=1) \
            and (self.num_beans>=1) else False
        self.food_diversity = True if (self.num_day_foods >= 12) and \
            (self.num_week_foods >= 25) else False
        self.fresh_vegetables = True if (self.qty_fresh_vegetables >= 6) else False
        self.fresh_fruits = True if (self.qty_fresh_fruits >= 4) and \
            (self.qty_fresh_fruits <= 7) else False
        self.dairy_products = True if (self.qty_dairy_products >= 4) and \
            (self.qty_dairy_products <= 10) else False
        self.cereal = True if (self.qty_cereal <= 3) and \
            (self.qty_cereal >= 1) else False
        self.lpfem = True if (self.qty_lpfem >= 2.4) and (self.qty_lpfem <= 4) else False
        self.egg = True if (self.qty_egg >= 1) and (self.qty_egg <=2) else False
        self.aquatic_products = True if (self.frequency_aquatic_products * 7 >= 1) and (self.frequency_aquatic_products * 7 <= 3) else False
        if self.D33 is None:
            self.light_salt = None
        else:
            self.light_salt = True if (self.D33 * 50 / 30 < 5) else False
        self.D31 = 0 if self.D31 is None else self.D31 * 500 / 30
        self.D32 = 0 if self.D32 is None else self.D32 * 500 / 30
        self.qty_oil = None
        self.healthy_oil = None   
            
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
    
    def count_qty(self, count_list:list):
        for count_item in count_list:
            self._count_qty(count_item[0], count_item[1])
            
    def _count_qty(self, type, count):
        qty = 0
        for attr in type:
            food = getattr(self, attr)
            if food.eat == 1 and food.consume != None:
                if food.per_day:
                    qty += food.consume * food.per_day
                elif food.per_week:
                    qty += food.consume * food.per_week / 7
                elif food.per_month:
                    qty += food.consume * food.per_month / 30
        setattr(self, count, qty)
                                                    
    def __repr__(self):
        message = "D4 to D30, num_day_foods, num_week_foods, num_potatoes, "
        message += "num_fruits_vegetables, num_lpfem, num_beans, num_beverage, "
        message += "balanced_diet, food_diversity, fresh_vegetables, qty_fresh_vegetables, "
        message += "fresh_fruits, qty_fresh_fruits, dairy_products, qty_dairy_products, "
        message += "cereal, qty_cereal, lpfem, qty_lpfem, egg, qty_egg, aquatic_products, "
        message += "frequency_aquatic_products, light_salt, healthy_oil, qty_oil"
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
        self.data_process()
        self.cal_guideline()
    
    def data_process(self):
        self.meals_avg_persons = self.meals_info.meals_avg_persons
        if self.meals_avg_persons != 0:
            self.foods_info.D31 /= self.meals_avg_persons
            self.foods_info.D32 /= self.meals_avg_persons
            self.foods_info.qty_oil = self.foods_info.D31 + self.foods_info.D32
            self.foods_info.healthy_oil = True if \
                (self.foods_info.qty_oil >= 25 and self.foods_info.qty_oil <= 30) else False
        else:
            self.foods_info.qty_oil = 0
            self.foods_info.healthy_oil = 0
                       
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
             ("healthy_oil", self.foods_info.healthy_oil),
             ("light_salt", self.foods_info.light_salt),
             ("light_wine", self.drink_info.light_wine)])
        
        self.evaluate_info.add_qty(    
            [("num_day_foods", self.foods_info.num_day_foods),
             ("qty_f_veg", self.foods_info.qty_fresh_vegetables),
             ("qty_f_fruits", self.foods_info.qty_fresh_fruits),
             ("qty_d_prods", self.foods_info.qty_dairy_products),
             ("qty_cereal", self.foods_info.qty_cereal),
             ("qty_lpfem", self.foods_info.qty_lpfem),
             ("qty_oil", self.foods_info.qty_oil),
             ("BMI", self.body_info.BMI),
             ("exe_seconds", self.activity_info.seconds_per_day),
             ("salt", self.foods_info.D33),
             ("wine", self.drink_info.drink_gram),
             ("qty_beverage", self.foods_info.qty_beverage),
             ("age", self.basic_info.age),
             ("sex", self.basic_info.sex),
             ("married", self.basic_info.married),
             ("career", self.basic_info.career),
             ("edu", self.basic_info.edu)])
                        
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
    
    def statistics(self):
        attrs = self.person_dict[10001].evaluate_info.evaluate_dict.keys()
        self.evaluate_ratio = list()
        self.evaluate_info = list()
        for attr in attrs:
            self._statistics(attr)
            self.evaluate_ratio.append(getattr(self, attr).get_ratio())
            self.evaluate_info.append(getattr(self, attr).get_info())
        self.evaluate_ratio = np.array(self.evaluate_ratio)
        self.evaluate_info = np.array(self.evaluate_info)
        self.evaluate_ratio = self.evaluate_ratio[np.argsort(-self.evaluate_ratio[:, 2].astype(float))]
        self.evaluate_info = self.evaluate_info[np.argsort(-self.evaluate_info[:, 3].astype(int))]
            
    def _statistics(self, name="balanced_diet"):
        total = len(self.person_dict)
        effective = 0
        meet = 0
        data_list = list()
        for person in self.person_dict.values():
            evaluate_info = getattr(person, "evaluate_info")
            evaluate_dict = getattr(evaluate_info, "evaluate_dict")
            data_list.append(evaluate_dict[name])
            if evaluate_dict[name] is not None:
                effective += 1
                meet += int(evaluate_dict[name])
        data_list = np.array(data_list)
        setattr(self, name, STATISTICS(name, data_list, total, effective, meet=meet))         
        self.message += (", " + name)
    
    def get_dataframe(self):
        person_data = pd.DataFrame()
        for person in self.person_dict.values():
            append_data = getattr(person.evaluate_info, "evaluate_dict")
            append_data.update(getattr(person.evaluate_info, "qty_dict"))
            person_data = person_data._append(append_data, ignore_index = True)
        person_data.to_csv("docs/processed_data.csv")

    def get_line_data(self, attrs:list, name):
        total_val = 0
        total = len(self.person_dict)
        effective = 0
        data_list = list()
        for person in self.person_dict.values():
            begin = True
            for attr in attrs:
                if begin:
                    var = getattr(person, attr)
                    begin = False
                else:
                    var = getattr(var, attr)
            data_list.append(var)
            if var is not None:
                effective += 1
                total_val += var
        data_list = np.array(data_list)
        avarage = total_val / effective
        setattr(self, name, STATISTICS(name, data_list, total, effective, avarage=avarage))
        self.message += (", " + name)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.message})" 


class EVALUATE:
    def __init__(self):
        self.evaluate_dict = dict()
        self.qty_dict = dict()
        
    def add_evaluate(self, add_list:list):
        for add_item in add_list:
            self._add_evaluate(add_item[0], add_item[1])
            
    def _add_evaluate(self, name, value):
        self.evaluate_dict[name] = value

    def add_qty(self, add_list:list):
        for add_item in add_list:
            self._add_qty(add_item[0], add_item[1])
            
    def _add_qty(self, name, value):
        self.qty_dict[name] = value
                    
    def __repr__(self):
        message = "evaluate_dict, qty_dict"
        return f"{self.__class__.__name__}({message})"       


class STATISTICS:
    def __init__(self, name, data, total, effective, meet=None, avarage=None):
        self.name = name
        self.data = data
        self.total = total
        self.effective = effective
        self.meet = meet
        self.avarage = avarage

    def get_info(self):
        return [self.name, self.total, self.effective, self.meet]
    
    def get_ratio(self):
        return [self.name, 1-self.meet/self.effective, self.meet/self.effective]
    
    def __repr__(self):
        message = "name, data, total, effective"
        if self.meet:
            message += ", meet"
        if self.avarage:
            message += ", avarage"
        return f"{self.__class__.__name__}({message})" 

           
###################################################################
#                          Utils Function                         #
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


def read_data(filename, save_path="docs/processed_data.npy"):
    data = np.array(pd.read_excel(filename))
    data = replace_nan_with_none(data[1:])
    np.save(save_path, data)
    

def get_data(filename="docs/processed_data.npy"):
    data = np.load(filename, allow_pickle=True)
    persons = Persons()
    for person_data in data:
        persons.add_person(Person(person_data))
    persons.statistics()
    return persons


def draw_ratio(data, tilte="Evaluating Indicator", x_lable="", 
               y_label="Ratio",fig_name="pics/evaluate_ratio.png"):
    plt.rcParams.update({'font.size': 12})
    plt.figure(figsize=(14, 10))
    data = pd.DataFrame(data[:, 1:].astype(float), index=data[:, 0], columns=['False', 'True'])
    data['name'] = data.index
    bottom_plot = sns.barplot(x='name', y='True', data=data, color="#0000A3")
    sns.barplot(x='name', y='False', data=data, color="#FF0000", bottom=data['True'])
    topbar = plt.Rectangle((0, 0), 1, 1, fc="#FF0000", edgecolor='none')
    bottombar = plt.Rectangle((0, 0), 1, 1, fc='#0000A3', edgecolor='none')
    l = plt.legend([bottombar, topbar], ['standard', 'nonstandard'], loc=1, ncol = 2, prop={'size':8})
    l.draw_frame(False)
    sns.despine(left=True)
    bottom_plot.set_ylabel(y_label)
    bottom_plot.set_xlabel(x_lable)
    bottom_plot.set_xticklabels(data.name, rotation=20, fontsize='small')
    plt.ylim(0, 1.1)
    plt.title(tilte)
    plt.savefig(fig_name)
    
    
def draw_histogram(data, x, bins, fig_name, figsize=(14,10), font_size=12, 
                   stat='probability',color = '#008080', ):
    sns.set(rc = {'figure.figsize':figsize})
    plt.rcParams.update({'font.size': font_size})
    sns.displot(data=data, x=x, bins=bins, stat=stat, color=color)
    plt.savefig(fig_name)
