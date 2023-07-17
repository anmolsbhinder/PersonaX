import pandas as pd
raw_data = pd.read_csv('/Users/a0s16cp/PycharmProjects/PersonaX/UCI invoice data/online_retail_09_10.csv')

#TRANSACTIONS

raw_data['Total'] = raw_data['Quantity'] * raw_data['UnitPrice']
transactions = raw_data[['InvoiceNo','CustomerID','Total','Quantity','Date']]
transactions= transactions.groupby(['InvoiceNo', 'CustomerID', 'Date']).agg(SubTotal=('Total', 'sum'), BasketSize=('Quantity','sum')).reset_index()
transactions['Date'] = pd.to_datetime(transactions['Date'])
transactions.to_csv('transactions.csv', index=False)





#CRITERIAS

criteria = transactions
criteria['Count'] = 1
criteria = transactions.groupby(['CustomerID']).agg(TotalRevenue=('SubTotal', 'sum'), TotalInvoices=('Count','sum')).reset_index()

returns = transactions[transactions['BasketSize'] < 0].groupby(['CustomerID']).agg(ReturnedItems=('BasketSize', 'sum')).reset_index()
# Merge the tables based on the customer ID column
criteria = pd.merge(criteria, returns[['CustomerID', 'ReturnedItems']], on='CustomerID', how='left')
# Replace NaN values with 0 for TotalReturns column
criteria['ReturnedItems'] = criteria['ReturnedItems'].fillna(0)
criteria['ReturnedItems'] = criteria['ReturnedItems'].abs()

buys = transactions[transactions['BasketSize'] > 0].groupby(['CustomerID']).agg(BoughtItems=('BasketSize', 'sum')).reset_index()
criteria = pd.merge(criteria, buys[['CustomerID', 'BoughtItems']], on='CustomerID', how='left')
criteria['BoughtItems'] = criteria['BoughtItems'].fillna(0)

# Removing garbage values
criteria = criteria[(criteria['BoughtItems'] >= criteria['ReturnedItems']) & (criteria['TotalRevenue']>=0)]

# criteria= criteria.loc[criteria['BoughtItems'] < criteria['ReturnedItems']]

criteria['AvgBasketSize'] = criteria['BoughtItems']/criteria['TotalInvoices']
criteria['AvgSubtotal'] = criteria['TotalRevenue']/criteria['TotalInvoices']
criteria['AvgItemCost'] = criteria['TotalRevenue']/criteria['BoughtItems']

most_recent_dates = transactions.groupby('CustomerID')['Date'].max().reset_index()
criteria = pd.merge(criteria, most_recent_dates, on='CustomerID', how='left')
criteria = criteria.rename(columns={'Date': 'RecentPurDate'})
criteria.to_csv('criteria.csv', index=False)





#CRITERIA SCORES

columns_to_process = ['TotalRevenue', 'TotalInvoices', 'ReturnedItems', 'BoughtItems',
                      'AvgBasketSize', 'AvgSubtotal', 'AvgItemCost', 'RecentPurDate']

criteria_scores = pd.DataFrame(columns=['CustomerID'])

for column in columns_to_process:
    # Create a new DataFrame with 'CustomerID' and the current column
    new_table = criteria[['CustomerID', column]].copy()

    # Sort the new table by the column values in descending order
    new_table = new_table.sort_values(by=column, ascending=False)

    # Calculate the score based on the percentile rank of each row
    new_table[f'Score_{column}'] = new_table[column].rank(pct=True)
    new_table[f'Score_{column}'] = new_table[f'Score_{column}']*100
    new_table.to_csv(f"{column}_Score.csv", index=False)
    # Merge the new table with the score_table on 'CustomerID'
    criteria_scores = pd.merge(criteria_scores, new_table[['CustomerID', f'Score_{column}']], on='CustomerID', how='outer')

criteria_scores.to_csv('criteria_scores.csv', index=False)





#SEGMENT SCORES

segment_scores = pd.DataFrame(columns=['CustomerID'])

# segement_master = pd.DataFrame(columns=['Segment Name', 'Criteria Array'])
# segement_master.to_csv('segment_master.csv', index=False)

def calculate_scores(criteria_scores, segment_scores, criteria_vector, type):
    temp = criteria_scores.copy()

    Scriterias = pd.read_csv('/database/segment_master.csv')
    row = {'Segment Name': type, 'Criteria Array': criteria_vector}
    # print(row)
    Scriterias.loc[len(Scriterias)] = row
    Scriterias.to_csv('segment_master.csv', index=False)

    for index in criteria_vector:
        if index < 0:
            temp.iloc[:, abs(index)] = 100 - temp.iloc[:, abs(index)]

    criteria_vector = [abs(value) for value in criteria_vector]
    scores = temp.iloc[:, criteria_vector].mean(axis=1)
    scores = pd.DataFrame({'CustomerID': criteria_scores['CustomerID'], f'{type}Score': scores})
    segment_scores = pd.merge(segment_scores, scores[['CustomerID', f'{type}Score']], on='CustomerID', how='outer')
    # print(segment_scores)
    scores = scores.sort_values(by=f'{type}Score', ascending=False)

    scores.to_csv(f'{type}_Scores.csv', index=False)
    return segment_scores

def calculate_s(criteria_scores, segment_scores, criteria_vector, type):
    temp = criteria_scores.copy()

    for index in criteria_vector:
        if index < 0:
            temp.iloc[:, abs(index)] = 100 - temp.iloc[:, abs(index)]

    criteria_vector = [abs(value) for value in criteria_vector]
    scores = temp.iloc[:, criteria_vector].mean(axis=1)
    scores = pd.DataFrame({'CustomerID': criteria_scores['CustomerID'], f'{type}Score': scores})
    segment_scores = pd.merge(segment_scores, scores[['CustomerID', f'{type}Score']], on='CustomerID', how='outer')
    # print(segment_scores)
    scores = scores.sort_values(by=f'{type}Score', ascending=False)

    scores.to_csv(f'{type}_Scores.csv', index=False)
    return segment_scores

def run_calculate_scores_for_all_segments(segment_scores):
    segment_master = pd.read_csv('/database/segment_master.csv')
    criteria_scores = pd.read_csv('/database/criteria_scores.csv')

    for _, row in segment_master.iterrows():
        type = row['Segment Name']
        criteria_vector = eval(row['Criteria Array'])

        segment_scores = calculate_s(criteria_scores, segment_scores, criteria_vector, type)

    segment_scores.to_csv('segment_scores.csv', index=False)


# Call the function to run the calculations for all segments
run_calculate_scores_for_all_segments(segment_scores)



