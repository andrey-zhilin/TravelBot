CREATE TABLE IF NOT EXISTS country(
country_id  VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR ,
currency VARCHAR,
name_en VARCHAR
);

CREATE TABLE IF  NOT EXISTS city(
city_id VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR,
coordinates_lon VARCHAR,
coordinates_lat VARCHAR,
name_en VARCHAR,
country_code VARCHAR,
FOREIGN KEY(country_code) REFERENCES country(country_id) ON DELETE SET NULL
);

CREATE TABLE IF  NOT EXISTS transport_point(
point_id VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR,
iata_type VARCHAR,
flightable BOOLEAN,
name_en VARCHAR,
city_code VARCHAR,
FOREIGN KEY(city_code) REFERENCES city(city_id) ON DELETE SET NULL
);

CREATE TABLE IF  NOT EXISTS airlines(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
name_primary VARCHAR,
name_en VARCHAR, 
iata_code VARCHAR
);

CREATE TABLE IF  NOT EXISTS routes(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
airline_iata VARCHAR,
departure_airport_iata VARCHAR,
arrival_airport_iata VARCHAR,
FOREIGN KEY(airline_iata) REFERENCES airlines(iata_code) ON DELETE SET NULL,
FOREIGN KEY(arrival_airport_iata) REFERENCES transport_point(point_id) ON DELETE SET NULL,
FOREIGN KEY(departure_airport_iata) REFERENCES transport_point(point_id) ON DELETE SET NULL
);
