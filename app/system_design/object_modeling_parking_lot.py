"""
Design a parking lot - modeled as objects

Requirements -
1) Height restrictions for trucks/cars
2) Time of parking vs cost
3) Access restrictions - handicapped, residents-only, visitors with guest parking, maternity,
 logistics

4) payment
5) entry/exit


class ParkingStructure(object):
    pass


class ParkingSpot(object):
    '''
    It has spot_size variable here, not vehicle_size.
    There is a context to a parking spot which could be apartment parking, beach parking,
    vista point, commercial mall parking, etc. Hence you can name your variables suitably.
    You dont want to solve a global problem, its too difficult to predict.

    Real-life problems have to be solved in a specific context.
    '''
    spot_size in ['compact', 'motor_cycle', 'trailer']

    restrictions in ['handicap', 'maternity']

    time_restrictions captures hourly, daily, etc
    pass


class Vehicle(object):
    '''
    If you start with vehicle class, its a red flag that you can't focus on the main aspect of the
    question.
    This has a size which can go from motorcycle to car to truck.
    '''
    pass


class Customer(object):
    credit_card (also think about square, venmo, cash, debit card)
    name
    parking_spot_number
    There is no notion of customer in payment system. Main system is the payment-interface.


class Transaction(object):
    timestamp

    def process_payment(credit_card):
        pass


class Payment(object):
    pre-payment
    entry/exit time


class ParkingTicket(object):
    entry_time
    exit_time


class PaymentBooth(object):
    ParkingTicket
    Receipt - most important aspect of payment-interface is receipt

ParkingSpots <- has many -- ParkingStructure

Makeit intuitive for real-world non-technical users who know the parking system, but not
necessarily know about technology. In other words, domain experts should be able to easily read
and understand your production code. (eg - modeling data scientists in molecular biology)

If input_data in api is not designed well, users will curse you. They will not want to use your
API. eg -
def pay(payment_request):
    '''
    If you combine cash and credit_card under payment_request, its a very bad design.
    '''
    pass

Take away - Design your APIs from the perspective of how they're going to be used.
Better to have separate methods like pay_cash() and pay_card().

For NFC payment, you need location data. Soon you will see complexity in your code.
If type = 'credit' , location should not be NULL.
You have to realize there is isolation in these cases.
They will blame that the API misguided us.

Impossible to enforce nullability in just the pay() method signature.

You will also have different error responses for pay_card and pay_cash.

"""