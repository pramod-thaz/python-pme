
import pandas as pd
import numpy as np
import math
from irr import series_xirr

def pme_calc(df, end_date):
    cf = df['cash_flow']
    nav = df['nav']
    bench = df['bench']

    combined_cf = cf.where(cf.index <= end_date, 0) + nav.where(nav.index == end_date, 0)

    irr = series_xirr(combined_cf[:end_date].fillna(0))
    tvpi = -1 * combined_cf.where(combined_cf.values >= 0, 0).sum() / combined_cf.where(combined_cf.values < 0, 0).sum()
    dpi = -1 * cf.where(cf.values >= 0, 0).sum() / cf.where(cf.values < 0, 0).sum()
    
    fvfactor = bench[end_date] / bench
    fvcf = (combined_cf * fvfactor) 

    dva = fvcf.sum()
    pme = -1 * fvcf.where(fvcf.values >= 0, 0).sum() / fvcf.where(fvcf.values < 0, 0).sum()
    alpha = math.log(1 + series_xirr(fvcf[:end_date].fillna(0)))
    bench_irr = math.exp(math.log(1 + irr) - alpha) - 1

    return {
                'irr': irr, 
                'tvpi': tvpi, 
                'dpi': dpi, 
                'dva': dva, 
                'pme': pme, 
                'alpha': alpha, 
                'bench_irr': bench_irr
            }