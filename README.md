# Django-authenication

This system contains authenication system with Django and DRF. 

## How to set up and run locally

1. Install [virtualenv](https://realpython.com/python-virtual-environments-a-primer/) based on python 3.8
2. Activate virtualenv
3. clone the repo and run

```bash
cd oxford-backend
pip install -r requirements.txt
```

4. If you want to run locally, run

```bash
python manage.py makemigration
python manage.py migrate
python manage.py runserver
```

## Database