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









# @app.route("/api/v1.0/precipitation")

# def precipitation():

#     max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()



#     # Get the first element of the tuple

#     max_date = max_date[0]



#     # Calculate the date 1 year ago from today

#     # The days are equal 366 so that the first day of the year is included

#     year_ago = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)

    

#     # Perform a query to retrieve the data and precipitation scores

#     results_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()



#     # Convert list of tuples into normal list

#     precipitation_dict = dict(results_precipitation)



#     return jsonify(precipitation_dict)

@app.route("/api/v1.0/precipitation")

def precipitation():

    """List of dates and precipitation observations from the last year"""

#Query for the dates and pcrp NOT temperature observations from the last year.

#Convert the query results to a Dictionary using date as the key and tobs as the value.

#Return the JSON representation of your dictionary.

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    rain = session.query(measurement.date, measurement.prcp).\

        filter(measurement.date > last_year).\

        order_by(measurement.date).all()



    prcp_totals = []

    for result in rain:

        row = {}

        row["date"] = rain[0]

        row["prcp"] = rain[1]

        prcp_totals.append(row)



    return jsonify(prcp_totals)



@app.route("/api/v1.0/stations")

def stations():

    stations_query = session.query(station.name, station.station)

    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)

    return jsonify(stations.to_dict())



def tobs():

    """List of Temperature Observations (tobs) for the previous year"""



    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temperature = session.query(measurement.date, measurement.tobs).\

        filter(measurement.date > last_year).\

        order_by(measurement.date).all()



    temp_totals = []

    for result in temperature:

        row = {}

        row["date"] = temperature[0]

        row["tobs"] = temperature[1]

        temp_totals.append(row)



    return jsonify(temp_totals)



@app.route("/api/v1.0/<start>")

def option1(start):



    start_date= dt.datetime.strptime(start, '%Y-%m-%d')

    last_year = dt.timedelta(days=365)

    start = start_date-last_year

    end =  dt.date(2017, 8, 23)

    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\

        filter(measurement.date >= start).filter(measurement.date <= end).all()

    trip = list(np.ravel(trip_data))

    return jsonify(trip)



@app.route("/api/v1.0/<start>/<end>")

def option2(start,end):



    start_date= dt.datetime.strptime(start, '%Y-%m-%d')

    end_date= dt.datetime.strptime(end,'%Y-%m-%d')

    last_year = dt.timedelta(days=365)

    start = start_date-last_year

    end = end_date-last_year

    trip_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\

        filter(measurement.date >= start).filter(measurement.date <= end).all()

    trip = list(np.ravel(trip_data))

    return jsonify(trip)



if __name__ == "__main__":

    app.run(debug=True)