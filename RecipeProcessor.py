import pymongo
from constant.ProofIcon import ProofIcon
from constant.Glass import Glass
from constant.Skill import Skill
from constant.RowName import RowName as rn
from constant.FieldName import FieldName as fn
from bson import ObjectId
from config.Config import Config

class RecipeProcessor:
    def __init__(self):
        self.MONGODB_HOST = Config.MONGODB_HOST
        self.MONGODB_PORT = Config.MONGODB_PORT
        self.MY_CLIENT = pymongo.MongoClient(self.MONGODB_HOST, self.MONGODB_PORT)
        self.DB = self.MY_CLIENT[Config.DB_NAME]
        self.CSV_PATH = Config.CSV_PATH
        self.JSON_PATH = Config.JSON_PATH

    def get_default_recipe(self, rows, json_outer_data):
        default_recipe = rows[rn.DEFAULT_RECIPE.value].strip()        
                
        if (default_recipe == ""):
            json_outer_data[fn.DEFAULT_RECIPE.value] = None
        else:
            found_default_recipe = self.DB.recipes.find({ "name": default_recipe, "defaultRecipe": { '$ne': None } })
            if (found_default_recipe == None):
                raise Exception('cannot find defaultRecipe: ', default_recipe)
            else: 
                json_outer_data[fn.DEFAULT_RECIPE.value] = ObjectId(default_recipe["_id"])


    def set_base_alcohol(self, rows, json_outer_data):
        base = rows[rn.BASE_ALCOHOL.value].strip()
        found_base = self.DB.bases.find_one({ "name" : base })
        if (found_base == None):
            raise Exception('cannot found base. base name is ', base)              
        else:                 
            json_outer_data[fn.BASE_ALCOHOL.value] = ObjectId(found_base["_id"])


    def set_skill(self, rows, json_outer_data):
        skill = rows[rn.SKILL.value].strip()

        if (skill == "쉐이크" ):
            json_outer_data[fn.SKILL.value] = Skill.Shake.value 
        elif(skill == "블렌드"):
            json_outer_data[fn.SKILL.value] = Skill.Blend.value 
        elif(skill == "빌드"):
            json_outer_data[fn.SKILL.value] = Skill.Build.value             
        elif(skill == "스터"):
            json_outer_data[fn.SKILL.value] = Skill.Stir.value
        elif(skill == "플로트"):
            json_outer_data[fn.SKILL.value] = Skill.Float.value
        else:
            raise Exception('Invalid skill value: {0}. Please insert value among 쉐이크, 블렌드, 빌드, 스터, 플로트'.format(skill))

    def set_glass(self, rows, json_outer_data):
        glass = rows[rn.GLASS.value].strip()
        if (glass == "칵테일" ):
            json_outer_data[fn.GLASS.value] = Glass.Cocktail.value 
        elif(glass == "하이볼"):
            json_outer_data[fn.GLASS.value] = Glass.Highball.value
        elif(glass == "온더락"):
            json_outer_data[fn.GLASS.value] = Glass.OnTheRock.value  
        elif(glass == "샴페인"):
            json_outer_data[fn.GLASS.value] = Glass.Champagne.value 
        elif(glass == "리큐어"):
            json_outer_data[fn.GLASS.value] = Glass.Liqueur.value             
        elif(glass == "마가리따"):
            json_outer_data[fn.GLASS.value] = Glass.Margarita.value
        elif(glass == "필스너"):
            json_outer_data[fn.GLASS.value] = Glass.Pilsner.value    
        elif(glass == "소서샴페인"):
            json_outer_data[fn.GLASS.value] = Glass.SaucerChampagne.value
        else: 
            raise Exception('Invalid glass value: {0}. Please insert value between 칵테일, 하이볼, 온더락, 샴페인, 리큐어, 마가리따, 필스너 and 소서샴페인'.format(glass))

    def set_ingredient_info(self, rows, json_outer_data):
        json_ingredient_list = []
        alcohol_percent = 0
        total_ML = 0
        for i in range(1, 6): 
            json_ingredient_data = {}
                    
            index = str(i)
            if (rows[rn.INGREDIENT.value + index] == ""):
                break
                    
            # ingredientId null인 경우
            ingredientName = rows[rn.INGREDIENT.value + index].strip()
            foundIngredient = self.DB.ingredients.find_one({ "name" : ingredientName })
            if (foundIngredient == None): 
                raise Exception('cannot found ingredient. Ingredinet name is ', ingredientName) 
            else: 
                json_ingredient_data[fn.INGREDIENT.value] = ObjectId(foundIngredient["_id"]) # objectId find로 가져와서 넣어줌
                    
            quantity = float(rows[rn.QUANTITY.value + index].strip())
            proof = float(rows[rn.PROOF.value + index].strip())
            json_ingredient_data[fn.QUANTITY.value] = quantity
            json_ingredient_data[fn.UNIT.value] = rows[rn.UNIT + index].strip()
                    
            if (json_ingredient_data[fn.QUANTITY.value] != 0): 
                alcohol_percent +=  quantity * proof
                        
            if (json_ingredient_data[fn.UNIT.value] == "ml"): 
                total_ML += quantity
            elif (json_ingredient_data[fn.UNIT.value] == "tsp"):
                total_ML += quantity * 5
            elif (json_ingredient_data[fn.UNIT.value] == "dashes"):
                total_ML += quantity * 0.2
            elif (json_ingredient_data[fn.UNIT.value] == "ea"):
                total_ML += quantity * 30

            json_ingredient_list.append(json_ingredient_data)
                            
        json_outer_data[fn.INGREDIENT.value] = json_ingredient_list
                
        if (alcohol_percent == 0):
            json_outer_data[fn.PROOF.value] = 0
            json_outer_data[fn.PROOF.value] = ProofIcon.LEVEL_0.value
        elif (total_ML != 0):
            proof = round( alcohol_percent / total_ML)
            json_outer_data[fn.PROOF.value] = proof
            if (0 < proof and proof < 10):
                json_outer_data[fn.PROOF_ICON.value] = ProofIcon.LEVEL_1.value
            elif (0 <= proof and proof < 20):
                json_outer_data[fn.PROOF_ICON.value] = ProofIcon.LEVEL_2.value
            elif (20 <= proof and proof < 30):
                json_outer_data[fn.PROOF_ICON.value] = ProofIcon.LEVEL_3.value
            else:
                json_outer_data[fn.PROOF_ICON.value] = ProofIcon.LEVEL_4.value

    def set_steps(self, rows, json_outer_data):
        steps = []
        for i in range(1, 5):
            index = str(i)
                    
            if (rows[rn.STEP.value + index] == "") :
                break
                    
            steps.append(rows[rn.STEP.value + index])
                
        json_outer_data[fn.STEP.value] = steps
