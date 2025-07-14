import json
from charisma_common.models import Unit, Faction

def main():
    with open("data/units.json") as f:
        unit_data = json.load(f)
        units = [Unit(**u) for u in unit_data]
        print(f"Loaded {len(units)} units")

    with open("data/factions.json") as f:
        faction_data = json.load(f)
        factions = [Faction(**f) for f in faction_data]
        print(f"Loaded {len(factions)} factions")

if __name__ == "__main__":
    main()
