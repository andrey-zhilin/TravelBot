CREATE TABLE IF NOT EXISTS country(
country_id  VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR NOT NULL,
name_en VARCHAR,
currency VARCHAR
);

CREATE TABLE IF  NOT EXISTS city(
city_id VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR NOT NULL,
name_en VARCHAR,
coordinates_lon VARCHAR,
coordinates_lat VARCHAR,
FOREIGN KEY(country_code) REFERENCES country(country_id)
);

CREATE TABLE IF  NOT EXISTS transport_point(
point_id VARCHAR NOT NULL PRIMARY KEY,
name_primary VARCHAR NOT NULL,
name_en VARCHAR,
FOREIGN KEY(city_code) REFERENCES city(city_id)
);


