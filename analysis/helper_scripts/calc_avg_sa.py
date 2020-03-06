import os
import pandas as pd


def calc_avg_sa(filename):
    # read form excel as dataframe
    THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    my_excelfile = os.path.join(THIS_FOLDER, 'excelfiles/' + filename)
    df = pd.read_excel(my_excelfile, sheet_name='Sheet1')
    # no need to display no.of reviews, so drop it
    del df['Number of Reviews']
    # Remove rows with 'Error'
    df = df[~df.Label.str.contains("ERROR")]

    # get the avg SA score
    sa = round(df["SA"].mean() * 100, 2)
    return sa
