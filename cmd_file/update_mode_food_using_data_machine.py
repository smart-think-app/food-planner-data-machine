import psycopg2
from psycopg2.extras import RealDictCursor
import data_machine

conn = psycopg2.connect(
    host="localhost",
    database="food-db",
    user="postgres",
    password="postgres", cursor_factory=RealDictCursor)

sql_query = "select * from \"food-info\" where mode is NULL limit 100"

cursor = conn.cursor()
cursor.execute(sql_query)
record = cursor.fetchall()

model_food = data_machine.load_model_food()
for item in record:
    material_level = item["material_level"]
    predict = data_machine.predict_mode_food(model=model_food,
                                             protein=material_level["protein"],
                                             fiber=material_level["fiber"], canxi=material_level["canxi"],
                                             starch=material_level["starch"], fat=material_level["fat"])

    if len(predict) > 0:
        print("Food {} Predict Mode {}".format(item["name"], predict[0]))
        sql_command = "update \"food-info\"  set mode = %s where id = %s "
        cursor.execute(sql_command, (predict[0], item["id"]))
        conn.commit()

cursor.close()
conn.close()
print("...Finished")
