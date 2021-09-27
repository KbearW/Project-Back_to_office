class User():
    """Customer of Uber Melon"""

    def __init__(self, name, zipcode, creditcard):
        """initialize user"""

        self.name = name
        self.zipcode = zipcode
        self.creditcard = creditcard


def charge_purchase(user, purchase_total):
    """Charge a customer for purchase of price total"""

    tax = calculate_tax(user, purchase_total)
    total_with_tax = purchase_total + tax

    ### Add code to charge user's credit card

    print(total_with_tax, " has been charged to your credit card")


def calculate_tax(user, total):
    """Calculate sales tax"""

    tax_rate = get_tax_rate(user)
    tax = total * tax_rate
    return tax


def get_tax_rate(user):
    """Return the tax rate for a given user."""

    state_tax_rates = {'CA': .075, 'TX': .0625, 'AK': 0, 'HI': .04}
    state = get_state_from_zipcode(user.zipcode)
    tax_rate = state_tax_rates[state]
    return tax_rate


def get_state_from_zipcode(zipcode):
    """Return the state for a given zipcode"""

    zipcode_states = { 94131: 'CA', 94102: 'CA', 77551: 'TX'}
    state = zipcode_states['zipcode']    # there is an error on this line
    return state



if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    customer123 = User("Mel", 94102, "Visa")
    charge_purchase(customer123, 400)
