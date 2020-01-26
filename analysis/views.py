from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import os
from analysis import aws
import json
import boto3


import re


# Create your views here.
def index(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    if len(os.listdir(os.path.join(THIS_FOLDER, "excelfiles"))) == 0:
        print("Directory is empty")
        aws.pulling_excelfiles()
    else:
        print("Directory is not empty")

    my_excelfile = os.path.join(THIS_FOLDER, 'excelfiles/bunsen-burger_reviews.xlsx')

    # read form excel as dataframe
    df = pd.read_excel(my_excelfile, sheet_name='Sheet1')
    # no need to display sentimental analysis and no.of reviews, so drop it
    # df = df.iloc[:, :-2]

    del df['Number of Reviews']

    print("Column headings:")
    print(df.columns)

    # Remove rows with 'Error'
    df = df[~df.Label.str.contains("ERROR")]

    # Create an empty list
    Row_list = []

    # Iterate over each row
    for rows in df.itertuples():
        # Create list for the current row
        my_list = [rows.Name, rows.Comment, rows.Date, rows.SA]

        # append the list to the final list
        Row_list.append(my_list)

    # pass the list to template
    return render(request, 'index.html', {"response": Row_list})


