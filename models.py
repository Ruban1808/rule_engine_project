import sqlite3

def init_db():
    """Initialize the database and create the necessary table."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL,
            ast_json TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_rule(rule_string, ast_json):
    """Insert a rule into the database."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO rules (rule_string, ast_json) VALUES (?, ?)', (rule_string, ast_json))
    conn.commit()
    conn.close()

def get_rules():
    """Retrieve all rules from the database."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM rules')
    rules = c.fetchall()
    conn.close()
    return rules

VALID_ATTRIBUTES = {"age", "department", "salary", "experience"}

def validate_data(data):
    """Validates that the provided data contains only allowed attributes."""
    for key in data.keys():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Invalid attribute: {key}")

def evaluate_rule(ast_node, data):
    """Evaluates the rule against provided data."""
    validate_data(data)  # Validate the input data

    if ast_node.type == "operand":
        condition = ast_node.value
        return eval(condition, {}, data)
    elif ast_node.type == "operator":
        left_eval = evaluate_rule(ast_node.left, data)
        right_eval = evaluate_rule(ast_node.right, data)
        if ast_node.value == "AND":
            return left_eval and right_eval
        elif ast_node.value == "OR":
            return left_eval or right_eval

def update_rule(rule_id, new_rule_string):
    """Updates an existing rule in the database."""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        ast_representation = create_rule(new_rule_string)
        c.execute('UPDATE rules SET rule_string = ?, ast_json = ? WHERE id = ?', (new_rule_string, str(ast_representation), rule_id))
        conn.commit()
    except ValueError as e:
        raise ValueError(f"Failed to update rule: {e}")
    finally:
        conn.close()
