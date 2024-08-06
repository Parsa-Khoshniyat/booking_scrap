import time

from booking.booking import Booking
with Booking() as bot :
    bot.land_first_page()
    try:
        bot.close_sign_in()
    except:
        pass
    time.sleep(2)
    bot.change_currency_to_usd()
    time.sleep(2)
    try:
        bot.close_sign_in()
    except:
        pass
    bot.select_place_to_go('New york')#city
    bot.select_data("2024-09-08","2024-09-15")#check_in and check_out time
    bot.select_adults(2)#number of adult person
    bot.submit()
    bot.close_sign_in()
    bot.lowest_price_first()
    bot.apply_star(5)#rating of property
    bot.resault_box()
    time.sleep(3)
    bot.create_excel_file()

