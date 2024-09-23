# Set Flask app
$env:FLASK_APP = "core.server:app"

# Run server using gunicorn
# python -m gunicorn -c gunicorn_config.py core.server:app
# python -c "from waitress import serve; from core.server import app; serve(app, host='0.0.0.0', port=8080)"
# Run Flask development server
python -m flask run --host=0.0.0.0 --port=8080