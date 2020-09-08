CREATE TABLE IF NOT EXISTS country(
country_id  VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR ,
currency VARCHAR,
name_en VARCHAR,
);

CREATE TABLE IF  NOT EXISTS city(
city_id VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR,
coordinates_lon VARCHAR,
coordinates_lat VARCHAR,
name_en VARCHAR,
country_code VARCHAR,
FOREIGN KEY(country_code) REFERENCES country(country_id)
);

CREATE TABLE IF  NOT EXISTS transport_point(
point_id VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR,
iata_type VARCHAR,
flightable BOOLEAN,
name_en VARCHAR,
city_code VARCHAR,
FOREIGN KEY(city_code) REFERENCES city(city_id)
);


