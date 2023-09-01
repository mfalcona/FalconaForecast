from flask import Flask, render_template
from google.cloud import storage
from google.cloud import bigquery

app = Flask(__name__)

@app.route('/')
def index():
    # Initialize BigQuery client
    client = bigquery.Client()

    # Query BigQuery data
    query = """
    SELECT * FROM `basic-cabinet-287500.falcona_forecast.forecast_ev_curr`
    """
    query_job = client.query(query)
    results = query_job.result()

    data = []
    for row in results:
        data.append(row)

    return render_template('index.html', data=data)

"""
if __name__ == '__main__':
    app.run(debug=True)
"""