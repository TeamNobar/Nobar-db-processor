import traceback
from RecipeProcessor import RecipeProcessor
from bson import json_util
import csv
from constant.RowName import RowName as rn
from constant.FieldName import FieldName as fn

def main():
    processor = RecipeProcessor()
    try:
        json_list = []
        with open(processor.CSV_PATH, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                json_outer_data = {}
                json_outer_data[fn.NAME.value] = row[rn.NAME.value].strip()
                json_outer_data[fn.EN_NAME.value] = row[rn.EN_NAME.value].strip()            
                json_outer_data[fn.VERSION.value] = row[rn.VERSION.value].strip()

                processor.set_base_alcohol(row, json_outer_data)
                processor.set_skill(row, json_outer_data)              
                processor.set_glass(row, json_outer_data)              
                processor.set_ingredient_info(row, json_outer_data)
                
                processor.set_steps(row, json_outer_data)
                json_list.append(json_outer_data)
                
            processor.DB.recipes.insert_many(json_list) 
            
    except Exception as e:      
        print(e)    
        print(traceback.format_exc())
        
    finally:    
        with open(processor.JSON_PATH, "w",  encoding='utf-8') as jsonf:
            jsonf.write(json_util.dumps(json_list, indent=4, ensure_ascii = False))

if __name__ == "__main__":
    main()
