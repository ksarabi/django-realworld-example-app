python manage.py makemigrations && python manage.py migrate
export DEBUG_MODE=False && python manage.py runserver 0.0.0.0:7000
# export DEBUG_MODE=True && python runserver 0.0.0.0:7000 --noreload --nothreading