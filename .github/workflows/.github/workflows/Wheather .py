import os
import requests
import smtplib
from email.message import EmailMessage

# 1. Configuration (For phone testing, paste your values inside the quotes)
# Once you move this code to GitHub, change them back to os.environ.get()
API_KEY = "PASTE_YOUR_API_KEY_HERE"
CITY = "London"  # Put your city here
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "receiver_email@gmail.com"

# 2. Ask OpenWeather for the forecast
url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
response = requests.get(url).json()

# SAFER CHECK: See if the server returned an error code
if response.get("cod") != "200":
    print("❌ Error from OpenWeatherMap:")
    print(f"Message: {response.get('message')}")
    print("Double check your API key formatting, city spelling, or wait 30 mins for activation.")
else:
    # If code is 200, everything works! Proceed safely:
    current_temp = response["list"][0]["main"]["temp"]
    rain_predicted = any("rain" in forecast for forecast in response["list"][:8])

    # 3. If conditions are met, send the email
    if current_temp > 35 or rain_predicted:
        msg = EmailMessage()
        msg["Subject"] = f"⚠️ Weather Alert for {CITY}!"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg.set_content(f"Alert! Current Temp: {current_temp}°C. Rain expected: {rain_predicted}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print("Alert email sent!")
    else:
        print(f"Weather in {CITY} is normal ({current_temp}°C). No email sent.")
      
