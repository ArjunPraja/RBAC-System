
# RBAC System

A Role-Based Access Control (RBAC) System built with Flask, Python, and JWT for secure user authentication and authorization. The system allows users to register as either employees or managers. After logging in, users are redirected to their respective pages based on their roles (Employee Page or Manager Page).

## Features
- **User Registration**: Users can register as either an employee or manager.
- **JWT Authentication**: JSON Web Tokens (JWT) are used for secure user authentication.
- **Role-based Redirection**: After logging in, users are redirected to either the employee or manager page based on their role.
- **Role-based Access Control**: Managers and employees have access to different resources and pages based on their roles.
  
## Technologies Used
- **Flask**: Web framework for building the application.
- **PyJWT**: Library for working with JWTs.
- **Flask-JWT-Extended**: Extension for integrating JWTs with Flask.
- **MongoDB** (or any database of your choice): For storing user details and roles.
  
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RBAC-System.git
   cd RBAC-System
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your database (SQLite is used by default, but you can modify the code to use another database).
   - Run the Flask application:
   ```bash
   python app.py
   ```

## API Endpoints

### 1. Register User
- **Route**: `POST /register`
- **Description**: Registers a new user as either an employee or manager.
- **Request Body**:
  ```json
  {
    "username": "user1",
    "password": "password123",
    "role": "employee"  // or "manager"
  }
  ```

### 2. Login
- **Route**: `POST /login`
- **Description**: Authenticates the user and returns a JWT token.
- **Request Body**:
  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "jwt-token-here"
  }
  ```

### 3. Protected Route (Employee Page)
- **Route**: `GET /employee`
- **Description**: Accessible only by employees.
- **Authorization**: Bearer token is required.

### 4. Protected Route (Manager Page)
- **Route**: `GET /manager`
- **Description**: Accessible only by managers.
- **Authorization**: Bearer token is required.

## How It Works

1. **User Registration**: Users can register as either an employee or manager. The role is specified during registration.
   
2. **Login and JWT Token Generation**: After logging in, a JWT token is generated and returned to the user. This token is used for authenticating the user for further requests.

3. **Role-based Redirection**:
   - After login, users are redirected to their respective pages based on their role.
     - Employees are redirected to `/employee`.
     - Managers are redirected to `/manager`.

4. **JWT Authentication**: For accessing the protected routes (`/employee` and `/manager`), users must include their JWT token in the `Authorization` header as `Bearer <token>`.

## Example Workflow

1. **Register a Manager**:
   ```bash
   POST /register
   {
     "username": "manager1",
     "password": "password123",
     "role": "manager"
   }
   ```

2. **Login as Manager**:
   ```bash
   POST /login
   {
     "username": "manager1",
     "password": "password123"
   }
   ```

3. **Access the Manager Page**:
   After successful login, use the `access_token` in the `Authorization` header to access the manager page:
   ```bash
   GET /manager
   Authorization: Bearer <access_token>
   ```

4. **Register an Employee**:
   ```bash
   POST /register
   {
     "username": "employee1",
     "password": "password123",
     "role": "employee"
   }
   ```

5. **Login as Employee**:
   ```bash
   POST /login
   {
     "username": "employee1",
     "password": "password123"
   }
   ```

6. **Access the Employee Page**:
   After successful login, use the `access_token` in the `Authorization` header to access the employee page:
   ```bash
   GET /employee
   Authorization: Bearer <access_token>
   ```

## Security

- JWT tokens are used for authentication. They are signed with a secret key (`JWT_SECRET_KEY`), ensuring that the tokens cannot be tampered with.
- The system provides role-based access control, ensuring that employees cannot access manager routes and vice versa.

## Contributing

Feel free to fork this repository, contribute, or raise issues. Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:
- Replace `yourusername` in the GitHub link with your actual GitHub username.
- Make sure to update the `JWT_SECRET_KEY` and database connection details as needed in your app.

```

This `README.md` file explains the features of your RBAC System, installation instructions, API usage, and how JWT is used for authentication.
