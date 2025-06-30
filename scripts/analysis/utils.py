import scipy.stats as stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import polars as pl
from matplotlib.ticker import FuncFormatter
from IPython.display import display
from itertools import combinations
pd.set_option('display.max_columns', 200)
import warnings
warnings.filterwarnings('ignore')
import re


def check_null(df, check_individual=False):
    null_count = df.isnull().sum()
    null_percentage = (df.isnull().mean() * 100).round(2)

    print("Null value report by column:\n")
    
    null_report = pd.DataFrame({
        'Total': null_count,
        'Percentage (%)': null_percentage
    })

    null_report_filtered = null_report[null_report['Total'] > 0]

    if not null_report_filtered.empty:
        columns_with_nulls = null_report_filtered.index.tolist()
        print("List of columns with null values:", columns_with_nulls)
       
        print("\nColumns with null values:")
        display(null_report_filtered)
        
        if check_individual:
            for column in columns_with_nulls:
                print(f"\nNull values in column '{column}':")
                display(df[df[column].isnull()])
        else:
            print("\nIndividual check option ignored.")
    else:
        print("No null values found in the DataFrame!")


def check_types(df):
    print("\nChecking data types by column:\n")
    display(df.dtypes)  

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if numeric_columns:
        print("\nColumns with numeric values:")
        print(numeric_columns)

        for column in numeric_columns:
            if df[column].apply(lambda x: not pd.api.types.is_number(x) and pd.notna(x)).any():
                print(f"\nWarning: Column '{column}' contains non-numeric values.")
            else:
                print(f"\nColumn '{column}' contains only valid numeric values.")
    else:
        print("\nNo numeric columns found.")
    
    non_numeric_columns = df.select_dtypes(exclude=['int64', 'float64']).columns.tolist()
    
    if non_numeric_columns:
        print("\nColumns with non-numeric values:")
        print(non_numeric_columns)
        
        for column in non_numeric_columns:
            print(f"\nSample values from column '{column}':")
            display(df[column].head())
    else:
        print("\nNo non-numeric columns found.")


def check_anomalies(df):
    total_columns = len(df.columns)
    valid_columns = 0
    anomaly_columns = []

    print("\nChecking columns for anomalies...\n")

    for column in df.columns:
        col_type = df[column].dtype
        unique_values = df[column].nunique()

        if col_type in ['int64', 'float64']:
            if df[column].apply(lambda x: not pd.api.types.is_number(x) and pd.notna(x)).any():
                anomaly_columns.append((column, "Contains non-numeric values"))
            elif unique_values == 1:
                anomaly_columns.append((column, "All values are the same"))
            else:
                valid_columns += 1
        else:
            if unique_values == 1:
                anomaly_columns.append((column, "All values are the same"))
            else:
                valid_columns += 1

    if anomaly_columns:
        print("\nColumns with detected anomalies:")
        for col_name, issue in anomaly_columns:
            print(f" - Column '{col_name}': {issue}")
            display(df[col_name].head()) 
    else:
        print("No anomalies found in the columns.")

    print(f"\nTotal columns that are OK: {valid_columns} out of {total_columns}")


def check_groupby(df, plot_graph=False, len_combination=2):
    group_columns = df.select_dtypes(exclude=['int64', 'float64']).columns.tolist()
    
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    if not group_columns:
        print("No categorical column identified for grouping.")
        return
    
    print(f"\nCategorical columns for grouping: {group_columns}")

    all_combinations = []
    for r in range(1, len(group_columns) + 1):
        comb = combinations(group_columns, r)
        all_combinations.extend(comb)

    for combination in all_combinations:
        if len(combination) <= len_combination:        
            combo_str = ', '.join(combination)
            print(f"\nCount of grouped elements by {combo_str}:")
            grouped_counts = df.groupby(list(combination)).size().reset_index(name='Total')
            display(grouped_counts)

            if plot_graph:
                ploting_graph(combination, grouped_counts)

    if not numeric_columns:
        print("\nNo numeric column identified for analysis.")
    else:
        for col in numeric_columns:
            print(f"\nDescriptive statistics for '{col}':")
            display(df[col].describe())


def groupby_columns(df, group_columns, plot_graph=False, len_combination=2):
    group_columns = [col.strip() for col in group_columns]
    missing_cols = [col for col in group_columns if col not in df.columns]
    if missing_cols:
        print(f"The following columns are not present in the DataFrame: {missing_cols}")
        return
    
    print(f"\nCategorical columns for grouping: {group_columns}")

    all_combinations = []
    for r in range(1, len(group_columns) + 1):
        comb = combinations(group_columns, r)
        all_combinations.extend(comb)

    for combination in all_combinations:
        if len(combination) <= len_combination:
            combo_str = ', '.join(combination)
            print(f"\nCount of grouped elements by {combo_str}:")
            grouped_counts = df.groupby(list(combination)).size().reset_index(name='Total')
            display(grouped_counts)

            if plot_graph:
                ploting_graph(combination, grouped_counts)


def format_func(value, tick_number):
    return f'{int(value):,}'


def format_combination(combination):
    if len(combination) == 0:
        return ""
    elif len(combination) == 1:
        return combination[0]
    elif len(combination) == 2:
        return f"{combination[0]} and {combination[1]}"
    else:
        return f"{', '.join(combination[:-1])} and {combination[-1]}"


def ploting_graph(combination, grouped_counts):
    combination_str = format_combination(combination)
    combination_legend = ' - '.join(combination)

    plt.figure(figsize=(10, 6))

    plot_data = grouped_counts.copy()

    if len(combination) == 1:
        col = combination[0]
        plot_data['Combination'] = plot_data[col].astype(str)
    else:
        plot_data['Combination'] = plot_data[list(combination)].apply(
            lambda row: ' - '.join(row.values.astype(str)), axis=1
        )

    sns.barplot(x='Combination', y='Total', data=plot_data)

    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

    plt.title(f'Grouped count by {combination_str}')
    plt.xticks(rotation=45)
    plt.ylabel('Total')
    plt.xlabel(combination_legend)
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    print('This file was created to be imported')
