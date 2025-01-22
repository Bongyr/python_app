import unittest
import requests

class TestAPI(unittest.TestCase):

    def test_api_response(self):
        url = "http://127.0.0.1:5000/api/endpoint"  # Замість цього використовуйте правильний URL вашого API
        response = requests.get(url)
        
        # Перевірка, чи відповідає код статусу 200
        self.assertEqual(response.status_code, 200)

        # Перевірка наявності конкретної інформації у відповіді
        self.assertIn("expected_value", response.text)

if __name__ == "__main__":
    unittest.main()
