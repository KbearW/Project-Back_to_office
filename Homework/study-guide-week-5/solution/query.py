"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# This is just a query object, not a result. So you get a
# flask_sqlalchemy.BaseQuery object. If you were to add .one() to the end
# of the query, you'd get a Brand object.

# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table acts as the middleperson in a many-to-many
# relationship. For example, if you want tables A and B to have an M2M
# relationship, you'd create a table AB which just had AB pairings in it.
# Then each of A and B would have a one-to-many relationship to the AB table.
# If, however, there were actual *information* associated with the pairing (so
# the AB table would have more than just id, A_id, and B_id fields), then the
# table that manages the relationship between A and B would be a "middle"
# table, not an association table.


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.get("ram")

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter_by(name='Corvette', brand_id='che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = (Brand.query.filter(Brand.founded == 1903,
                         Brand.discontinued.is_(None))
                 .all())

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = (Brand.query.filter(db.or_(Brand.discontinued.isnot(None),
                                Brand.founded < 1950))
                 .all())

# Get all models whose brand_id is not ``for``.
q8 = Model.query.filter(Model.brand_id != 'for').all()


# Note that any or all of the above queries could also be done using
# db.session.query(ClassName).filter(...).all() or .one()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year, and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models = Model.query.filter_by(year=year).all()

    # print results, if any, or a message saying there are none
    print("\n\n----------------- {year} -----------------".format(year=year))
    if models:
        for model in models:
            result_str = "{brand} {model} ({HQ})"
            print(result_str.format(brand=model.brand.name,
                                    model=model.name,
                                    HQ=model.brand.headquarters))
        print()
    else:
        print("No models from that year in the database\n")

# alternatively, we can use a join:
# def get_model_info(year):
#     """Takes in a year, and prints out each model name, brand name, and brand
#     headquarters for that year using only ONE database query."""

#     results = (db.session.query(Brand.name,
#                                 Model.name,
#                                 Brand.headquarters)
#                          .join(Model)
#                          .filter(Model.year == year)
#                          .all())

#     # print(results, if any, or a message saying there are none)
#     print("\n\n----------------- {year} -----------------".format(year=year))
#     if results:
#         for result in results:
#             brand, model, HQ = result
#             result_str = "{brand} {model} ({HQ})"
#             print(result_str.format(brand=brand,
#                                     model=model,
#                                     HQ=HQ))
#         print()
#     else:
#         print("No models from that year in the database\n")


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    all_brands = Brand.query.all()

    for brand in all_brands:
        print("\n{brand}".format(brand=brand.name))
        print("-" * 25)
        if brand.models:
            for model in brand.models:
                print("  {year} {model}".format(year=model.year,
                                                model=model.name))
        else:
            print("  None\n")
    print()


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    results = Brand.query.filter(Brand.name.ilike('%'+mystr+'%')).all()
    return results


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    results = (Model.query.filter(Model.year >= start_year,
                                  Model.year < end_year)
                          .all())
    return results

