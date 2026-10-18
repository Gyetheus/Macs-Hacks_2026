import ast
import operator
import math
from decimal import Decimal

# Only allow basic arithmetic operations.
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

class MathEngine:
    def __init__(self):
        # list of variables so that GUI can access it
        self.variables = {
            "pi": math.pi,
            "e": math.e
        }

    def process_input(self, user_input):
        # GUI calls this function to process all inputs
        
        # 1. Detect Variable Assignment
        if "=" in user_input:
            # Split into exactly two parts at the first '='
            left_side, right_side = user_input.split("=", 1)
            var_name = left_side.strip()
            expression = right_side.strip()

            # Ensure the variable name is valid
            if not var_name.isidentifier():
                return "Error: Invalid variable name"

            # Calculate the right side of the equals sign
            result = self.calculate(expression)
            
            # If the calculation succeeded, store it in our shared dictionary
            if result is not None:
                self.variables[var_name] = result
                return f"{var_name} saved as {result}"
            else:
                return "Error: Invalid math expression"

        # Standard Evaluation
        else:
            result = self.calculate(user_input)
            return result if result is not None else "Error: Invalid math expression"

    def calculate(self, expression):
        try:
            tree = ast.parse(expression, mode="eval")
            return self.evaluate(tree.body)
        except Exception:
            return None

    def evaluate(self, node):
        # Numbers
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        # Variables: Look inside self.variables for variable names and values
        elif isinstance(node, ast.Name):
            if node.id in self.variables:
                return self.variables[node.id]
            raise ValueError(f"Undefined variable: {node.id}")

        # Binary operations
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in OPERATORS:
                raise ValueError("Unsupported operator")
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return OPERATORS[op_type](left, right)

        # Unary operations
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -self.evaluate(node.operand)
            elif isinstance(node.op, ast.UAdd):
                return self.evaluate(node.operand)
            raise ValueError("Unsupported unary operator")

        # Square root
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "sqrt"
            and len(node.args) == 1
            and not node.keywords
        ):
            return math.sqrt(self.evaluate(node.args[0]))

        else:
            raise ValueError("Unsupported expression") 