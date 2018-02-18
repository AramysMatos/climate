from app import app
from flask import jsonify, request, json
import peewee


db = peewee.SqliteDatabase('banco.db')

#object class climate
class Climate(peewee.Model):
    date = peewee.DateField()
    rainfall = peewee.FloatField()
    temperature = peewee.IntegerField()
    ID = peewee.IntegerField()
	
	#returns a dictionary with weather information
    def to_dict(self):
        return {'ID':self.ID, 'date': self.date, 'rainfall': self.rainfall, 'temperature': self.temperature}

    class Meta:
        database = db
		
try:
    db.create_table(Climate)
except Exception as e:
    pass


#returns all weather data	
@app.route('/climate')
def climates():
    return jsonify([climate.to_dict() for climate in Climate.select()])

#returns a weather data from an id
@app.route('/climate/<int:id_climate>')
def climate(id_climate):
    try:
        climate = Climate.get(id=id_climate)
        return jsonify(climate.to_dict())
    except Climate.DoesNotExist:
        return jsonify({'status': 404, 'mensagem': 'Climate not found'})

		
#adds json weather data
@app.route('/climate', methods=['POST'])		
def new_climate():
    try:	
			
		climate = Climate( date=request.form.get('date'), rainfall=request.form.get('rainfall'), temperature=request.form.get('temperature'))
		climate.save()		
		return jsonify(request.json)

    except Climate.DoesNotSaved:
        return jsonify({'status': 404, 'mensagem': 'Climate not saved'})

#deletes a weather data		
@app.route('/climate/<int:id_climate>', methods=['DELETE'])
def delete_climate(id_climate):
    try:
        climate = Climate(id=id_climate)
        climate.delete_instance()

        return jsonify({'status': 200, 'mensagem': 'Success'})
        
    except Climate.DoesNotExist:
        return jsonify({'status': 404, 'mensagem': 'Climate not found'})
