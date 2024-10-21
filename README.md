# Rule Engine Project

## Objective

Develop a simple 3-tier rule engine application with a Simple UI, API, and Backend to determine user eligibility based on attributes such as age, department, income, and experience. The system utilizes an Abstract Syntax Tree (AST) to represent conditional rules and allows for dynamic creation, combination, and modification of these rules.

## Features

- **Create Rules**: Dynamically create eligibility rules using a user-friendly API.
- **Combine Rules**: Efficiently combine multiple rules into a single AST.
- **Evaluate Rules**: Evaluate combined rules against user-provided data.
- **Error Handling**: Gracefully handle errors related to invalid rule strings or data formats.
- **Attribute Validation**: Validate user data against a predefined catalog of attributes.
- **Modify Existing Rules**: Update existing rules and their associated ASTs.
- **User-Defined Functions**: Support for user-defined functions within rules for advanced conditions.

## Technologies Used

- Python
- Flask (web framework)
- SQLite (database)

## Getting Started

### Prerequisites

- Python 3.x
- Pip (Python package installer)

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd rule_engine_project

2. **Set Up Virtual Environment** (Optional)

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # For macOS/Linux
   myenv\Scripts\activate  # For Windows

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt

**Project Structure**

rule_engine_project/
│
├── app.py                 # Main application file for the API
├── models.py              # Contains the database and data models
├── rule_engine.py         # Contains AST, rule parsing, and evaluation logic
├── database.db            # SQLite database file (created at runtime)
└── requirements.txt       # All the Python dependencies

**Initializing the Database**
   Run the following command to initialize the SQLite database:

   
   python -c "from models import init_db; init_db()"


**Running the Application**
   Start the Flask server with the command:
   
   python app.py

The server will run at http://127.0.0.1:5000/.

**API Endpoints**
 1.Create a Rule

  - POST /create_rule
  - Request Body :
    ```bash
     {
    "rules": [
        "((age > 30 and department == 'Sales') or (age < 25 and department == 'Marketing')) and (salary > 50000 or experience > 5)",
        "((age > 30 and department == 'Marketing')) and (salary > 20000 or experience > 5)"
    ]
    }

 2.Combine Rules

  - POST /combine_rules
  - Request Body :
      ```bash
     {
    "rules": [
        "((age > 30 and department == 'Sales') or (age < 25 and department == 'Marketing')) and (salary > 50000 or experience > 5)",
        "((age > 30 and department == 'Marketing')) and (salary > 20000 or experience > 5)"
    ]
    }

 3.Evaluate Rule

   - POST /evaluate
   - Request Body :
      ```bash
     {
    "rule": "((age > 30 and department == 'Sales') and (salary > 50000 and experience > 2))"
    }

 4.Update a Rule

  - PUT /update_rule/<rule_id>
  - Request Body :

     ```bash
     {
    "rule": "((age > 40 and department == 'Sales') or (age < 30 and department == 'Marketing'))"
    }

**Testing the API**
Use tools like Postman or cURL to test the API endpoints.

**Contributing**
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request!

**License**
This project is licensed under the MIT License. See the LICENSE file for details.

**Acknowledgments**
Thanks to the contributors and resources that helped in building this project.
