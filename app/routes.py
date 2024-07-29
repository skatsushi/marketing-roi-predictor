from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager, bq_client
from app.models import User
from app.forms import LoginForm
from app.services import load_model_cloud, save_prediction_to_bq
import pandas as pd

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    """Handles the prediction request."""
    model = load_model_cloud()
    try:
        input_data = {
            'index': request.form['index'],
            'EMAIL': request.form['EMAIL'],
            'SEARCH_ENGINE': request.form['SEARCH_ENGINE'],
            'SOCIAL_MEDIA': request.form['SOCIAL_MEDIA'],
            'VIDEO': request.form['VIDEO']
        }

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])

        # Predict
        y_predictions = model.predict(input_df)

        # Save prediction to BigQuery
        save_prediction_to_bq(current_user.get_id(), input_data, y_predictions.tolist()[0])

        # Render template with prediction result
        return render_template('index.html', prediction_text='Predicted ROI: {}'.format(y_predictions[0]))

    except Exception as e:
        return render_template('index.html', prediction_text='Error: {}'.format(str(e)))

@app.route('/history')
@login_required
def history():
    query = f"""
    SELECT * FROM `skatsushi.marketing_data.prediction_history`
    WHERE user_id = '{current_user.get_id()}'
    ORDER BY timestamp DESC
    """
    query_job = bq_client.query(query)
    history = query_job.result()
    return render_template('history.html', history=history)



