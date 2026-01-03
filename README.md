**Drop Me: RVM Deposit & Rewards Ecosystem**

This project provides a scalable backend solution for a Recycling Vending Machine (RVM) system. 
It features a complete ecosystem where users register, interact with specific physical machines, and automatically manage rewards through a digital wallet.

**** Setup & Installation Environment: ****

Create a virtual environment and install the required dependencies:

Bash
python -m venv venv
source venv/bin/activate  

**On Windows:**

venv\Scripts\activate

pip install -r requirements.txt

Database: 
Run migrations to set up the SQLite database:

Bash

python manage.py migrate

Superuser: Create an admin account to access the dashboard:

Bash

python manage.py createsuperuser

Run: Start the development 

server:

Bash
python manage.py runserver


**Note:** To access the management dashboard, navigate to http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

### *** Project Architecture ***  

The system is designed as a Real-World Ecosystem, ensuring data normalization and scalability.

--Entity-Relationship Diagram--

The following schema visualizes the relationships between users, their reward wallets, physical hardware locations, and recycling activity.
Data Models

•User: Handles authentication and secure session management.

•RVM (Machine): Represents physical hardware. Tracks locations (e.g., "Parking", "Main Lobby") and machine status.

•Wallet: A 1-to-1 relationship with the User. It stores the live balance of reward points.

•Deposit: The central log that links a User to a specific RVM. It stores material type, weight, and calculates points at the time of transaction.

--Business Logic: The Reward Engine--

Points are calculated and transferred automatically using a Django Model Override. When a deposit is saved:

1.Calculation: Points are calculated ( Plastic=1$,  Glass=2$,  Metal=3$ per kg).

2.Atomic Update: The calculated points are automatically added to the linked User's Wallet balance.

**--API Endpoints ---** 

/api/register/	        POST	         Create account (automatically creates a Wallet)

/api/login/	            POST	         Obtain Auth Token

/api/deposit/	        POST	         Log deposit from an RVM (links User + Machine)

/api/summary/	        GET	             View user's total weight, points, and wallet status


**Sample Deposit Request (From RVM Hardware)**

JSON
{
  "machine": 1,
  "material_type": "METAL",
  "weight": 5.0
}

**Sample Summary Response**

{
  "username": "Fatma",
  "total_recycled_weight": 11.0,
  "total_points_earned": 32.0,
  "wallet_status": "Active"
}


**Tech Stack***

-Python and Django & Django REST Framework (DRF): 
Core backend and API logic.

-Token Authentication: 
security for hardware-to-server communication.
