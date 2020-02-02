import requests
import pandas as pd
from openpyxl import load_workbook
import os


def analyse_comments(rows):
    workbook = load_workbook(filename=raw_excelfile)
    sheet = workbook.active

    count = 1

    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('version', '2019-07-12'),
    )
    # responseSrr = ""

    for comment in rows:
        count += 1
        try:
            comment = str(comment.encode('utf-8'))

            data = ' {\n  "text": "' + comment + '",' \
                                                 '\n  "features": {\n    "sentiment": {\n     \n},\n    ' \
                                                 '"keywords": {\n     \n}\n  }\n}'

            response = requests.post(
                'https://gateway-lon.watsonplatform.net/natural-language-understanding/api/v1/analyze',
                headers=headers, params=params, data=data,
                auth=('apikey', 'BaaDAfn3qpjkCo2Hsm173CLmCKqD-Bv2OIYpnxX4LetC')).json()

            # check if there is an error in the response. I think there is a lot of errors because of the free plan we are using.
            if "error" in response:
                print(str(count) + " ERROR " + str(response) + " - " + str(comment))
                add_senti_analysis(count, "ERROR", sheet, workbook)
                add_label(count, "ERROR", sheet, workbook)
                add_keywords(count, "ERROR", sheet, workbook)
            else:
                # add the sentimental score into excel
                add_senti_analysis(count, (((response.get("sentiment")).get("document")).get("score", "ERROR-0")), sheet, workbook)

                # add label
                add_label(count, (((response.get("sentiment")).get("document")).get("label", "ERROR-0")), sheet, workbook)

                # add the keywords
                i = 0
                keywords = ""
                while i < len(response.get("keywords")):
                    keywords += (response.get("keywords")[i]).get("text") + ","
                    i += 1
                add_keywords(count, keywords, sheet, workbook)
        except Exception as error:
            print("here2")
            # if anything goes wrong add error to all fields
            add_senti_analysis(count, "ERROR", sheet, workbook)
            add_keywords(count, "ERROR", sheet, workbook)


def add_senti_analysis(count, data, worksheet, book):

    worksheet['E'+str(count)] = data

    book.save(raw_excelfile)


def add_label(count, data, worksheet, book):

    worksheet['F'+str(count)] = data

    book.save(raw_excelfile)


def add_keywords(count, data, worksheet, book):

    worksheet['G'+str(count)] = data

    book.save(raw_excelfile)


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
raw_folder = os.path.join(THIS_FOLDER, 'raw_excelfiles')
raw_excelfile = os.path.join(raw_folder, 'bunsen-burger_reviews.xlsx')
# making data frame from csv file
dataframe = pd.read_excel(raw_excelfile)
# retrieving just the comments.
rows = dataframe['Comment']

analyse_comments(rows)

