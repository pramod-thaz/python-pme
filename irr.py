import pandas as pd
import numpy as np
from ErrorHandler import errorHandler

@errorHandler
def series_xirr(a, guess=0.00):
    '''Calculates XIRR from a series of cashflows with dates as index 
    '''

    amounts = a.values
    dates = a.index.values

    years = np.array(dates-dates[0], dtype='timedelta64[D]').astype(int)/365

    step = 0.05
    epsilon = 0.0001
    limit = 1000
    residual = 1

    #Test for direction of cashflows
    disc_val_1 = np.sum(amounts/((1+guess)**years))
    disc_val_2 = np.sum(amounts/((1.05+guess)**years))
    mul = 1 if disc_val_2 < disc_val_1 else -1
    #Calculate XIRR    
    for i in range(limit):
        prev_residual = residual
        residual = np.sum(amounts/((1+guess)**years))
        if abs(residual) > epsilon:
            if np.sign(residual) != np.sign(prev_residual):
                step /= 2
            guess = guess + step * np.sign(residual) * mul   
        else:
            return guess

@errorHandler
def df_xirr(df, guess=0.05, date_column = 'date', amount_column = 'amount'):
    '''Calculates XIRR from a series of cashflows. 
       Needs a dataframe with columns date and amount, customisable through parameters. 
       Requires Pandas, NumPy libraries'''

    #df = df.sort_values(by=date_column).reset_index(drop=True)
    df['years'] = df[date_column].apply(lambda x: (x-df[date_column][0]).days/365)
    step = 0.05
    epsilon = 0.0001
    limit = 1000
    residual = 1

    #Test for direction of cashflows
    disc_val_1 = df[[amount_column, 'years']].apply(
                lambda x: x[amount_column]/((1+guess)**x['years']), axis=1).sum()
    disc_val_2 = df[[amount_column, 'years']].apply(
                lambda x: x[amount_column]/((1.05+guess)**x['years']), axis=1).sum()
    mul = 1 if disc_val_2 < disc_val_1 else -1

    #Calculate XIRR    
    for i in range(limit):
        prev_residual = residual
        df['disc_val'] = df[[amount_column, 'years']].apply(
                lambda x: x[amount_column]/((1+guess)**x['years']), axis=1)
        residual = df['disc_val'].sum()
        if abs(residual) > epsilon:
            if np.sign(residual) != np.sign(prev_residual):
                step /= 2
            guess = guess + step * np.sign(residual) * mul   
        else:
            return guess
            
