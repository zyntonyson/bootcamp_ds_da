import pandas as pd
import argparse
import numpy as np
import uuid
import random
import os
from datetime import datetime, timedelta

parser=argparse.ArgumentParser(description='Generate Datasets for S10 DA')
parser.add_argument('dataset', nargs='*', default=[], help='Datasets created by this process')
parser.add_argument('-V','--verbose', action='store_true', help='Increase output verbosity')



def generar_fechas_aleatorias(start_date, end_date, n_dates=1):
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0, microsecond=0)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date).replace(hour=0, minute=0, second=0, microsecond=0)

    delta_seconds = int((end_date - start_date).total_seconds())
    

    segundos_aleatorios = np.random.choice(range(delta_seconds), n_dates)
    fechas = [start_date + timedelta(seconds=int(s)) for s in segundos_aleatorios]
    
    return fechas



# Dates
days_of_data=180
end_date= datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=days_of_data)).strftime("%Y-%m-%d")


if __name__ == '__main__':
    args, _ = parser.parse_known_args()

SEED_VALUE =42
rng = np.random.default_rng(SEED_VALUE)

current_dataset ='s_10_a_b_mean_test'

if len(args.dataset) == 0 or current_dataset in args.dataset:


    TREATMENTS = ['B','A']
    M_TREATMENTS = [1800,1600]
    S_TREATMENTS= [25,25]


    REPORT_FILENAME=os.path.join('datasets',current_dataset+'.csv')
    (
        pd.DataFrame(
            {'group':TREATMENTS, 'm':M_TREATMENTS,'sd':S_TREATMENTS, 'n_visits':rng.gamma(shape=20, scale=18, size=len(TREATMENTS)) }
        )
        .assign(
            n_visits = lambda df: df.n_visits.round().astype(int),
            amount = lambda df: df.apply(lambda x: rng.normal(size=int(x['n_visits']),loc=int(x['m']),scale=int(x['sd'])), axis=1).round(2)
        )
        .explode('amount')
        .assign(
            ts_visit = lambda df: generar_fechas_aleatorias(start_date=start_date,end_date=end_date,n_dates=df.shape[0]),
            uuid_user = lambda df: [str(uuid.uuid5(uuid.NAMESPACE_DNS,str(i+1))) for i in range(df.shape[0])]

        )
        .drop(columns=['m','n_visits','sd'])
        .to_csv(REPORT_FILENAME,index=False)
    )



current_dataset ='s_10_a_b_multiple_hypothesis'
if len(args.dataset) == 0 or current_dataset in args.dataset:

    TREATMENTS = ['MacOS','Android','IOS','Windows']
    P_TREATMENTS = np.random.choice([2,3,5,7,11,13],len(TREATMENTS))
    P_TREATMENTS=P_TREATMENTS/P_TREATMENTS.sum()


    REPORT_FILENAME=os.path.join('datasets',current_dataset+'.csv')
    (
        pd.DataFrame(
            {'device':TREATMENTS, 'p_convertion':P_TREATMENTS, 'n_visits':rng.gamma(shape=334, scale=289, size=len(TREATMENTS)) }
        )
        .assign(
            n_visits = lambda df: df.n_visits.round().astype(int),
            convertion = lambda df: df.apply(lambda x: rng.binomial(n=1,size=x['n_visits'],p=x['p_convertion']), axis=1)
        )
        .explode('convertion')
        .assign(
            ts_visit = lambda df: generar_fechas_aleatorias(start_date=start_date,end_date=end_date,n_dates=df.shape[0]),
            uuid_user = lambda df: [str(uuid.uuid5(uuid.NAMESPACE_DNS,str(i+1))) for i in range(df.shape[0])]

        )
        .drop(columns=['p_convertion','n_visits'])
        .to_csv(REPORT_FILENAME,index=False)
    )


