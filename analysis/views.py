from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import os


# Create your views here.
def index(request):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_excelfile = os.path.join(THIS_FOLDER, 'bunsen_reviews.xls')

    # read form excel as dataframe
    df = pd.read_excel(my_excelfile, sheet_name='Sheet1')
    # no need to display sentimental analysis and no.of reviews, so drop it
    df = df.iloc[:, :-2]

    print("Column headings:")
    print(df.columns)

    # add null to cells with empty values
    df['Name'].replace('', np.nan, inplace=True)
    df['Review'].replace('', np.nan, inplace=True)
    df['Date'].replace('', np.nan, inplace=True)

    df.dropna(subset=['Name'], inplace=True)
    df.dropna(subset=['Review'], inplace=True)
    df.dropna(subset=['Date'], inplace=True)

    # Create an empty list
    Row_list = []

    # Iterate over each row
    for rows in df.itertuples():
        # Create list for the current row
        my_list = [rows.Name, rows.Review, rows.Date]

        # append the list to the final list
        Row_list.append(my_list)

    # Print the list
    print(Row_list)

    # pass the list to template

    return render(request, 'index.html', {"response": Row_list})

class PostListView():

  template_name = 'index.html'
  context_object_name = 'rows'
  ordering = ['-date_posted']
  paginate_by = 5
