export DJANGO_SETTINGS_MODULE='codeteamtask.settings'
pip install -r dependencies.txt
python3 manage.py makemigrations
python3 manage.py migrate
sh run.sh