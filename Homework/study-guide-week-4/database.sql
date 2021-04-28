-- NOTE that sqlalchemy/database.sql is a symbolic link to sql/database.sql. ALL changes will be reflected in the sqlalchemy assessment.

CREATE TABLE brands (
    brand_id VARCHAR(5) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    founded INTEGER,
    headquarters VARCHAR(50),
    discontinued INTEGER
);

CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    brand_id VARCHAR(5) REFERENCES brands(brand_id) NOT NULL,
    name VARCHAR(50) NOT NULL
);

INSERT INTO brands (brand_id, name, founded, headquarters, discontinued)
VALUES ('for', 'Ford', 1903, 'Dearborn, MI', NULL),
('chr', 'Chrysler', 1925, 'Auburn Hills, Michigan', NULL),
('cit', 'Citroen', 1919, 'Saint-Ouen, France', NULL),
('hil', 'Hillman', 1907, 'Ryton-on-Dunsmore, England', 1981),
('che', 'Chevrolet', 1911, 'Detroit, Michigan', NULL),
('cad', 'Cadillac', 1902, 'New York City, NY', NULL),
('bmw', 'BMW', 1916, 'Munich, Bavaria, Germany', NULL),
('aus', 'Austin', 1905, 'Longbridge, England', 1987),
('fai', 'Fairthorpe', 1954, 'Chalfont St Peter, Buckinghamshire', 1976),
('stu', 'Studebaker', 1852, 'South Bend, Indiana', 1967),
('pon', 'Pontiac', 1926, 'Detroit, MI', 2010),
('bui', 'Buick', 1903, 'Detroit, MI', NULL),
('ram', 'Rambler', 1901, 'Kenosha, Washington', 1969),
('ply', 'Plymouth', 1928, 'Auburn Hills, Michigan', 2001),
('tes', 'Tesla', 2003, 'Palo Alto, CA', NULL);

INSERT INTO models (year, brand_id, name) VALUES
(1909, 'for', 'Model T'),
(1926, 'chr', 'Imperial'),
(1948, 'cit', '2CV'),
(1950, 'hil', 'Minx Magnificent'),
(1953, 'che', 'Corvette'),
(1954, 'che', 'Corvette'),
(1954, 'cad', 'Fleetwood'),
(1955, 'che', 'Corvette'),
(1955, 'for', 'Thunderbird'),
(1956, 'che', 'Corvette'),
(1957, 'che', 'Corvette'),
(1957, 'bmw', '600'),
(1958, 'che', 'Corvette'),
(1958, 'bmw', '600'),
(1958, 'for', 'Thunderbird'),
(1959, 'aus', 'Mini'),
(1959, 'che', 'Corvette'),
(1959, 'bmw', '600'),
(1960, 'che', 'Corvair'),
(1960, 'che', 'Corvette'),
(1960, 'fai', 'Rockette'),
(1961, 'aus', 'Mini Cooper'),
(1961, 'stu', 'Avanti'),
(1961, 'pon', 'Tempest'),
(1961, 'che', 'Corvette'),
(1962, 'pon', 'Grand Prix'),
(1962, 'che', 'Corvette'),
(1962, 'stu', 'Avanti'),
(1962, 'bui', 'Special'),
(1963, 'aus', 'Mini'),
(1963, 'aus', 'Mini Cooper S'),
(1963, 'ram', 'Classic'),
(1963, 'for', 'E-Series'),
(1963, 'stu', 'Avanti'),
(1963, 'pon', 'Grand Prix'),
(1963, 'che', 'Corvair 500'),
(1963, 'che', 'Corvette'),
(1964, 'che', 'Corvette'),
(1964, 'for', 'Mustang'),
(1964, 'for', 'Galaxie'),
(1964, 'pon', 'LeMans'),
(1964, 'pon', 'Bonneville'),
(1964, 'pon', 'Grand Prix'),
(1964, 'ply', 'Fury'),
(1964, 'stu', 'Avanti'),
(1964, 'aus', 'Mini Cooper');


-- Insert a Brand

INSERT INTO brands (brand_id, name, founded, headquarters, discontinued)
    VALUES ('sub', 'Subaru', 1953, 'Tokyo, Japan', NULL);


-- Insert Models

INSERT INTO models (year, brand_id, name)
    VALUES (2015, 'che', 'Malibu'),
           (2015, 'sub', 'Outback');

-- Create an Awards Table

CREATE TABLE awards (award_id SERIAL PRIMARY KEY,
                     year INTEGER NOT NULL,
                     winner_id INTEGER NULL REFERENCES models(model_id),
                     name VARCHAR(50) NOT NULL);

-- Insert Awards

SELECT model_id
    FROM models
    WHERE year = 2015
    AND brand_id LIKE 'che'
    AND name LIKE 'Malibu';

SELECT model_id
    FROM models
    WHERE year = 2015
    AND brand_id LIKE 'sub'
    AND name LIKE 'Outback';

INSERT INTO awards (winner_id, name, year)
    VALUES (47, 'IIHS Safety Award', 2015),
           (48, 'IIHS Safety Award', 2015);

INSERT INTO awards (name, year)
    VALUES ('Best in Class', 2015);

