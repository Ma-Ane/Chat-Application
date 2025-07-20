# FastAPI Chat Application

This is a simple yet extensible **real-time chat application** built using **FastAPI** and **WebSocket**, secured with **JWT-based authentication** and backed by **PostgreSQL**.

## Features

- User Registration and Login with JWT
- Role-Based Access Control (Admin, User)
- WebSocket-based real-time chat
- Protected WebSocket endpoint with token validation
- PostgreSQL database for persisting users and messages
- Room-based chat system
- Modular and scalable codebase


## Tech Stack

- **Backend**: FastAPI
- **Real-time Communication**: WebSocket
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy or SQLModel
- **Authentication**: JWT (JSON Web Tokens)
- **Server**: Uvicorn


## Project Structure

    ├── app/  
    │   ├── main.py              # FastAPI entry point  
    │   ├── models.py            # SQLAlchemy/SQLModel models  
    │   ├── schemas.py           # Pydantic schemas  
    │   ├── auth.py              # JWT generation and verification  
    │   ├── database.py          # DB connection logic  
    │   ├── websocket.py         # WebSocket endpoint and broadcasting  
    │   └── utils.py             # Utility functions    
    |   └── requirements.txt     # required packages  
    └── README.md  


## Running the Application

1. Clone the repository  

        git clone https://github.com/your-username/fastapi-chat-app.git  
        cd fastapi-chat-app  

2. Setup virtual environment  

        python -m venv venv  
        source venv/bin/activate  # On Windows: venv\Scripts\activate  

3. Install required dependencies  

       pip install -r requirements.txt  

5. Configure PostgreSQL  

       DATABASE_URL = "postgresql://username:password@localhost/dbname"  

7. Run the server  

        uvicorn app.main:app --reload  

