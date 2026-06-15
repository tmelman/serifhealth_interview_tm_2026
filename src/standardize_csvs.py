import pandas as pd
import datetime as dt
 
def standardize_csvs():
    hpt_csv = "../data/hpt_extract_20250213.csv"
    tic_csv = "../data/tic_extract_20250213.csv"

    hpt = pd.read_csv(hpt_csv)
    tic = pd.read_csv(tic_csv)

    # standardize rates
    tic['date'] = tic['network_year_month'].apply(lambda x: dt.date(int(str(x)[:4]),int(str(x)[4:]),1)) # 1st day of month in absence of day
    hpt['date'] = hpt['last_updated_on'].apply(lambda x: dt.date(int(x.split('-')[0]),int(x.split('-')[1]),int(x.split('-')[2])))
    # standardize code
    hpt['code'] = hpt['raw_code'].apply(lambda x: int(x.split(' ')[-1]))
    # standardize payer names
    tic['payer'] = tic['payer'].str.lower().str.replace(' ','').str.split('-').apply(lambda x: x[0])
    hpt['payer'] = hpt['payer_name'].str.lower().str.replace(' ','')
    # extract ein from filename
    hpt['ein']=hpt['source_file_name'].apply(lambda x: int(x.split('_')[0].replace('-','')[:9]))
    # cut unnecessary columns out
    hpt = hpt.iloc[:,6:]
    # rate
    hpt'

    hpt.to_csv("../data/hpt_processed.csv")
    tic.to_csv("../data/tic_processed.csv")
    

