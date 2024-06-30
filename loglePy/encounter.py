# keep the dungeon name, id, and image in the same order
encounterName = ["Algeth'ar Academy", "Brackenhide Hollow", "Halls of Infusion", "Neltharus", "Ruby Life Pools", "Azure Vault", "Nokhud Offensive", "Uldaman"]
encounterId = [62526, 62520, 62527, 62519, 62521, 62515, 62516, 62451]

# used to create an encounter object for easier management
class Encounter():
    def __init__(self, name, Id):
        self.name = name    # name of the encounter
        self.id = Id        # the ID of the encounter
        self.amount = '0'   # dps/hps
        self.parse = '0'    # parse number
        self.rAmount = '0'  # rounded amount
        self.rParse = '0'   # rounded parse
        self.spec = ''      # spec name of the logs being used
        self.numberOfFights  = 0 # the number of logs that include the encounter

    def asdict(self):
        return {
            'name': self.name,
            'id': self.id,
            'amount': self.amount,
            'parse': self.parse,
            'rAmount': self.rAmount,
            'rParse': self.rParse,
            'spec': self.spec,
            'numberOfFights': self.numberOfFights }

def newEncounterObj():
    encounterObj = []
    for i in range(len(encounterName)): encounterObj.append(Encounter(encounterName[i], encounterId[i]).asdict());
    return encounterObj