from django.shortcuts import render
import pandas as pd
import os
from analysis import aws


# Create your views here.
def index(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    if len(os.listdir(os.path.join(THIS_FOLDER, "excelfiles"))) == 0:
        print("Directory is empty")
        aws.pulling_excelfiles()
    else:
        print("Directory is not empty")
        excel_files = os.listdir(os.path.join(THIS_FOLDER, "excelfiles"))

    # list to store the detail of shops
    shops = []
    for file in excel_files:
        # split the file name before the underscore and get the name
        # then replace the hyphens with space
        name = ((file.split('_', 1)[0]).replace("-", " ")).title()

        # read form excel as dataframe
        my_excelfile = os.path.join(THIS_FOLDER, 'excelfiles/' + file)
        df = pd.read_excel(my_excelfile, sheet_name='Sheet1')
        # no need to display no.of reviews, so drop it
        del df['Number of Reviews']
        # Remove rows with 'Error'
        df = df[~df.Label.str.contains("ERROR")]

        # get the avg SA score
        sa = round(df["SA"].mean()*100, 2)
        shops.append({"name": name, "sa": sa})

    # pass the names of the files to the index page
    return render(request, 'index.html', {"shops": shops})


def shop_table(request, id):

    # convert the shopname to excel file name
    # first of all lower all words in the names and replace spaces with hyphens
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_excelfile = os.path.join(THIS_FOLDER, 'excelfiles/'+(id.lower().replace(" ", "-"))+'_reviews.xlsx')

    # read form excel as dataframe
    df = pd.read_excel(my_excelfile, sheet_name='Sheet1')
    # no need to display no.of reviews, so drop it
    del df['Number of Reviews']
    # Remove rows with 'Error'
    df = df[~df.Label.str.contains("ERROR")]

    # Create an empty list
    Row_list = []

    # Iterate over each row
    for rows in df.itertuples():
        # Create list for the current row
        my_list = [rows.Name, rows.Comment, rows.Keywords, rows.SA]

        # append the list to the final list
        Row_list.append(my_list)

    return render(request, 'shopTable.html', {"response": Row_list})


def shop_chart(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    if len(os.listdir(os.path.join(THIS_FOLDER, "csvfiles"))) == 0:
        print("Directory is empty")
        aws.pulling_csvfiles()
    else:
        print("Directory is not empty")
        csv_files = os.listdir(os.path.join(THIS_FOLDER, "csvfiles"))

    return render(request, 'charts.html')
