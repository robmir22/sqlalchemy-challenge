import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #""Retrieve the last 12 months of precipitation data""
    date = dt.datetime(2017, 8, 23)
    T12_date = date - dt.timedelta(days=365)
    sel = [measurement.date, measurement.prcp]
    data = session.query(*sel).\
    filter(measurement.date >= T12_date).order_by(measurement.date).all()
    session.close()

    # Convert list of tuples into normal list
    precipitation = list(np.ravel(data))

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations = session.query(station.station, station.name, station.elevation, station.latitude, station.longitude).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations))

    return jsonify(station_list)


if __name__ == '__main__':
    app.run(debug=True)
