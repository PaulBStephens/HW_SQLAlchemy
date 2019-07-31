from flask import Flask, jsonify

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask setup
app = Flask(__name__)

# Flask Routes
# @app.route("/")
# def available():
#     return"""<html>


@app.route("/")

def welcome():

    """List all available api routes."""

    return (

        f"Available Routes:<br/>"

        f"<br/>"

        f"/api/v1.0/precipitation<br/>"

        f"- List of dates and percipitation observations from the last year<br/>"

        f"<br/>"

        f"/api/v1.0/stations<br/>"

        f"- List of stations from the dataset<br/>"

        f"<br/>"

        f"/api/v1.0/tobs<br/>"

        f"- List of Temperature Observations (tobs) for the previous year<br/>"

        f"<br/>"

        f"/api/v1.0/start<br/>"

        f"- List of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range<br/>"

        f"<br/>"

        f"/api/v1.0/start/end<br/>"

        f"- List of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range, inclusive<br/>"



    )









@app.route("/api/v1.0/precipitation")

def precipitation():

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()



    # Get the first element of the tuple

    max_date = max_date[0]



    # Calculate the date 1 year ago from today

    # The days are equal 366 so that the first day of the year is included

    year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)

    

    # Perform a query to retrieve the data and precipitation scores

    results_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()



    # Convert list of tuples into normal list

    precipitation_dict = dict(results_precipitation)



    return jsonify(precipitation_dict)