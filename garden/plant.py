import math

from .plantData import PlantData


class Plant:
    """
    Class representing a plot space on the garden minigame's grid.
    """
    data: PlantData = None
    """The information for this plant, like maturity rate, name, etc."""
    ticksUntilDecay: int = 0
    """Remaining lifespan of the plant. Note that plants have reduced efficiency at two ticks left of life."""
    ticksUntilMature: int = 0
    """Remaining ticks until plant becomes mature, unlocking 100% of plant benefits and enabling reproduction."""
    isMature: bool = False
    """Notes if the plant is currently mature or not."""
    x: int = 0
    """x coordinate of the plot this plant is located in."""
    y: int = 0
    """y coordinate of the plot this plant is located in."""

    def __init__(self, data: PlantData, lifeTick: int):
        """
        Create a Plant object.

        :param data: The universal plant information.
        :param lifeTick: The current age of this plant.
        :type data: PlantData
        :type lifeTick: int
        """
        # ignore plot modifiers for now
        self.data = data
        self.isMature = self.data.mature <= lifeTick

        if self.isMature:
            self.ticksUntilDecay = math.ceil(
                (100 / (self.data.ageTick + self.data.ageTickR / 2))
                * ((100 - lifeTick) / 100)
            )
        else:
            self.ticksUntilMature = math.ceil(
                (100 / (self.data.ageTick + self.data.ageTickR / 2))
                * ((self.data.mature - lifeTick) / 100)
            )

    def __repr__(self):
        if self.isMature:
            maturity = f"Decays in {self.ticksUntilDecay} ticks"
        else:
            maturity = f"Matures in {self.ticksUntilMature} ticks"
        return f"{self.data.name} ({self.x}, {self.y}) {maturity}"
