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
