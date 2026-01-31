"""
Unittest tests for Indian to US Unit Converter
Author: Vikas Raminmohammadi (VIKAS0804)
Modified for Lab1 submission
"""

import sys
import os
import unittest

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import calculator


class TestUnitConverter(unittest.TestCase):

    # ========== TEMPERATURE TESTS ==========
    
    def test_celsius_to_fahrenheit(self):
        """Test Celsius to Fahrenheit conversion"""
        self.assertEqual(calculator.celsius_to_fahrenheit(0), 32)
        self.assertEqual(calculator.celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(calculator.celsius_to_fahrenheit(37), 98.6, places=1)
        self.assertEqual(calculator.celsius_to_fahrenheit(25), 77)
        self.assertEqual(calculator.celsius_to_fahrenheit(40), 104)

    # ========== DISTANCE TESTS ==========
    
    def test_kilometers_to_miles(self):
        """Test kilometers to miles conversion"""
        self.assertAlmostEqual(calculator.kilometers_to_miles(1), 0.621, places=3)
        self.assertAlmostEqual(calculator.kilometers_to_miles(10), 6.214, places=2)
        # Bangalore to Chennai
        self.assertAlmostEqual(calculator.kilometers_to_miles(350), 217.48, places=1)
    
    def test_meters_to_feet(self):
        """Test meters to feet conversion"""
        self.assertAlmostEqual(calculator.meters_to_feet(1), 3.281, places=2)
        self.assertAlmostEqual(calculator.meters_to_feet(10), 32.808, places=2)
        self.assertAlmostEqual(calculator.meters_to_feet(3), 9.843, places=2)

    # ========== WEIGHT TESTS ==========
    
    def test_kilograms_to_pounds(self):
        """Test kilograms to pounds conversion"""
        self.assertAlmostEqual(calculator.kilograms_to_pounds(1), 2.205, places=2)
        self.assertAlmostEqual(calculator.kilograms_to_pounds(70), 154.32, places=1)
        self.assertAlmostEqual(calculator.kilograms_to_pounds(23), 50.71, places=1)
    
    def test_grams_to_ounces(self):
        """Test grams to ounces conversion"""
        self.assertAlmostEqual(calculator.grams_to_ounces(100), 3.527, places=2)
        self.assertAlmostEqual(calculator.grams_to_ounces(500), 17.637, places=2)
        self.assertAlmostEqual(calculator.grams_to_ounces(1000), 35.274, places=2)

    # ========== VOLUME TESTS ==========
    
    def test_liters_to_gallons(self):
        """Test liters to US gallons conversion"""
        self.assertAlmostEqual(calculator.liters_to_gallons(1), 0.264, places=2)
        self.assertAlmostEqual(calculator.liters_to_gallons(45), 11.888, places=2)

    # ========== HELPER FUNCTION TESTS ==========
    
    def test_describe_weather(self):
        """Test weather description function"""
        result = calculator.describe_weather(20)
        self.assertEqual(result['celsius'], 20)
        self.assertEqual(result['fahrenheit'], 68.0)
        self.assertEqual(result['category'], 'pleasant')
        
        result = calculator.describe_weather(40)
        self.assertEqual(result['celsius'], 40)
        self.assertEqual(result['fahrenheit'], 104.0)
        self.assertEqual(result['category'], 'hot')
    
    def test_convert_height(self):
        """Test height conversion"""
        result = calculator.convert_height(175)
        self.assertEqual(result['cm'], 175)
        self.assertEqual(result['meters'], 1.75)
        self.assertEqual(result['feet'], 5)
        self.assertAlmostEqual(result['inches'], 8.9, places=1)
        
        result = calculator.convert_height(183)
        self.assertEqual(result['feet'], 6)
        self.assertAlmostEqual(result['inches'], 0.0, places=0)
    
    def test_driving_distance(self):
        """Test driving distance conversion"""
        result = calculator.driving_distance(10)
        self.assertEqual(result['kilometers'], 10)
        self.assertAlmostEqual(result['miles'], 6.21, places=1)
        
        result = calculator.driving_distance(350)
        self.assertEqual(result['kilometers'], 350)
        self.assertAlmostEqual(result['miles'], 217.48, places=1)

    # ========== ERROR HANDLING TESTS ==========
    
    def test_negative_values(self):
        """Test that negative values raise errors where appropriate"""
        with self.assertRaises(ValueError):
            calculator.kilometers_to_miles(-10)
        
        with self.assertRaises(ValueError):
            calculator.kilograms_to_pounds(-5)
        
        with self.assertRaises(ValueError):
            calculator.liters_to_gallons(-1)
    
    def test_invalid_input_types(self):
        """Test that invalid input types raise ValueError"""
        with self.assertRaises(ValueError):
            calculator.celsius_to_fahrenheit("hot")
        
        with self.assertRaises(ValueError):
            calculator.kilometers_to_miles("100km")
        
        with self.assertRaises(ValueError):
            calculator.convert_height("5'10\"")


if __name__ == '__main__':
    unittest.main()
