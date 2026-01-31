"""
Pytest tests for Indian to US Unit Converter
Author: Vikas Neriyanuru (VIKAS0804)
Modified for Lab1 submission
"""

import pytest
from src import calculator

# ========== TEMPERATURE TESTS ==========

def test_celsius_to_fahrenheit():
    """Test Celsius to Fahrenheit conversion"""
    # Freezing point
    assert calculator.celsius_to_fahrenheit(0) == 32
    # Boiling point
    assert calculator.celsius_to_fahrenheit(100) == 212
    # Body temperature
    assert calculator.celsius_to_fahrenheit(37) == pytest.approx(98.6, 0.1)
    # Pleasant weather in India
    assert calculator.celsius_to_fahrenheit(25) == 77
    # Hot Delhi summer
    assert calculator.celsius_to_fahrenheit(40) == 104


# ========== DISTANCE TESTS ==========

def test_kilometers_to_miles():
    """Test kilometers to miles conversion"""
    assert calculator.kilometers_to_miles(1) == pytest.approx(0.621, 0.001)
    assert calculator.kilometers_to_miles(10) == pytest.approx(6.214, 0.001)
    # Bangalore to Chennai distance
    assert calculator.kilometers_to_miles(350) == pytest.approx(217.48, 0.01)
    # Mumbai to Pune
    assert calculator.kilometers_to_miles(150) == pytest.approx(93.21, 0.01)

def test_meters_to_feet():
    """Test meters to feet conversion"""
    assert calculator.meters_to_feet(1) == pytest.approx(3.281, 0.001)
    assert calculator.meters_to_feet(10) == pytest.approx(32.808, 0.001)
    # Average room height in India (3m)
    assert calculator.meters_to_feet(3) == pytest.approx(9.843, 0.001)


# ========== WEIGHT TESTS ==========

def test_kilograms_to_pounds():
    """Test kilograms to pounds conversion"""
    assert calculator.kilograms_to_pounds(1) == pytest.approx(2.205, 0.001)
    # Average Indian male weight
    assert calculator.kilograms_to_pounds(70) == pytest.approx(154.32, 0.01)
    # Luggage weight limit
    assert calculator.kilograms_to_pounds(23) == pytest.approx(50.71, 0.01)

def test_grams_to_ounces():
    """Test grams to ounces conversion"""
    assert calculator.grams_to_ounces(100) == pytest.approx(3.527, 0.001)
    assert calculator.grams_to_ounces(500) == pytest.approx(17.637, 0.001)
    # 1 kg = 35.274 oz
    assert calculator.grams_to_ounces(1000) == pytest.approx(35.274, 0.001)


# ========== VOLUME TESTS ==========

def test_liters_to_gallons():
    """Test liters to US gallons conversion"""
    assert calculator.liters_to_gallons(1) == pytest.approx(0.264, 0.001)
    # Car fuel tank (45 liters)
    assert calculator.liters_to_gallons(45) == pytest.approx(11.888, 0.001)
    # Milk bottle (1 liter)
    assert calculator.liters_to_gallons(1) == pytest.approx(0.264, 0.001)


# ========== HELPER FUNCTION TESTS ==========

def test_describe_weather():
    """Test weather description function"""
    # Pleasant weather
    result = calculator.describe_weather(20)
    assert result['celsius'] == 20
    assert result['fahrenheit'] == 68.0
    assert result['category'] == 'pleasant'
    
    # Warm weather
    result = calculator.describe_weather(25)
    assert result['celsius'] == 25
    assert result['fahrenheit'] == 77.0
    assert result['category'] == 'warm'
    
    # Hot Delhi summer
    result = calculator.describe_weather(40)
    assert result['celsius'] == 40
    assert result['fahrenheit'] == 104.0
    assert result['category'] == 'hot'
    
    # Cold winter
    result = calculator.describe_weather(10)
    assert result['celsius'] == 10
    assert result['category'] == 'cold'

def test_convert_height():
    """Test height conversion"""
    # Average Indian male height (175 cm)
    result = calculator.convert_height(175)
    assert result['cm'] == 175
    assert result['meters'] == 1.75
    assert result['feet'] == 5
    assert result['inches'] == pytest.approx(8.9, 0.1)
    
    # 6 feet = 183 cm
    result = calculator.convert_height(183)
    assert result['feet'] == 6
    assert result['inches'] == pytest.approx(0.0, 0.2)

def test_driving_distance():
    """Test driving distance conversion"""
    # Short trip
    result = calculator.driving_distance(10)
    assert result['kilometers'] == 10
    assert result['miles'] == pytest.approx(6.21, 0.01)
    
    # Bangalore to Chennai
    result = calculator.driving_distance(350)
    assert result['kilometers'] == 350
    assert result['miles'] == pytest.approx(217.48, 0.01)


# ========== ERROR HANDLING TESTS ==========

def test_negative_values():
    """Test that negative values raise errors where appropriate"""
    with pytest.raises(ValueError):
        calculator.kilometers_to_miles(-10)
    
    with pytest.raises(ValueError):
        calculator.kilograms_to_pounds(-5)
    
    with pytest.raises(ValueError):
        calculator.liters_to_gallons(-1)

def test_invalid_input_types():
    """Test that invalid input types raise ValueError"""
    with pytest.raises(ValueError):
        calculator.celsius_to_fahrenheit("hot")
    
    with pytest.raises(ValueError):
        calculator.kilometers_to_miles("100km")
    
    with pytest.raises(ValueError):
        calculator.convert_height("5'10\"")
