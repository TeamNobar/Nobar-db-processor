from enum import Enum 

class FieldName(Enum):
    NAME = 'name'
    EN_NAME = 'enName'
    DEFAULT_RECIPE = 'defaultRecipe'
    VERSION = 'version'
    BASE_ALCOHOL = 'base'
    SKILL = 'skill'
    GLASS = 'glass'
    INGREDIENT = 'ingredient'
    QUANTITY = 'quantity'
    PROOF = 'proof'
    PROOF_ICON = 'proofIcon'
    UNIT = 'unit'
    STEP = 'steps'

    def __str__(self):
        return str(self.value)