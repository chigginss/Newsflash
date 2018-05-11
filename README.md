# Newsflash

Newsflash displays the most popular news breaking right now in a D3.js visual. It organizes trending stories by the popularity and bias of the respective media outlet. Newsflash allows you to learn more about where your news comes from; users can observe how different bias may influence how news is reported. Additionally, users can search for trending coverage around a certain topic, and save these search terms. Newsflash visualizes data from NewsAPI, and combines this data with metrics from AllSides and Alexa's top 500 websites.

# Tech 

Newsflash is built on a Flask server with a PostgreSQL database. The front end template is created uses HTML, CSS, Bootstrap and Jinja2. Javascript's JQuery and AJAX interact with the backend. The visuals were created with D3.js, using JSON data from NewsAPI and the database, which is combined on my server using Python and SQLAlchemy. Server routes are tested using the Python unittest module.

Make sure you are using Python 2.7 and create a virtualenv to install requirements.txt. 

You will need to make your own NewsAPI account and APIKey in order to use the D3 visual.

# Features 

- View Top Trending news for the current time, complete with a key for Bias and Scale. Titles are links to the respective outlet and will open in a new tab.
- Search for news coverage by a keyword, brand or name.
- Allows users to create an account, log-in, favorite search terms, and share coverage through mail.

### Landing 
![alt text](https://github.com/chigginss/Newsflash/blob/master/static/css/landing.JPG)

### Homepage 
![alt text](https://github.com/chigginss/Newsflash/blob/master/static/css/homepage.JPG)

### Register
![alt text](https://github.com/chigginss/Newsflash/blob/master/static/css/accountreg.JPG)

### Login
![alt text](https://github.com/chigginss/Newsflash/blob/master/static/css/login.JPG)

### Search for News (logged out)
![alt text](https://github.com/chigginss/Newsflash/blob/master/static/css/search.JPG)

### Search for News (logged in)
![alt text](https://github.com/chigginss/Newsflash/blob/master/static/css/loginsearch.JPG)

# About the Developer 

Cierra Higgins is software engineer located in the SF bay area.
