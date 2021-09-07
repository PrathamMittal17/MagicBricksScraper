# MagicBricksScraper

## This tool can be used to scrape property data from MagicBricks website.<br/>
It returns bhk,price(in lakhs),transaction type(new property/resale),address,area(in sqft),furnishing status.<br/>
The data is stored in a csv format.<br/>

To use the tool all you need to do is give city name and location for csv file to be saved to the function getData.<br/>If you are giving a city name which has words separated by space then pass them with a <b>-</b> in between eg: 'New-Delhi'.<br/>

You can also pass an optional parameter data_qty with a integer value to the function getData to get more data.(Default value is 3 and higher the value more the data)<br/>
You can also pass start_values parameter with a integer value to the function getData to get data from that index.(Default value is 0)</br>

You also will need to give location for your Selenium Webdriver in the variable drive_path.<br/>

<b>Happy Scraping</b>
