import pandas as pd
import numpy as np
from src.datasets.pds import sg as service_sg
from src.datasets.companies import lib as service_lib
from src.datasets.pds import plot as service_plot


df_comp_info = pd.read_excel('src/datasets/companies/Company Information_20190630.xlsm')
df_pd_info = pd.read_excel('src/datasets/pds/cri_pds.xlsm', skiprows=[0,1,2], header=0)

df_all_info = service_sg.get_company_and_pd_data_single(df_comp_info, df_pd_info)
# df_all_info = pd.read_csv('SG_Company_PD_Data.csv')

df_gap_info = service_lib.find_gap_months(df_all_info)
# df_gap_info.to_csv('Gap_data.csv')

df_incomplete_year_info = service_lib.incomplete_year(df_all_info)
# df_incomplete_year_info.to_csv('Incomplete_year_data.csv')

df_incomplete_quarter_info = service_lib.incomplete_quarter(df_all_info)
# df_incomplete_quarter_info.to_csv('Incomplete_quarter_data.csv')


service_plot.plot_yearly(df_all_info, 'mean', '60_month')
service_plot.plot_quarterly(df_all_info, 'mean', '60_month')