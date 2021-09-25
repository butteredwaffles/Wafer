class PlantData:
    """
    Contains information for a single type of plant in the garden minigame.
    """

    name: str = "N/A"
    """The plant's name."""
    id: int = 0
    """The ID of the plant according to save data."""
    unlocked: bool = False
    """Indicates whether this plant has been unlocked or not (i.e. whether its seed has been harvested before)."""
    mutations: list[int] = []
    """Indicates what other plants seeds of this plant type may grow into."""
    children: list[int] = []
    """Indicates what other plants this plant type can spawn via reproduction."""
    cost: int = 0
    """Indicates how many minutes of CPS are required to purchase this seed."""
    ageTick: float = 0.0
    """Indicates how quickly this plant generally ages.
    
    All plants grow from 0-100. ageTick can be anywhere from a low value, like 0.4, to higher values, like 10.
    In essence it is the minimum amount this plant must age per tick."""
    ageTickR: float = 0.0
    """A random amount between 0.0 and this number is chosen to add onto ageTick each tick. See ageTick docs for more
    information on aging."""
    mature: int = 0
    """Indicates the age at which this plant reaches maturity. 
    
    Lower number generally means faster maturation, but ageTick can add more nuance to make this not as
    straightforward."""
    immortal: bool = False
    """Indicates whether this plant ages."""
    fungus: bool = False
    """Indicates if this plant is a fungus."""
    weed: bool = False
    """Indicates if this plant is a weed."""
    plantable: bool = True
    """Indicates if this plant has a seed and is able to be planted."""
