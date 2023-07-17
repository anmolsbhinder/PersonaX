from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

criteria = pd.read_csv('/database/criteria.csv')
criteria_scores = pd.read_csv('/database/criteria_scores.csv')
segment_scores = pd.read_csv('/database/segment_scores.csv')


@app.route('/api/customerprofile/<customer_id>', methods=['GET'])
def get_customer_details(customer_id):

    customer_id = float(customer_id)
    # Retrieve data from the tables based on the CustomerID
    criteria_data = criteria[criteria['CustomerID'] == customer_id]
    criteria_score_data = criteria_scores[criteria_scores['CustomerID'] == customer_id]
    segment_score_data = segment_scores[segment_scores['CustomerID'] == customer_id]

    # Merge the data from the tables
    merged_data = pd.merge(criteria_data, criteria_score_data, on='CustomerID', how='inner')
    merged_data = pd.merge(merged_data, segment_score_data, on='CustomerID', how='inner')

    # Convert the merged data to JSON
    json_data = merged_data.to_dict(orient='records')

    # Return the JSON response
    return jsonify(json_data) , 200, {'Content-Type': 'application/json'}





if __name__ == '__main__':
    app.run(port=5000)
