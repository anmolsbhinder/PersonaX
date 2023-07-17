from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

criteria = pd.read_csv('/database/criteria.csv')
Scriterias = pd.read_csv('/database/segment_master.csv')


@app.route('/api/segmentpg', methods=['GET'])
def get_segments_criterias():

    df2 = pd.DataFrame(Scriterias)
    segmentlist = df2['Segment Name'].tolist()

    return jsonify(segmentlist) , 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(port=5000)
