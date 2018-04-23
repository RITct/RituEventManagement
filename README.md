# RituEventManagement

>**Disclaimer:** _This is a very quick prototype, there are bugs within the system. Use carefully and contribute to fix._

This is an app to manage registrations in any event.

Created during Ritu 2018 as an internal tool. 

## Features
* Centralized registrations.
* Supports multiple different departments.
* Multiple users per department.
* One super admin.

## Instalation

## Requirements
* Python 3.5 or above
* Django 2.0 oe above

## How to set up

1. Clone the repository.
2. Install requirements
    ```bash
    $ pip install -r requirements.txt
    ```
3. Set up database by editing the file `RituEventManagement/settings.py`.
    > By default using sqlite. This is recommended for small scale deployment due to ease of management and backup.
4. Run the following commands to initialize the application
    ```bash
    $ python3 manage.py init_db
    ```
    > The database is initialized using the data available in python file `event_details.py`. A sample is provided with the project, 
the same must be maintained.

5. Create event volunteer accounts
    ```sh
    $ python3 manage.py create_event_volunteers
    ```
6. Create registration desk user.
    ```sh
    $ python3 manage.py create_registration_desk
    ```
    > Repeat step 5 and 6 as much as needed.
  
  
  
  
