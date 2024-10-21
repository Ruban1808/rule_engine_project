from flask import Flask, request, jsonify
from rule_engine import create_rule, combine_rules, evaluate_rule
from models import insert_rule, get_rules
class Node:
    def __init__(self, value):
        self.value = value


app = Flask(__name__)
  # Now parse the string
def convert_to_python_syntax(rule_string):
    return rule_string.replace('AND', 'and').replace('OR', 'or')
   

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    """API endpoint to create a rule and store it in the database."""
    rule_string = request.json.get('rule')
    if not rule_string:
        return jsonify({'error': 'Rule string is required'}), 400

    # Convert SQL-like syntax to Python syntax
    rule_string = convert_to_python_syntax(rule_string)

    try:
        ast_representation = create_rule(rule_string)
    except SyntaxError as e:
        return jsonify({'error': str(e)}), 400  # Handle syntax errors gracefully

    insert_rule(rule_string, str(ast_representation))
    return jsonify({'ast': str(ast_representation)})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    print("Combine rules API called")  # Debugging output
    rules = request.json.get('rules')
    print("Received rules:", rules)
    """API endpoint to combine multiple rules."""
    if not rules:
        return jsonify({'error': 'Rules are required'}), 400

    combined_ast = combine_rules(rules)
    return jsonify({'combined_ast': str(combined_ast)})

@app.route('/evaluate', methods=['POST'])
def evaluate_rule_api():
    """API endpoint to evaluate a rule against user data."""
    selected_rule = request.json.get('rule')  # Use .get() to avoid KeyError
    print("Evaluating:", selected_rule)

    try:
        # Define Node if needed, or remove it if not used
        ast_representation = eval(selected_rule, {"__builtins__": None, "age": 35, "department": "Sales", "salary": 60000, "experience": 3})
        return jsonify({"result": ast_representation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update_rule/<int:rule_id>', methods=['PUT'])
def update_rule_api(rule_id):
    new_rule_string = request.json.get('rule')
    if not new_rule_string:
        return jsonify({'error': 'New rule string is required'}), 400

    try:
        update_rule(rule_id, new_rule_string)
        return jsonify({'message': 'Rule updated successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
