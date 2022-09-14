export DJANGO_SETTINGS_MODULE='codeteamtask.settings'
pip3 install -r dependencies.txt
python3 manage.py makemigrations
python3 manage.py migrate
sh run.sh