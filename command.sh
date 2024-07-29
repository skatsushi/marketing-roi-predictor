docker build -t flask-app .


docker tag flask-app gcr.io/skatsushi/flask-app



docker push gcr.io/skatsushi/flask-app



gcloud run deploy roi-model-flask \
    --image gcr.io/skatsushi/flask-app \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated