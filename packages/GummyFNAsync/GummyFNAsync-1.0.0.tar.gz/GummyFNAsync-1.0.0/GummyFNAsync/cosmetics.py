from .enums import *


class BRCosmetic:
    """Represents a Fortnite playlist.

        Attributes
        ----------
        raw: :class:`Dict[:class:`str`, Any]`
            Raw data from BenBot (can be used to reconstruct object)
        id: :class:`str`:
            The id of the cosmetic.
        path: :class:`str`:
            The path in the game files where this cosmetic was located.
        icons: :class:`dict`:
            Dictionary containing 3 keys: icon, featured & series.
        name: :class:`str`:
            Display Name of this cosmetic.
        description: :class:`str`:
            The displayed description of this cosmetic.
        short_description: :class:`str`:
            The displayed short description of this cosmetic.
        backend_type: Enum[:class:`BackendType`]:
            The type of this cosmetic in the backend.
        rarity: :class:`str`:
            The displayed rarity of this cosmetic.
        backend_rarity: Enum[:class:`BackendRarity`]:
            The displayed short description of this cosmetic.
        set: :class:`str`:
            The displayed set of this cosmetic.
        set_text: :class:`str`:
            The whole "Part of the ... set" text with the set.
        series: :class:`dict`:
            Dictionary containing 2 keys: name & colors.
        variants: :class:`list`:
            List containing the data of the cosmetics variants.
        gameplay_tags: :class:`list`:
            List containing the gameplay tags of this cosmetic.
        """
    def __init__(self, data: dict) -> None:
        self.data = data
        self.id = data['info']['id']
        self.images = data['images']
        self.name = data['info']['name']
        self.description = data['info']['description']
