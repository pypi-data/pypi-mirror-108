import pandas as pd

class Client:
    def __init__(self, name, CPF, date, product):
        self.name = name
        self.CPF = CPF
        self.date = date
        self.product = product
        
    def push_to_database(self, database):
        dictionary = {'Name': self.name,
                      'CPF': self.CPF,
                      'Date': self.date,
                      'Product': self.product}
        
        df = pd.DataFrame(dictionary, index=[0])
        
        database = pd.concat([database, df])
        return database
    
    def __str__(self):
        return f'''
Name: {self.name}
CPF: {self.CPF}
Date: {self.date}
Product: {self.product}'''
