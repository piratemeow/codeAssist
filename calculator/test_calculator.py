import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.evaluate("1 + 2"), 3.0)
        self.assertEqual(self.calculator.evaluate("10 + 20"), 30.0)
        self.assertEqual(self.calculator.evaluate("1 + 2 + 3"), 6.0)

    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate("5 - 2"), 3.0)
        self.assertEqual(self.calculator.evaluate("10 - 20"), -10.0)
        self.assertEqual(self.calculator.evaluate("10 - 2 - 3"), 5.0)

    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate("2 * 3"), 6.0)
        self.assertEqual(self.calculator.evaluate("5 * 0"), 0.0)
        self.assertEqual(self.calculator.evaluate("2 * 3 * 4"), 24.0)

    def test_division(self):
        self.assertEqual(self.calculator.evaluate("6 / 2"), 3.0)
        self.assertAlmostEqual(self.calculator.evaluate("7 / 2"), 3.5)
        with self.assertRaises(ZeroDivisionError):
            self.calculator.evaluate("1 / 0")

    def test_modulo(self):
        self.assertEqual(self.calculator.evaluate("7 % 2"), 1.0)
        self.assertEqual(self.calculator.evaluate("10 % 5"), 0.0)

    def test_mixed_operations(self):
        self.assertEqual(self.calculator.evaluate("1 + 2 * 3"), 7.0)
        self.assertEqual(self.calculator.evaluate(" (1 + 2) * 3"), 9.0)
        self.assertEqual(self.calculator.evaluate("10 - 4 / 2"), 8.0)
        self.assertEqual(self.calculator.evaluate(" (10 - 4) / 2"), 3.0)
        self.assertEqual(self.calculator.evaluate("1 + 2 * 3 - 4 / 2"), 5.0) # 1 + 6 - 2 = 5

    def test_parentheses(self):
        self.assertEqual(self.calculator.evaluate("(1 + 2) * 3"), 9.0)
        self.assertEqual(self.calculator.evaluate("((1 + 2) * 3)"), 9.0)
        self.assertEqual(self.calculator.evaluate("1 + (2 * 3)"), 7.0)
        with self.assertRaises(ValueError):
            self.calculator.evaluate("(1 + 2")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("1 + 2)")

    def test_float_numbers(self):
        self.assertAlmostEqual(self.calculator.evaluate("1.5 + 2.5"), 4.0)
        self.assertAlmostEqual(self.calculator.evaluate("5.0 / 2.0"), 2.5)
        self.assertAlmostEqual(self.calculator.evaluate("1.1 * 2.2"), 2.42)

    def test_empty_expression(self):
        self.assertIsNone(self.calculator.evaluate(""))
        self.assertIsNone(self.calculator.evaluate("   "))

    def test_invalid_token(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("1 + abc")
        with self.assertRaises(ValueError):
            self.calculator.evaluate("1 $ 2")

    def test_unary_minus(self):
        # The current calculator doesn't support unary minus directly without parentheses,
        # so these tests will likely fail or behave unexpectedly without changes to the tokenizer/parser.
        # For now, we'll test cases that should work with the current parsing.
        # If the intention is to support unary minus, the tokenizer/parser would need modification.
        self.assertEqual(self.calculator.evaluate("3 - (1 - 2)"), 4.0) # 3 - (-1) = 4
        self.assertEqual(self.calculator.evaluate("-(1 + 2)"), -3.0) # This will fail with current implementation
        self.assertEqual(self.calculator.evaluate("-5 + 2"), -3.0) # This will fail with current implementation

if __name__ == "__main__":
    unittest.main()
