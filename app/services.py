from google.cloud import storage, bigquery
import joblib
from datetime import datetime

def load_model_cloud():
    storage_client = storage.Client()
    bucket_name = "skatsushi-mlops"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob("advertising_roi/artifact/model.joblib")
    blob.download_to_filename("model.joblib")
    model = joblib.load("model.joblib")
    return model


def save_prediction_to_bq(user_id, input_data, predicted_output):
    bq_client = bigquery.Client()
    table_id = "skatsushi.marketing_data.prediction_history"
    
    # 現在のタイムスタンプを追加
    current_time = datetime.utcnow().isoformat()
    
    rows_to_insert = [{
        'user_id': user_id,
        'input_data': input_data,
        'predicted_output': predicted_output,
        'timestamp': current_time  # タイムスタンプフィールドを追加
    }]
    
    errors = bq_client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        raise Exception(f"BigQuery insert error: {errors}")
        




