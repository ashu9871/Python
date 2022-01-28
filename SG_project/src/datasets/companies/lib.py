import numpy as np

def get_df_columns(df, columns_list):
	new_df = df[columns_list]
	return new_df


def get_df_column_val(df, column_name, value):
	new_df = df[df[column_name] == value]
	return new_df


def get_quarter_column(df):
	conditions = [
		(df['month'].isin([1,2,3])),
		(df['month'].isin([4,5,6])),
		(df['month'].isin([7,8,9])),
		(df['month'].isin([10,11,12]))
	]
	choices = ['Q1', 'Q2', 'Q3', 'Q4']
	df['Quarter'] = np.select(conditions, choices, default='Q1')
	return df


def groupby_quarter(df):
	column_list = [
		'U3_Company_Number', 
		 'year', 
		'Quarter'
	]
	total_months = range(1,13)

	df_grouped = df.groupby(column_list).agg({
		'1_month': [
			'mean', 'var'
		],
		'3_month': [
			'mean', 'var'
		],
		'6_month': [
			'mean', 'var'
		], 
		'12_month': [
			'mean', 'var'
		],
		'24_month': [
			'mean', 'var'
		],
		'36_month': [
			'mean', 'var'
		],
		'60_month': [
			'mean', 'var'
		]
	})
	return df_grouped


def groupby_year(df):
	column_list = [
		'U3_Company_Number', 
		'year', 
	]
	total_months = range(1,13)

	df_grouped = df.groupby(column_list).agg({
		'1_month': [
			'mean', 'var'
		],
		'3_month': [
			'mean', 'var'
		],
		'6_month': [
			'mean', 'var'
		], 
		'12_month': [
			'mean', 'var'
		],
		'24_month': [
			'mean', 'var'
		],
		'36_month': [
			'mean', 'var'
		],
		'60_month': [
			'mean', 'var'
		]
	})
	return df_grouped


def find_gap_months(df):
	column_list = [
		'U3_Company_Number', 
		'year' 
	]
	total_months = range(1,13)

	df_gaps = df.groupby(column_list).agg({
		'month': [
			'count', 
			lambda x: list(set(total_months)-set(list(x)))
		],
		'Company_Name': 'first',
		'Country_Domicile': 'first',
		'Ticker': 'first',
		'BICS_Sector': 'first'
	})
	return df_gaps


def incomplete_year(df):
	column_list = [
		'U3_Company_Number', 
		'year' 
	]
	df_year = df.groupby(column_list).agg({
		'month': [
			'min',
			'max',
			'count'
		],
		'Company_Name': 'first',
		'Country_Domicile': 'first',
		'Ticker': 'first',
		'BICS_Sector': 'first'
	})

	index_names = df_year[
		(
			(df_year['month']['min'] != 1) | 
			(df_year['month']['max'] != 12)
		) | 
		(
			(df_year['month']['min'] != 1) & 
			(df_year['month']['max'] != 12)
		)
	].index

	df_year.drop(index_names, inplace = True)

	return df_year


def incomplete_quarter(df):
	get_quarter_column(df)
	column_list = [
		'U3_Company_Number', 
		'year',
		'Quarter'
	]
	df_quart = df.groupby(column_list).agg({
		'month': [
			'min',
			'max',
			'count'
		],
		'Company_Name': 'first',
		'Country_Domicile': 'first',
		'Ticker': 'first',
		'BICS_Sector': 'first'
	})
	
	index_names = df_quart[ 
		(
			(df_quart.index.get_level_values('Quarter') == 'Q1') & 
			(
				(df_quart['month']['min'] != 1) | 
				(df_quart['month']['max'] != 3)
			)
		) | 
		(
			(df_quart.index.get_level_values('Quarter') == 'Q2') & 
			(
				(df_quart['month']['min'] != 4) | 
				(df_quart['month']['max'] != 6)
			)
		) | 
		(
			(df_quart.index.get_level_values('Quarter') == 'Q3') & 
			(
				(df_quart['month']['min'] != 7) | 
				(df_quart['month']['max'] != 9)
			)
		) | 
		(
			(df_quart.index.get_level_values('Quarter') == 'Q4') & 
			(
				(df_quart['month']['min'] != 10) | 
				(df_quart['month']['max'] != 12)
			)
		)
	].index
	
	df_quart.drop(index_names, inplace = True)

	return df_quart
