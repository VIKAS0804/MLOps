"""
Indian to US Unit Converter Module
Author: Vikas Neriyanuru (VIKAS0804)
Date: January 31, 2026

A practical unit converter for someone moving from India to the US.
Converts common measurements: temperature, distance, weight, and volume.
"""

# ========== TEMPERATURE CONVERSIONS ==========

def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    Common in India and Common in US
    
    Args:
        celsius (int/float): Temperature in Celsius
    Returns:
        float: Temperature in Fahrenheit
    """
    if not isinstance(celsius, (int, float)):
        raise ValueError("Temperature must be a number.")
    return (celsius * 9/5) + 32


# ========== DISTANCE CONVERSIONS ==========

def kilometers_to_miles(km):
    """
    Convert kilometers to miles.
    Used in India and Used in US
    
    Args:
        km (int/float): Distance in kilometers
    Returns:
        float: Distance in miles
    """
    if not isinstance(km, (int, float)):
        raise ValueError("Distance must be a number.")
    if km < 0:
        raise ValueError("Distance cannot be negative.")
    return km * 0.621371

def meters_to_feet(meters):
    """
    Convert meters to feet.
    Used in India and Used in US
    Args:
        meters (int/float): Height/length in meters
    Returns:
        float: Height/length in feet
    """
    if not isinstance(meters, (int, float)):
        raise ValueError("Distance must be a number.")
    if meters < 0:
        raise ValueError("Distance cannot be negative.")
    return meters * 3.28084


# ========== WEIGHT CONVERSIONS ==========

def kilograms_to_pounds(kg):
    """
    Convert kilograms to pounds.
    Used in India and Used in US
    
    Args:
        kg (int/float): Weight in kilograms
    Returns:
        float: Weight in pounds
    """
    if not isinstance(kg, (int, float)):
        raise ValueError("Weight must be a number.")
    if kg < 0:
        raise ValueError("Weight cannot be negative.")
    return kg * 2.20462

def grams_to_ounces(grams):
    """
    Convert grams to ounces.
    Used in India and Used in US
    Args:
        grams (int/float): Weight in grams
    Returns:
        float: Weight in ounces
    """
    if not isinstance(grams, (int, float)):
        raise ValueError("Weight must be a number.")
    if grams < 0:
        raise ValueError("Weight cannot be negative.")
    return grams * 0.035274


# ========== VOLUME CONVERSIONS ==========

def liters_to_gallons(liters):
    """
    Convert liters to US gallons.
    Used in India and Used in US (for fuel, milk etc)
    
    Args:
        liters (int/float): Volume in liters
    Returns:
        float: Volume in US gallons
    """
    if not isinstance(liters, (int, float)):
        raise ValueError("Volume must be a number.")
    if liters < 0:
        raise ValueError("Volume cannot be negative.")
    return liters * 0.264172


# ========== PRACTICAL HELPER FUNCTIONS ==========

def describe_weather(celsius):
    """
    Describe weather in both Celsius and Fahrenheit with category.
    Useful for understanding US weather forecasts!
    
    Args:
        celsius (int/float): Temperature in Celsius
    Returns:
        dict: Temperature in both units with description
    """
    if not isinstance(celsius, (int, float)):
        raise ValueError("Temperature must be a number.")
    
    fahrenheit = celsius_to_fahrenheit(celsius)
    
    if celsius < 0:
        category = "freezing cold"
    elif celsius < 15:
        category = "cold"
    elif celsius < 25:
        category = "pleasant"
    elif celsius < 35:
        category = "warm"
    else:
        category = "hot"
    
    return {
        'celsius': celsius,
        'fahrenheit': round(fahrenheit, 1),
        'category': category,
        'description': f"{celsius}°C ({fahrenheit:.1f}°F) - {category}"
    }

def convert_height(cm):
    """
    Convert height from centimeters to feet and inches.
    Very useful for filling US forms!
    
    Args:
        cm (int/float): Height in centimeters
    Returns:
        dict: Height in various formats
    """
    if not isinstance(cm, (int, float)):
        raise ValueError("Height must be a number.")
    if cm < 0:
        raise ValueError("Height cannot be negative.")
    
    total_inches = cm / 2.54
    feet = int(total_inches // 12)
    inches = round(total_inches % 12, 1)
    
    return {
        'cm': cm,
        'meters': round(cm / 100, 2),
        'feet': feet,
        'inches': inches,
        'total_inches': round(total_inches, 1),
        'description': f"{feet}'{inches}\""
    }

def driving_distance(km):
    """
    Convert driving distance with practical context.
    
    Args:
        km (int/float): Distance in kilometers
    Returns:
        dict: Distance in both units
    """
    if not isinstance(km, (int, float)):
        raise ValueError("Distance must be a number.")
    if km < 0:
        raise ValueError("Distance cannot be negative.")
    
    miles = kilometers_to_miles(km)
    
    return {
        'kilometers': km,
        'miles': round(miles, 2),
        'description': f"{km} km = {miles:.2f} miles"
    }


# Example usage (commented out for testing)
# if __name__ == "__main__":
#     # Temperature: Delhi summer
#     print(describe_weather(40))  # 40°C in Delhi
#     
#     # Height: Average Indian male
#     print(convert_height(175))  # 175 cm
#     
#     # Distance: Bangalore to Chennai
#     print(driving_distance(350))  # 350 km
