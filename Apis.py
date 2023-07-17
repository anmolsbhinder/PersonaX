from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

from main import create_new_score

app = Flask(__name__)
CORS(app)

@app.route('/api/customerprofile/<customer_id>', methods=['GET'])
def get_customer_details(customer_id):
    criteria = pd.read_csv('criteria.csv')
    criteria_scores = pd.read_csv('criteria_scores.csv')
    segment_scores = pd.read_csv('segment_scores.csv')

    customer_id = float(customer_id)
    # Retrieve data from the tables based on the CustomerID
    criteria_data = criteria[criteria['CustomerID'] == customer_id]
    table1_json = criteria_data.to_dict(orient='records')

    criteria_score_data = criteria_scores[criteria_scores['CustomerID'] == customer_id]
    criteria_score_data = criteria_score_data.drop("CustomerID", axis=1)
    table2_json = criteria_score_data.to_dict(orient='records')

    segment_score_data = segment_scores[segment_scores['CustomerID'] == customer_id]
    segment_score_data = segment_score_data.drop("CustomerID", axis=1)
    table3_json = segment_score_data.to_dict(orient='records')

    response = {
        'criteria': table1_json,
        'criteria_scores': table2_json,
        'segment_scores': table3_json
    }

    return jsonify(response)

    # Merge the data from the tables
    # merged_data = pd.merge(criteria_data, criteria_score_data, on='CustomerID', how='inner')
    # merged_data = pd.merge(merged_data, segment_score_data, on='CustomerID', how='inner')

    # Convert the merged data to JSON
    # json_data = merged_data.to_dict(orient='records')

    # Return the JSON response
    # return jsonify(json_data), 200, {'Content-Type': 'application/json'}


@app.route('/api/segmentprofile/<string:type>/<int:count>', methods=['GET'])
def get_segment_details(type, count):
    criteria = pd.read_csv('criteria.csv')

    segment_stats = pd.DataFrame(
        columns=['CustomerID', 'TotalRevenue', 'TotalInvoices', 'ReturnedItems', 'BoughtItems', 'Segment'])

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

    segment_master = pd.read_csv('segment_master.csv')
    segment_master= segment_master[segment_master['Segment Name'] == type]
    table3_json = segment_master.to_dict(orient='records')

    response = {
        'customerlist': table1_json,
        'segment_stats': table2_json,
        'criteria_vector': table3_json
    }

    return jsonify(response)


@app.route('/api/createsegment/<string:type>/<int:count>/<values>', methods=['GET'])
def create_segment(type, count, values):
    criteria = pd.read_csv('criteria.csv')
    criteria_scores = pd.read_csv('criteria_scores.csv')
    segment_scores = pd.read_csv('segment_scores.csv')

    # criteria_vector = request.args.getlist('values')
    criteria_vector = list(map(int, values.split(',')))
    segment_scores = create_new_score(criteria_scores, segment_scores, criteria_vector, type)
    segment_scores.to_csv('segment_scores.csv', index=False)

    return get_segment_details(type,count);

    # segment_stats = pd.DataFrame(
    #     columns=['CustomerID', 'TotalRevenue', 'TotalInvoices', 'ReturnedItems', 'BoughtItems', 'Segment'])
    #
    # # Retrieve customers from the tables based on the type
    # customerlist = pd.read_csv(f'/Users/a0s16cp/PycharmProjects/PersonaX/{type}_Scores.csv')
    # customerlist = customerlist.head(count)
    # table1_json = customerlist.to_dict(orient='records')
    #
    # filtered_table = criteria.iloc[:, 0:5]
    # filtered_table = filtered_table[filtered_table['CustomerID'].isin(customerlist['CustomerID'])]
    # summed_row = filtered_table.sum()
    # summed_row['Segment'] = f'{type}'
    # segment_stats = pd.concat([segment_stats, summed_row.to_frame().T], ignore_index=True)
    # # segment_stats = pd.DataFrame(filtered_table)
    # # print(segment_stats)
    #
    #
    # # # Remove the first column
    # segment_stats = segment_stats.iloc[:, 1:]
    #
    # # Move the last column to the first position
    # last_column = segment_stats.columns[-1]
    # segment_stats = segment_stats[[last_column] + list(segment_stats.columns[:-1])]
    #
    # segment_stats['AvgBasketSize'] = segment_stats['BoughtItems'] / segment_stats['TotalInvoices']
    # segment_stats['AvgSubtotal'] = segment_stats['TotalRevenue'] / segment_stats['TotalInvoices']
    # segment_stats['AvgItemCost'] = segment_stats['TotalRevenue'] / segment_stats['BoughtItems']
    # # segment_stats = segment_stats[segment_stats['Segment'] == type]
    #
    # table2_json = segment_stats.to_dict(orient='records')
    #
    # segment_master = pd.read_csv('segment_master.csv')
    # segment_master = segment_master[segment_master['Segment Name'] == type]
    # table3_json = segment_master.to_dict(orient='records')
    #
    # response = {
    #     'customerlist': table1_json,
    #     'segment_stats': table2_json,
    #     'criteria_vector': table3_json
    # }
    #
    # return jsonify(response)


@app.route('/api/segmentpg', methods=['GET'])
def get_segments_criterias():

    segment_stats = pd.DataFrame(
        columns=['CustomerID', 'TotalRevenue', 'TotalInvoices', 'ReturnedItems', 'BoughtItems', 'Segment'])

    segment_master = pd.read_csv('segment_master.csv')
    df2 = pd.DataFrame(segment_master)
    segmentlist = df2['Segment Name'].tolist()

    return jsonify(segmentlist) , 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(port=5000)
