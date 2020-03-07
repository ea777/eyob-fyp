from django.shortcuts import render
import pandas as pd
import os
from analysis import aws
from analysis.helper_scripts.calc_avg_sa import calc_avg_sa
from collections import Counter
import json
import nltk
from nltk.corpus import stopwords

# Create your views here.
def index(request):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    # first check if the folder exists
    if os.path.exists((os.path.join(THIS_FOLDER, "excelfiles"))) != True:
        print("Directory doesn't exist - Creating")
        os.mkdir((os.path.join(THIS_FOLDER, "excelfiles")))
        aws.pulling_excelfiles()
    else:
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

        shops.append({"name": name, "sa": calc_avg_sa(file)})

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
        response = {"name": id, "rows": Row_list, "avg_sa": calc_avg_sa((id.lower().replace(" ", "-"))+'_reviews.xlsx')}
    return render(request, 'shopTable.html', {"response": response})


def shop_chart(request, id):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    if len(os.listdir(os.path.join(THIS_FOLDER, "static/csvfiles"))) == 0:
        print("Directory is empty")
        aws.pulling_csvfiles()
    else:
        print("Directory is not empty")
        csv_files = os.listdir(os.path.join(THIS_FOLDER, "static/csvfiles"))

    my_csvfile = 'csvfiles/'+(id.lower().replace(" ", "-")) + '_reviews.csv'
    my_excelfile = (id.lower().replace(" ", "-")) + '_reviews.xlsx'

    my_excelfile_keywords = os.path.join(THIS_FOLDER, 'excelfiles/' + (id.lower().replace(" ", "-")) + '_reviews.xlsx')

    # read form excel as dataframe
    df = pd.read_excel(my_excelfile_keywords, sheet_name='Sheet1')

    # clear file first
    open(os.path.join(THIS_FOLDER, 'static/keywords.txt'), 'w').close()

    words_list = []
    final_list_json = []

    # Iterate over each Keywords column
    for rows in df['Keywords']:
        # Write into keywords txt
        words = str(rows).replace(",", " ").lower()

        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        words_array = words.split(" ")

        for word in words_array:
            # remove punctuation from the word
            no_punct = ""
            for char in word:
                if char not in punctuations:
                    no_punct = no_punct + char

            words_list.append(no_punct)

    # using remove() to remove empty string from list
    while "" in words_list:
        words_list.remove("")

    s = set(stopwords.words('english'))
    final_words_list = [w for w in words_list if not w in s]

    filtered_sentence = []

    for w in final_words_list:
        if w not in s:
            filtered_sentence.append(w)

    unique_words = set(filtered_sentence)
    for word in unique_words:
        d = Counter(filtered_sentence)
        final_list_json.append({"word": word, "weight": ((d[word] / len(filtered_sentence)) * 100) * 2 })

    response = {"name": id, "csv": my_csvfile, "avg_sa": calc_avg_sa(my_excelfile), "keywords": json.dumps(final_list_json)}
    return render(request, 'shopChart.html', {"response": response})
