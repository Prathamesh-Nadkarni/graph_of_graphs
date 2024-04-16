import time
import os
import openai
import pickle
import yaml
import pandas as pd
import csv
import numpy as np

def API_Request(Prompt:str) -> str:

    with open('src\Product Network\config.yml') as config:
      config_dict = yaml.safe_load(config)

    openai.api_key = config_dict["OpenAIAPI"]

    openai.Model.retrieve("gpt-3.5-turbo")

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": Prompt}]
        )
    
    return resp['choices'][0]['message']["content"]

def Isfloat(Float_String:int) -> bool:
    return Float_String.replace('.', '').isdigit()

def remove_whitespace(Probabilties_List:list) -> list:
    if len(Probabilties_List) != 10:
        return Probabilties_List
    for x in range(0,len(Probabilties_List)):
        Probabilties_List[x] = Probabilties_List[x].replace(" ", "")
    return Probabilties_List

def sort_response(Probabilties_List:list) -> list:
    if len(Probabilties_List) != 10:
        return Probabilties_List
    
    if "Health&Beauty" not in Probabilties_List or "Electronics" not in Probabilties_List  or "Books" not in Probabilties_List or "Groceries" not in Probabilties_List or "Home&Kitchen" not in Probabilties_List:
        return Probabilties_List
    
    He_index = Probabilties_List.index("Health&Beauty")
    E_index = Probabilties_List.index("Electronics")
    B_index = Probabilties_List.index("Books")
    G_index = Probabilties_List.index("Groceries")
    Ho_index = Probabilties_List.index("Home&Kitchen")

    return [Probabilties_List[He_index], Probabilties_List[He_index+1],Probabilties_List[E_index], Probabilties_List[E_index+1],Probabilties_List[B_index], Probabilties_List[B_index+1],Probabilties_List[G_index], Probabilties_List[G_index+1],Probabilties_List[Ho_index], Probabilties_List[Ho_index+1],]


def Request_Probabilities(Product:str) -> str:
    Request_Probabilities = "<act as a classifier> <give me probabilities that "+ Product + " belongs to the following five classes : [Health & Beauty, Electronics, Books, Groceries, Home & Kitchen]> <return the probabilities only><format : class,probability,class,probability><Do not reorder the list>"
    Class_Probabilities = API_Request(Request_Probabilities)
    Probabilties = Class_Probabilities.split(",")
    #Formatting Check
    Probabilties = remove_whitespace(Probabilties)
    Probabilties = sort_response(Probabilties)
    max_attempts = 0
    while len(Probabilties) != 10 or Probabilties[0] != "Health&Beauty" or Probabilties[2] != "Electronics" or Probabilties[4] != "Books" or Probabilties[6] != "Groceries" or Probabilties[8] != "Home&Kitchen":
        print("fail")
        print(Probabilties)
        Class_Probabilities = API_Request(Request_Probabilities)
        Probabilties = Class_Probabilities.split(",")
        Probabilties = remove_whitespace(Probabilties)
        Probabilties = sort_response(Probabilties)
        max_attempts = max_attempts + 1
        if max_attempts > 5:
            return ["Rate Limit"]
    return Probabilties

def Write_Data(Product:str, Probabilties:list) -> None:
    with open('src\Product Network\Probilities.csv','a', newline='', encoding='utf-8' , errors='replace') as fd:
        writer = csv.writer(fd)
        writer.writerow([Product,Probabilties[1],Probabilties[3],Probabilties[5],Probabilties[7],Probabilties[9]])

def main(Dataset:str):
    if Dataset == "product":
        Product_dataset = pd.read_csv('src\Product Network\AmazonProducts.csv')
        shuffled_indices = np.random.RandomState(seed=42).permutation(Product_dataset.index)
        Product_dataset_shuffled = Product_dataset.loc[shuffled_indices].reset_index(drop=True)
        Product_Index = 0
        
        for INDX in range(11000,len(Product_dataset_shuffled["name"])):
            Probabilities = Request_Probabilities(Product_dataset_shuffled["name"][INDX])
            if len(Probabilities) == 1 and Probabilities[0] == "Rate Limit":
                print(INDX)
                continue
            Write_Data(Product_dataset_shuffled["name"][INDX],Probabilities)
            Product_Index = Product_Index + 1
    if Dataset == "book":
        Product_book_dataset = pd.read_csv('src\Product Network\data_books.csv')
        shuffled_book_indices = np.random.RandomState(seed=42).permutation(Product_book_dataset.index)
        Product_dataset_book_shuffled = Product_book_dataset.loc[shuffled_book_indices].reset_index(drop=True)
        Product_Index = 0
        
        for INDX in range(0,2500):
            #len(Product_dataset_book_shuffled["Title"])
            Probabilities = Request_Probabilities("Book: " + Product_dataset_book_shuffled["Title"][INDX])
            if len(Probabilities) == 1 and Probabilities[0] == "Rate Limit":
                print(INDX)
                continue
            Write_Data(Product_dataset_book_shuffled["Title"][INDX],Probabilities)
            Product_Index = Product_Index + 1

    


if __name__ == "__main__":
    main("book")