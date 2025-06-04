git clone <your-repo-url>
cd fitness_booking
python -m venv venv
source venv/bin/activate   # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py seed
python manage.py runserver
