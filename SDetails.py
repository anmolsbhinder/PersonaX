from flask import Flask, jsonify
import pandas as pd
import json

app = Flask(__name__)

# segment_stats = pd.read_csv('/Users/a0s16cp/PycharmProjects/PersonaX/segment_stats.csv')
segment_stats = pd.DataFrame(columns=['CustomerID', 'TotalRevenue', 'TotalInvoices', 'ReturnedItems', 'BoughtItems','Segment'])
criteria = pd.read_csv('/database/criteria.csv')

# type='BigSpender'
# count=10

@app.route('/api/segmentprofile/<string:type>/<int:count>', methods=['GET'])
def get_segment_details(type, count):
    global segment_stats
    # Retrieve customers from the tables based on the type
    customerlist = pd.read_csv(f'/Users/a0s16cp/PycharmProjects/PersonaX/{type}_Scores.csv')
    customerlist = customerlist.head(count)
    table1_json = customerlist.to_dict(orient='records')



    filtered_table = criteria.iloc[:, 0:5]
    filtered_table = filtered_table[filtered_table['CustomerID'].isin(customerlist['CustomerID'])]
    summed_row = filtered_table.sum()
    summed_row['Segment'] = f'{type}'
    segment_stats = pd.concat([segment_stats, summed_row.to_frame().T], ignore_index=True)
    # segment_stats = pd.DataFrame(filtered_table)
    # print(segment_stats)


    # # Remove the first column
    segment_stats = segment_stats.iloc[:, 1:]

    # Move the last column to the first position
    last_column = segment_stats.columns[-1]
    segment_stats = segment_stats[[last_column] + list(segment_stats.columns[:-1])]

    segment_stats['AvgBasketSize'] = segment_stats['BoughtItems'] / segment_stats['TotalInvoices']
    segment_stats['AvgSubtotal'] = segment_stats['TotalRevenue'] / segment_stats['TotalInvoices']
    segment_stats['AvgItemCost'] = segment_stats['TotalRevenue'] / segment_stats['BoughtItems']
    # segment_stats = segment_stats[segment_stats['Segment'] == type]

    table2_json = segment_stats.to_dict(orient='records')

    Scriterias = pd.read_csv('/database/segment_master.csv')
    Scriterias= Scriterias[Scriterias['Segment Name'] == type]
    table3_json = Scriterias.to_dict(orient='records')

    response = {
        'customerlist': table1_json,
        'segment_stats': table2_json,
        'criteria_vector': table3_json
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5000)
