#### **RVM Deposit \& Rewards API**

This project provides a backend solution for a Reverse Vending Machine (RVM) system. It allows users to register, log their recyclable deposits (Plastic, Metal, Glass), and automatically earn reward points based on the material type and weight.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
##### **\*\*🛠 Setup \& Installation\*\***
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

1.Environment: Create a virtual environment and install the required dependencies:

Bash

python -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate

pip install -r requirements.txt



2.Database: Run migrations to set up the SQLite database:

Bash

python manage.py migrate



3.Superuser: Create an admin account to access the dashboard:

Bash

python manage.py createsuperuser



4.Run: Start the development server:

Bash

python manage.py runserver





**NOTE: To access the management dashboard:**

1.Once the server is running, navigate to http://127.0.0.1:8000/admin/ in your web browser, add ”/admin/” to the end of your URL to get there.



2.Log in using the superuser credentials you created in the previous step to manage deposits and view user tokens.



&nbsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
##### **\*\*Project Architecture\*\***
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Data Models**

•	User: Standard Django User model for handling authentication and associating deposits with specific individuals.

•	Deposit: Stores the core recycling data. I included a machine\_id to track which RVM submitted the data and a points\_earned field to store the reward value permanently at the time of the transaction.



**Business Logic**

The reward calculation is handled automatically within the Deposit model's save() method. 

This ensures that whether a deposit is created via the API or manually via the Admin panel, the points are always calculated correctly:

•	Plastic: 1 pt/kg

•	Metal: 3 pts/kg

•	Glass: 2 pts/kg

**API Endpoints:** 



**Endpoint	      Method	   Description**

/api/register/	 POST	   Create a new account

/api/login/	         POST	   Get an Auth Token

/api/deposit/	 POST	   Log a new recycling deposit

/api/summary/	 GET	   View total weight and points



***Sample Deposit Request (POST) From the RVM for example:***



Header: Authorization: Token <your\_token\_here>

JSON

{

&nbsp;   "material\_type": "METAL",

&nbsp;   "weight": 5.0,

&nbsp;   "machine\_id": "RVM\_NYC\_001"

}



***Sample Summary Response (GET)***

JSON

{

&nbsp;   "username": "coder123",

&nbsp;   "total\_recycled\_weight": 12.5,

&nbsp;   "total\_points\_earned": 28.0

}

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

##### **\*\*Tech Stack \& Abbreviations\*\***

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

•	Django

•	DRF: Django REST Framework (Used for building the API).

•	ORM: Object-Relational Mapper 

•	Token Auth: A stateless security method where a string (token) represents the user's session.



