import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Customer, Flight, Pilot



Base = declarative_base()
engine = create_engine('sqlite:///flights.db')


@click.group()
def cli():
    pass


@click.command()
def init_db():
    """Initialize the database."""
    Base.metadata.create_all(engine)
    click.echo('Database initialized.')

Session = sessionmaker(bind=engine)
@click.command()
def add_customer():
    """Add a customer to the database or log in an existing customer."""
    email = click.prompt('Enter your email')

    session = Session()

    # Check if the customer with the provided email already exists
    existing_customer = session.query(Customer).filter_by(email=email).first()

    if existing_customer:
        click.echo(f"Welcome back, {existing_customer.name}!")
        customer_id = existing_customer.id
        list_flights(customer_id)
    else:
        first_name = click.prompt('Enter your first name')
        last_name = click.prompt('Enter your last name')

        new_customer = Customer(name=f"{first_name} {last_name}", email=email)
        session.add(new_customer)
        click.echo('Customer added to the database.')
        session.commit()

        click.echo(f'Welcome, {new_customer.name}!')
        customer_id = new_customer.id

    click.echo(f'Your customer ID: {customer_id}')
    list_flights(customer_id)

@click.command()
def list_customers():
    """List available customers"""
    session = Session()
    customers = session.query(Customer).all()
    print(customers)

def list_flights(customer_id):
    """List available flights."""
    # Add logic to fetch and display available flights
    # You can customize the query based on your model structure
    session = Session()
    flights = session.query(Flight).all()

    click.echo('Available flights:')
    for flight in flights:
        click.echo(f" {flight.plane_name} - {flight.takeoff_time}hrs: {flight.destination}")

    # Handle user input for choosing a flight
    flight_name = click.prompt('Enter the name of the flight you want to book', type=str)
    if flight_name == "exit":
        session.close()
    else:

        selected_flight = session.query(Flight).filter_by(plane_name=flight_name).first()

    if selected_flight:
        click.echo(f"Price for {selected_flight.plane_name}: {selected_flight.price}")

    # Handle user input for payment
    proceed_payment = click.confirm(f'Do you want to proceed with the payment for {selected_flight.plane_name}?')

    if proceed_payment:
    # Add logic to handle payment confirmation and assign the customer to the selected flight
        customer = session.query(Customer).get(customer_id)
    
    # Assuming selected_flight.id is the unique identifier for flights
    customer.flight_id = selected_flight.id
    
    # Append the customer to the selected flight
    selected_flight.customers.append(customer)
    
    # Commit the changes to the database
    session.commit()
    
    click.echo('Payment successful. Customer assigned to the flight.')
     
    # click.echo('Payment canceled.')


    # Display additional details like plane name and pilot
    click.echo(f"Selected Plane: {selected_flight.plane_name}")
    click.echo(f"Pilot: {selected_flight.pilot.name}")
    click.echo(f"takeoff: {selected_flight.takeoff_time}")

    session.close()

# Add commands to the CLI group
cli.add_command(init_db)
cli.add_command(add_customer)
cli.add_command(list_customers)

if __name__ == '__main__':
    cli()
