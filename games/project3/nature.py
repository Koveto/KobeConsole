class Nature:

    VALID_STATS = [
        "atk",
        "def",
        "spatk",
        "spdef",
        "spe"
    ]

    def __init__(
        self,
        name,
        boosted_stat,
        reduced_stat
    ):

        if boosted_stat is not None:
            if boosted_stat not in Nature.VALID_STATS:
                raise ValueError(
                    f"Invalid boosted stat: {boosted_stat}"
                )

        if reduced_stat is not None:
            if reduced_stat not in Nature.VALID_STATS:
                raise ValueError(
                    f"Invalid reduced stat: {reduced_stat}"
                )

        self.name = name
        self.boosted_stat = boosted_stat
        self.reduced_stat = reduced_stat


HARDY   = Nature("Hardy",   None,    None)
LONELY  = Nature("Lonely",  "atk",   "def")
BRAVE   = Nature("Brave",   "atk",   "spe")
ADAMANT = Nature("Adamant", "atk",   "spatk")
NAUGHTY = Nature("Naughty", "atk",   "spdef")

BOLD    = Nature("Bold",    "def",   "atk")
DOCILE  = Nature("Docile",  None,    None)
RELAXED = Nature("Relaxed", "def",   "spe")
IMPISH  = Nature("Impish",  "def",   "spatk")
LAX     = Nature("Lax",     "def",   "spdef")

TIMID   = Nature("Timid",   "spe",   "atk")
HASTY   = Nature("Hasty",   "spe",   "def")
SERIOUS = Nature("Serious", None,    None)
JOLLY   = Nature("Jolly",   "spe",   "spatk")
NAIVE   = Nature("Naive",   "spe",   "spdef")

MODEST  = Nature("Modest",  "spatk", "atk")
MILD    = Nature("Mild",    "spatk", "def")
QUIET   = Nature("Quiet",   "spatk", "spe")
BASHFUL = Nature("Bashful", None,    None)
RASH    = Nature("Rash",    "spatk", "spdef")

CALM    = Nature("Calm",    "spdef", "atk")
GENTLE  = Nature("Gentle",  "spdef", "def")
SASSY   = Nature("Sassy",   "spdef", "spe")
CAREFUL = Nature("Careful", "spdef", "spatk")
QUIRKY  = Nature("Quirky",  None,    None)

NATURES = {
    nature.name: nature
    for nature in [
        HARDY,
        LONELY,
        BRAVE,
        ADAMANT,
        NAUGHTY,
        BOLD,
        DOCILE,
        RELAXED,
        IMPISH,
        LAX,
        TIMID,
        HASTY,
        SERIOUS,
        JOLLY,
        NAIVE,
        MODEST,
        MILD,
        QUIET,
        BASHFUL,
        RASH,
        CALM,
        GENTLE,
        SASSY,
        CAREFUL,
        QUIRKY
    ]
}