import json
from collections import namedtuple, defaultdict
from functools import wraps
import inspect
from pprint import pprint


class new_decorator(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        log_string = f'{self.func.__name__} was called'
        print(log_string)

        return self.func(*args)


def my_decorator(func):
    @wraps(func)
    def wrapper(*args):
        print(f'{func.__name__} was called')
        return func(*args)
    return wrapper


@new_decorator
def my_func(*args):
    print('hello world')


def profile():
    name = 'vwtal'
    age = 23
    height = 150
    Test = namedtuple('MyTest', 'name age height')
    return Test(name=name, age=age, height=height)


def add_to(num, target=[]):
    target.append(num)
    print(target)
    return target

colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

favourite_color = defaultdict(list)
for name, color in colours:
    favourite_color[name].append(color)

tree = lambda : defaultdict(tree)
some_dict = tree()
some_dict['lvl1']['lvl2'] = 'test'

colour =  {"Red" : 198, "Green" : 170, "Blue" : 160, 'white': 50, 'black':40, 'yellow':400 }

first_name = ['Joe','Earnst','Thomas','Martin','Charles']
last_name = ['Schmoe','Ehlmann','Fischer','Walter','Rogan','Green']
age = [23, 65, 11, 36, 83]

new_value = zip(first_name, last_name, age)
new_value = list(new_value)
test1, *test2 = zip(*new_value)


class MyClass(object):

    def __init__(self, ):
        self.info = {
            'name': 'vitaliy',
            'email': 'drozdik13@ukr.net',
            'age': 45
        }

    def __getitem__(self, item):
        return self.info[item]


a = MyClass()

def some_test(pattern):
    print(f'Searching for {pattern}')
    while True:
        line = (yield)
        if pattern in line :
            print(line)


def find_max(nums):
    max_num = float('-inf')
    for num in nums:
        if num > max_num:
            max_num = num
    return max_num


array = ['Welcome', 'To', 'Turing']
print('-'.join(array))