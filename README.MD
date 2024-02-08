# Django REST API Messaging System

### Important to know 
- This project has already been deployed through the render cloud and is probably in hibernation currently make a request and wait around 30 seconds 

## Overview

This project implements a simple messaging system using Django and Django REST Framework. It allows users to send messages to each other, view all messages, read specific messages, and delete messages they own or have received.

## Features

- User registration and authentication.
- Send messages to other registered users.
- View all messages where the user is either the sender or receiver.
- View all unread messages.
- Read a specific message.
- Delete a message as the sender or receiver.


### Prerequisites

- Python 3.8 or higher
- pip
- Virtualenv (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shalevhagshur/Messages-System-API.git

2. Navigate to the project directory:
    ```bash
    cd messaging-api

3. Create and activate a virtual environment:
    python -m venv venv

    # On Windows
    .\venv\Scripts\activate

    # On Unix or MacOS
    source venv/bin/activate

4. Install the requirements:
    pip install -r requirements.txt

5. If You Wanna Run it locally
    python manage.py runserver

6. Usage
The API is accessible at http://127.0.0.1:8000/api/.
Use the following endpoints to interact with the API:
/api/register/ - For user registration.
/api/token/ - To obtain authentication tokens.
/api/messages/ - To send or view messages.
/api/messages/<message_id>/ - To read or delete specific messages.