import datetime
import functions
import logging
import time
import weather


logging.basicConfig(filename="log_file.log", encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')

day_sunny_wallpaper = "day.jpeg"
day_rainy_wallpaper = "rain.png"
night_wallpaper = "night.png"

while True:
    print("STATUS: auto-wallpaper is running...")
    logging.info("Program started")

    today_date = datetime.date.today()                          # example: 2026-06-18
    twilight_api = functions.get_twilight_api(today_date)       # returns filtered json
    today_sunrise = functions.get_sunrise_datetime(twilight_api, today_date)    # return sunrise datetime object
    today_sunset = functions.get_sunset_datetime(twilight_api, today_date)      # return sunset datetime object
    # ? now_datetime = datetime.datetime.now() # return the datetime object at this moment // this code was not used previously 

    # checks to see if it is after sunset (waits for tomorrow's sunrise if it is) otherwise waits for either today's sunrise or sunset
    if (datetime.datetime.now() > today_sunset):
        logging.info("1")
        tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
        twilight_api = functions.get_twilight_api(today_date) # still passing today_date b/c api provides next day info after sunset
        today_sunrise = functions.get_sunrise_datetime(twilight_api, tomorrow_date)

        functions.run_gsettings(night_wallpaper)

        while (datetime.datetime.now() < today_sunrise):
            time.sleep(60)


        if(weather.get_condition() < 1006): 
            functions.run_gsettings(day_sunny_wallpaper)
        else:
            functions.run_gsettings(day_rainy_wallpaper)

        logging.info("2")

    else:
        if (datetime.datetime.now() < today_sunrise):
            logging.info("3")
            
            functions.run_gsettings(night_wallpaper)

            while(datetime.datetime.now() < today_sunrise):
                time.sleep(60)

            if(weather.get_condition() < 1006): 
                functions.run_gsettings(day_sunny_wallpaper)
            else:
                functions.run_gsettings(day_rainy_wallpaper)

            logging.info("4")

        else:
            logging.info("5")
            
            if(weather.get_condition() < 1006): 
                functions.run_gsettings(day_sunny_wallpaper)
            else:
                functions.run_gsettings(day_rainy_wallpaper)

            while(datetime.datetime.now() < today_sunset):
                time.sleep(60)

                if(weather.get_condition() < 1006): 
                    functions.run_gsettings(day_sunny_wallpaper)
                else:
                    functions.run_gsettings(day_rainy_wallpaper)

            functions.run_gsettings(night_wallpaper)

            logging.info("6")
