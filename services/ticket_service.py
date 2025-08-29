import random
from datetime import datetime, timedelta
from typing import List
from faker import Faker
from models.ticket import Ticket

# --- Internal Helper for Data Generation ---
fake = Faker()
AGENTS = [fake.name() for _ in range(5)]


def _generate_mock_tickets(count: int, version: str) -> List[Ticket]:
    """
    Internal helper function to generate a list of new ticket objects.
    This does NOT interact with the database.
    """
    tickets = []
    for _ in range(count):
        create_date = fake.date_time_between(start_date=datetime(2026, 1, 1), end_date=datetime(2026, 12, 31))
        status = random.choice(["Open", "Resolved"])
        resolved_date = None
        csat = None

        if status == "Resolved":
            max_resolve_date = datetime(2026, 12, 31, 23, 59, 59)
            resolved_date = fake.date_time_between(start_date=create_date, end_date=max_resolve_date)
            if random.random() > 0.5:
                csat = f"{random.randint(70, 100)}%"

        if version == "v2":
            create_date_for_response = int(create_date.timestamp())
            resolved_date_for_response = int(resolved_date.timestamp()) if resolved_date else None
        else:
            create_date_for_response = create_date
            resolved_date_for_response = resolved_date

        ticket_data = {
            "Create Date": create_date_for_response,
            "Status": status,
            "Resolved Date": resolved_date_for_response,
            "Agent": random.choice(AGENTS),
            "CSAT": csat,
            "Description": fake.paragraph(nb_sentences=3),
            "Subject": fake.sentence(nb_words=4).replace('.', ''),
            "Customer Email": fake.email(),
            "endpoint_version": version,
        }
        tickets.append(Ticket.model_validate(ticket_data))
    return tickets


# --- Main Service Function ---
async def get_or_create_tickets_for_version(version: str) -> List[Ticket]:
    """
    Checks if tickets for a specific version exist in the database.
    If they exist, it returns them.
    If not, it generates them, saves them to the DB, and then returns them.
    """
    existing_tickets = await Ticket.find(Ticket.endpoint_version == version).to_list()
    if existing_tickets:
        print(f"Found {len(existing_tickets)} existing tickets for version '{version}'. Returning from DB.")
        return existing_tickets

    print(f"No tickets found for version '{version}'. Generating new ones.")
    number_of_tickets = random.randint(100, 120)
    new_tickets = _generate_mock_tickets(number_of_tickets, version)
    await Ticket.insert_many(new_tickets)
    print(f"Successfully saved {len(new_tickets)} new tickets to the DB for version '{version}'.")
    return new_tickets