from fastapi import FastAPI
from faker import Faker
import random
import hashlib
from datetime import datetime, timedelta
import requests
import uuid
import uvicorn
import json

app = FastAPI(title="Jackpot API")

fake = Faker()

properties = {
    "RLC": "Red Lantern Casino",
    "BMC": "Blue Meridian Casino",
    "GPC": "Glass Palm Casino"
}

game_titles = [
    "88 Fortunes",
    "Buffalo Gold",
    "Wheel of Fortune",
    "Blackjack T1"
]

game_models = [
    "A560X-ST",
    "A600H",
    "Raptor",
    "A-Star Curve",
    "Atlas AINS"
]

manufacturers = [
    "Aristocrat",
    "IGT",
    "AGS",
    "Konami",
    "Light & Wonder"
]

cabinet_types = [
    "UPRIGHT",
    "SLANT",
    "CURVE"
]


def generate_person_id(activeclubid):

    return str(
        int(
            hashlib.md5(
                ("jack" + activeclubid).encode()
            ).hexdigest(),
            16
        ) % 90000 + 10000
    )


def generate_jackpot_record(activeclubid):

    person_id = generate_person_id(
        activeclubid
    )

    property_code = random.choice(
        list(properties.keys())
    )

    property_name = properties[
        property_code
    ]

    jackpot_timestamp = (
        datetime.now()
        - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(1, 12)
        )
    )

    jackpot_amount = round(
        random.choice([
            random.uniform(500, 5000),
            random.uniform(5000, 8000),
            
        ]),
        2
    )

    jackpot_event_id = random.randint(
        10000000000,
        99999999999
    )

    source_person_key = hashlib.md5(
        ("jack" + activeclubid).encode()
    ).hexdigest()

    event_id = hashlib.md5(
        str(uuid.uuid4()).encode()
    ).hexdigest()

    event_group_id = hashlib.md5(
        activeclubid.encode()
    ).hexdigest()

    metadata = {

        "club_key":
            hashlib.md5(
                activeclubid.encode()
            ).hexdigest(),

        "fact_key":
            jackpot_event_id,

        "person_id":
            person_id,

        "person_id_src_cd":
            "jackpot",

        "person_key":
            hashlib.md5(
                person_id.encode()
            ).hexdigest(),

        "property_id":
            property_code
    }

    return {

        "EVENT_TIMESTAMP":
            jackpot_timestamp.isoformat(),

        "EVENT_TIMESTAMP_PROPERTY":
            jackpot_timestamp.isoformat(),

        "EVENT_TIMESTAMP_PROPERTY_TIMEZONE":
            "America/New_York",

        "DURATION":
            0,

        "GAMING_DATE":
            jackpot_timestamp.date().isoformat(),

        "GAMING_DATE_TIMEZONE":
            "America/New_York",

        "SOURCE_PERSON_KEY":
            source_person_key,

        "PERSON_ID":
            person_id,

        "ACTIVE_CLUB_ID":
            activeclubid,

        "SOURCE":
            "CMP",

        "ENTITY":
            "JACKPOT",

        "ACTION":
            "PLAY",

        "ENTITY_ACTION":
            "JACKPOT:PLAY",

        "DETAILS":
            f"Jackpot Win ${jackpot_amount}",

        "EVENT_ID":
            event_id,

        "EVENT_GROUP_ID":
            event_group_id,

        "PROPERTY_NAME":
            property_name,

        "PROPERTY_CODE":
            property_code,

        "PROPERTY_ACCOUNTING_CODE":
            property_code,

        "SF_PROPERTY_ID":
            property_code,

        "PROPERTY_ID":
            property_code,

        "PROPERTY_ADDR1":
            fake.street_address(),

        "PROPERTY_ADDR2":
            fake.secondary_address(),

        "PROPERTY_CITY":
            fake.city(),

        "PROPERTY_STATE":
            fake.state(),

        "PROPERTY_COUNTRY":
            "USA",

        "PROPERTY_POSTAL_CODE":
            fake.postcode(),

        "TRANSACTION_AMOUNT":
            "",

        "PLAYER_VALUE":
            "",

        "JACKPOT_EVENT_ID":
            jackpot_event_id,

        "JACKPOT_ID":
            jackpot_event_id,

        "JACKPOT_IS_SETTLED":
            random.choice(
                [True, False]
            ),

        "JACKPOT_IS_TAXABLE":
            jackpot_amount >= 1200,

        "JACKPOT_WIN_AMOUNT":
            jackpot_amount,

        "JACKPOT_PAID_AMOUNT":
            0,

        "JACKPOT_GAME_MFR":
            random.choice(
                manufacturers
            ),

        "JACKPOT_GAME_MODEL":
            random.choice(
                game_models
            ),

        "JACKPOT_GAME_TITLE":
            random.choice(
                game_titles
            ),

        "JACKPOT_SERIAL_NUMBER":
            f"SN{random.randint(100000,999999)}",

        "JACKPOT_GAME_TYPE":
            random.choice([
                "PROGRESSIVE",
                "VIDEO SLOT",
                "MULTI GAME"
            ]),

        "JACKPOT_IS_LEASED":
            random.choice(
                [True, False]
            ),

        "JACKPOT_LEASE_RATE_TYPE":
            random.choice([
                "FIXED",
                "PERCENTAGE",
                "DAILY"
            ]),

        "JACKPOT_CABINET_TYPE":
            random.choice(
                cabinet_types
            ),

        

        "LOAD_TIMESTAMP":
            datetime.now().isoformat()
    }


@app.get("/v1/jackpot")
async def jackpot():

    api_url = (
        "https://casino-api-ob26.onrender.com/"
        "v1/player-activity"
    )

    response = requests.get(
        api_url
    )

    player_data = response.json()

    unique_activeclubids = []

    seen = set()

    for row in player_data:

        activeclubid = row[
            "ACTIVECLUBID"
        ]

        if activeclubid not in seen:

            seen.add(
                activeclubid
            )

            unique_activeclubids.append(
                activeclubid
            )

        if len(unique_activeclubids) == 50:
            break

    final_records = []

    for activeclubid in unique_activeclubids:

        final_records.append(
            generate_jackpot_record(
                activeclubid
            )
        )

    return final_records


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8008
    )
