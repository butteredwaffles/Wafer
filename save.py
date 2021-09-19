from dataclasses import dataclass
from datetime import datetime


@dataclass
class Building:
    amount: int
    total_bought: int
    total_cookies_produced: int
    level: int


# Achievement data is loaded from a server-side file as it is not unique to users.
@dataclass
class Achievement:
    id: int
    name: str
    desc: str


# Upgrade data is also not unique to users.
@dataclass
class Upgrade:
    id: int
    name: str
    desc: str
    cost: int


@dataclass
class Save:
    version: float
    start_time: datetime
    end_time: datetime
    bakery_name: str
    seed: str
    cookies: float
    total_cookies: float
    total_cookie_clicks: float
    total_gcookie_clicks: float
    milk_type: int
    grandma_cookies: float
    buildings: list[Building]
    achievements: list[Achievement]
    upgrades: list[Upgrade]
