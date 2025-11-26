# def calculate_expression(expression):
#     try:
#         expression = expression.strip().replace(' ', '')
#         allowed_chars = set('0123456789+-*/.()')
#         if not all(c in allowed_chars for c in expression):
#             return None
#         result = eval(expression)
#         return str(result)
#     except:
#         return None

class ExpressionCalculator:
    def __init__(self):
        self.allowed_chars = set('0123456789+-*/.()')

    def sanitize(self, expression):
        if expression is None:
            return None
        return expression.strip().replace(' ', '')

    def is_valid(self, expression):
        if not expression:
            return False
        return all(char in self.allowed_chars for char in expression)

    def calculate(self, expression):
        expression = self.sanitize(expression)
        if not self.is_valid(expression):
            return None
        try:
            return str(eval(expression))
        except Exception:
            return None

_calculator = ExpressionCalculator()

def calculate_expression(expression):
    return _calculator.calculate(expression)