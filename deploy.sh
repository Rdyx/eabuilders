# Make sure you're in the root folder before starting script
. venv/bin/activate
python manage.py collectstatic --no-input
gcloud app deploy
