
# Guaíba River Elevation Prediction App

This Flask application fetches water level data from the Guaíba River and predicts future elevations based on linear regression. The data is scraped from a specified URL and the application plots the actual and predicted water levels on a graph.

Link: **[App in Heroku](https://elevation-predication-a3cc309a132f.herokuapp.com/)** (disabled)

## Features

- Fetches the latest water level data from the specified URL.
- Uses linear regression to predict future water levels.
- Displays the data and predictions on a graph.
- Hosted on Heroku.

## Prerequisites

- Python 3.9.x
- Pip (Python package installer)
- Git
- Heroku CLI (command line interface)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/rodolfobortolin/nivel-guaiba.git
   cd nivel-guaiba
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application Locally

1. **Set the FLASK_APP environment variable:**

   ```bash
   export FLASK_APP=app.py  # On Windows use `set FLASK_APP=app.py`
   ```

2. **Run the Flask application:**

   ```bash
   flask run
   ```

3. Open your web browser and go to `http://127.0.0.1:5000`.

## Deploying to Heroku

1. **Login to Heroku:**

   ```bash
   heroku login
   ```

2. **Create a new Heroku application:**

   ```bash
   heroku create your-app-name
   ```

3. **Set the buildpack to Python:**

   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Deploy the application:**

   ```bash
   git add .
   git commit -m "Initial commit"
   git push heroku master
   ```

5. **Open your Heroku app in the browser:**

   ```bash
   heroku open
   ```

## Project Structure

```
/nivel-guaiba
|-- app.py
|-- requirements.txt
|-- runtime.txt
|-- Procfile
|-- templates
    |-- index.html
```

- `app.py`: The main Flask application.
- `requirements.txt`: Lists the Python dependencies.
- `runtime.txt`: Specifies the Python version.
- `Procfile`: Specifies the commands that are executed by the Heroku app.
- `templates/index.html`: HTML template for the Flask application.

## Dependencies

- Flask
- Pandas
- Matplotlib
- Requests
- BeautifulSoup4
- Scikit-learn

## Acknowledgements

- [Heroku](https://www.heroku.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [Requests](https://requests.readthedocs.io/en/master/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scikit-learn](https://scikit-learn.org/stable/)
