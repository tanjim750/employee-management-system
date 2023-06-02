import requests
from app.models import holiday
from datetime import datetime, timedelta
for year in range(2005,2025):

    # API endpoint and parameters for Bangladesh
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        "api_key": "ed193659de8d61ad88ab30d3cc9b2514df260a7c",  
        "country": "BD",
        "year": year,
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Parse the JSON response
    data = response.json()

    # Extract the holiday information
    holidays = data["response"]["holidays"]

    for Holiday in holidays:
        if ("National holiday" in Holiday["type"]) or (Holiday["primary_type"] == "Government Holiday"):
            year = Holiday["date"]["datetime"]["year"]
            month = Holiday["date"]["datetime"]["month"]
            day = Holiday["date"]["datetime"]["day"]

            date_object = datetime(year,month,day).date()

            holiday.objects.create(
                name = Holiday["name"],
                date = date_object,
                description = Holiday["description"]
            )



# capture all friday between 2000 to 2030
for year in range(2000,2031):
    for month in range(1,13):
        current_date = datetime(year,month,1).date()

        while current_date.weekday() != 4:
            current_date += timedelta(days=1)

        while current_date.month == month:
            date_already_exist = holiday.objects.filter(date=current_date).first()
            print(date_already_exist)
            if date_already_exist is None:
                holiday.objects.create(
                    name = "Friday",
                    date = current_date,
                    description = "Weekends"
                )

            current_date += timedelta(days=7)