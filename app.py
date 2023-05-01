import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")

def precipitation():

    """Return a list of all station names"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    date_precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()

    precipitation = {date: prcp for date, prcp in date_precipitation}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    """Return a list of all station names"""
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    """Return a list of all station names"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    session.close()

    all_temperatures = list(np.ravel(results))

    return jsonify(all_temperatures)

@app.route("/api/v1.0/temp/<start>")
def stats(start=None):

    """Return a list of all station names"""
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= dt.datetime.strptime(start,"%m/%d/%Y")).all()
    session.close()

    all_stats = list(np.ravel(results))

    return jsonify(all_stats)

@app.route("/api/v1.0/temp/<start>/<end>")
def stats2(start=None, end=None):

    """Return a list of all station names"""
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= dt.datetime.strptime(start,"%m/%d/%Y")).\
    filter(Measurement.date <= dt.datetime.strptime(end,"%m/%d/%Y")).all()

    session.close()

    all_stats = list(np.ravel(results))

    return jsonify(all_stats)

if __name__ == '__main__':
    app.run(debug=True)
