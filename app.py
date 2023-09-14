from model import *
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading


app = Flask (__name__)
"""
@app.route("/")
def index():
   konobari = session.query(Konobari).all()
   items = []
   for item in konobari:
        items.append(
            {      
                "id": item.id,
                "ime": item.ime,
                "prezime": item.prezime,
                
                "broj_stola": item.broj_stola
            }
        )
   return json.dumps(items)

   @app.route("/konobari/add")
   def add_konobari ():
        ime = request.args.get("ime")
        prezime = request.args.get("prezime")
        
        broj_stola = request.args.get("broj_stola")
        konobari = Konobari(ime=ime, prezime=prezime, broj_stola=broj_stola)
        session.add(konobari)
        session.commit()
        return "{'message': 'Dodan novi konobar u bazu.'}"

"""

socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)


producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    api_version=(0, 10, 2),
    value_serializer=json_serializer
)

consumer = KafkaConsumer(
    'konobari',
    bootstrap_servers=['kafka:9092'],
    api_version=(0, 10, 2),
    value_deserializer=json_deserializer,
    group_id='test-group',
    auto_offset_reset='earliest'
)

kafka_thread = None


@app.route("/")
def index ():
    konobari = session.query(Konobari).all()
    return render_template('konobari.html', konobari=konobari)

@app.route("/konobari/delete/<int:id>", methods=["DELETE"])
def delete_konobari(id):
    # ID se sada prenosi putem URL-a
    # Dohvati objekt Razred sa navedenim ID-om
    konobari = session.query(Konobari).get(id)

    if konobari:  # ako Razred s ovim ID-om postoji
        session.delete(konobari)
        session.commit()
        # Uspješno izbrisano
        return jsonify({'message': f'Konobar sa ID {id} je izbrisan.'}), 200
    else:
        # Nema Razreda s ovim ID-om
        return jsonify({'message': f'Nema konobara s ID {id}.'}), 404

@app.route("/konobari/<int:id>", methods=["GET"])
def get_konobari(id):
    konobari = region.get_or_create(
        f'Konobari:{id}', 
        creator=lambda: session.query(Konobari).get(id),
        expiration_time=60  
    )
    if konobari:
        return jsonify([{"id": konobari.id, "ime": konobari.ime, "prezime": konobari.prezime, "broj_stola": konobari.broj_stola}]), 200
    else:
        return jsonify({'message': f'Nema konobara s ID {id}.'}), 404

@app.route("/konobari/edit", methods=["PUT"])
def edit_konobari():
    id = request.form.get("id")
    ime = request.form.get("ime")
    prezime = request.form.get("prezime")
    
    broj_stola = request.form.get("broj_stola")

    if id:  
        konobari = session.query(Konobari).get(id)
        if konobari:  
            if ime: 
                konobari.ime = ime
            if prezime: 
                konobari.prezime = prezime
            
            if broj_stola: 
                konobari.broj_stola = broj_stola
            
            session.commit()

            producer.send("konobari", [{"id": konobari.id, "ime": konobari.ime, "prezime": konobari.prezime, "broj_stola": konobari.broj_stola}])
            producer.flush()

            # Uspješno ažurirano
            return jsonify({'message': f'Konobar sa ID {id} je ažuriran.'}), 200
        else:
            # Nema konobara s ovim ID-om
            return jsonify({'message': f'Nema konobara s ID {id}.'}), 404
    else:
        # Nije pružen ID
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/konobari/add", methods=["POST"])
def add_konobari():
    # Dohvati ime,prezime,email,broj
    ime = request.form.get("ime")
    prezime = request.form.get("prezime")
    
    broj_stola = request.form.get("broj_stola")
    
    # Dodaj novog zaposlenika
    konobari = Konobari(ime=ime, prezime=prezime, broj_stola=broj_stola)
    session.add(konobari)
    session.commit()

    producer.send("konobari", [{"id": konobari.id, "ime": konobari.ime, "prezime": konobari.prezime, "broj_stola": konobari.broj_stola}])
    producer.flush()

    # Dobra je praksa vratiti ispravan JSON zahtjev
    return jsonify({'message': 'Dodan novi konobar u bazu.'})

@socketio.on('connect', namespace='/kafka')
def connect():
    global kafka_thread
    if kafka_thread is None or not kafka_thread.is_alive():
        kafka_thread = threading.Thread(target=kafka_consumer)
        kafka_thread.start()

def kafka_consumer():
    for poruka in consumer:
        konobari = poruka.value
        socketio.emit('data', {'konobari': konobari}, namespace='/kafka')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
    