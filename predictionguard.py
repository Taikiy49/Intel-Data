from predictionguard import PGClient

client = PGClient(
    project_id='project_id',
    api_key='31d39487230046f9b9b0549bb6549191',
    timeout=5.0
)

# Make a prediction
prediction = client.predict(features)

# Report the prediction outcome
client.report(prediction_id=prediction['id'], label=1)
