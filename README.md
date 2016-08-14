# Accounts/Payments Web Service
This service implements very basic accounts logic as well as payment transactions
It allows storage of user accounts with their preferred currencies. Payments
automatically make currency conversion to appropriately load the funds.

Note:
Using Python 3.4

## Quickstart:

This will create a virtual environment, install dependencies, and populate it with test data:

```bash
$ virtualenv venv -p /usr/bin/python3  #  create virtual environment
$ source venv/bin/activate             #  activate virtual environment
$ pip install -r requirements.txt      #  install requirements
$ DJANGO_SETTINGS_MODULE=coins_test.settings python manage.py runserver  # run development server
```


Run Tests:
```bash
$ DJANGO_SETTINGS_MODULE=coins_test.settings python manage.py test
```

## API docs

API documentation can be found [here](apiary.apib).
