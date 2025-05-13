import hashlib
import json
import time
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Abilita CORS per permettere richieste dal frontend

# File per la persistenza della blockchain
BLOCKCHAIN_FILE = 'car_blockchain.json'

class Block:
    def __init__(self, index, timestamp, car_data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.car_data = car_data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "car_data": self.car_data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "car_data": self.car_data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, block_dict):
        block = cls(
            block_dict["index"], 
            block_dict["timestamp"], 
            block_dict["car_data"], 
            block_dict["previous_hash"]
        )
        block.hash = block_dict["hash"]
        return block

class CarBlockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()
        
        # Se la catena è vuota dopo il caricamento, crea il blocco genesis
        if not self.chain:
            self.create_genesis_block()
            self.save_chain()
        
    def create_genesis_block(self):
        # Crea il blocco iniziale (genesis)
        genesis_block = Block(0, datetime.now().isoformat(), {"message": "Genesis Block"}, "0")
        self.chain.append(genesis_block)
        
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_car_data(self, car_id, car_data):
        # Aggiungi un nuovo blocco con i dati dell'auto
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_timestamp = datetime.now().isoformat()
        new_car_data = {
            "car_id": car_id,
            "data": car_data,
            "recorded_at": new_timestamp
        }
        new_block = Block(new_index, new_timestamp, new_car_data, previous_block.hash)
        
        # Verifica la validità prima di aggiungere
        if self.is_valid_new_block(new_block, previous_block):
            self.chain.append(new_block)
            self.save_chain()  # Salva la catena dopo ogni aggiunta
            return new_block
        return None
    
    def is_valid_new_block(self, new_block, previous_block):
        # Verifica che il blocco sia valido
        if previous_block.index + 1 != new_block.index:
            return False
        if previous_block.hash != new_block.previous_hash:
            return False
        if new_block.calculate_hash() != new_block.hash:
            return False
        return True
    
    def is_chain_valid(self):
        # Verifica l'intera catena
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def get_car_history(self, car_id, date=None):
        # Ottieni la storia di una macchina specifica, opzionalmente filtrata per data
        car_blocks = []
        for block in self.chain:
            if block.index > 0:  # Salta il genesis block
                if block.car_data.get("car_id") == car_id:
                    # Se una data è specificata, filtra per quella data
                    if date:
                        # Estrai la data dal timestamp (il timestamp è in formato ISO)
                        block_date = block.timestamp.split('T')[0]  # Prende solo YYYY-MM-DD
                        if block_date == date:
                            car_blocks.append(block.to_dict())
                    else:
                        # Se nessuna data è specificata, aggiungi tutti i blocchi
                        car_blocks.append(block.to_dict())
        return car_blocks
    

    def get_all_blocks(self):
        return [block.to_dict() for block in self.chain]
    
    def save_chain(self):
        # Salva la blockchain su file
        chain_data = [block.to_dict() for block in self.chain]
        try:
            with open(BLOCKCHAIN_FILE, 'w') as file:
                json.dump(chain_data, file, indent=4)
            print(f"Blockchain salvata in {BLOCKCHAIN_FILE}")
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio della blockchain: {e}")
            return False
    
    def load_chain(self):
        # Carica la blockchain da file
        if os.path.exists(BLOCKCHAIN_FILE):
            try:
                with open(BLOCKCHAIN_FILE, 'r') as file:
                    chain_data = json.load(file)
                    
                self.chain = [Block.from_dict(block_dict) for block_dict in chain_data]
                print(f"Blockchain caricata da {BLOCKCHAIN_FILE} con {len(self.chain)} blocchi")
                
                # Verifica l'integrità della catena caricata
                if not self.is_chain_valid():
                    print("ATTENZIONE: La blockchain caricata non è valida!")
                    self.chain = []  # Resetta la catena se non valida
                    return False
                return True
            except Exception as e:
                print(f"Errore durante il caricamento della blockchain: {e}")
                self.chain = []
                return False
        else:
            print(f"File blockchain {BLOCKCHAIN_FILE} non trovato. Verrà creata una nuova blockchain.")
            return 

# Inizializza la blockchain
blockchain = CarBlockchain()

# API Endpoints
@app.route('/add_car_data', methods=['POST'])
def add_data():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Nessun dato JSON ricevuto"}), 400
        
        required_fields = ['car_id', 'pressure', 'temperature', 'engineOn', 
                          'batteryStatus', 'oilLevel', 'brakesWear', 
                          'fuelLevel', 'mileage', 'fault']
        
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Dati mancanti: {', '.join(missing_fields)}"}), 400
        
        car_id = data['car_id']
        car_data = {
            'pressure': data['pressure'],
            'temperature': data['temperature'],
            'engineOn': data['engineOn'],
            'batteryStatus': data['batteryStatus'],
            'oilLevel': data['oilLevel'],
            'brakesWear': data['brakesWear'],
            'fuelLevel': data['fuelLevel'],
            'mileage': data['mileage'],
            'fault': data['fault']
        }
        
        block = blockchain.add_car_data(car_id, car_data)
        
        if block:
            return jsonify({
                "message": "Dati auto aggiunti con successo", 
                "block": block.to_dict(),
                "blockchain_size": len(blockchain.chain)
            }), 201
        else:
            return jsonify({"error": "Errore nell'aggiunta dei dati"}), 400
    except Exception as e:
        return jsonify({"error": f"Errore del server: {str(e)}"}), 500

@app.route('/get_car_history/<car_id>', methods=['GET'])
def get_history(car_id):
    try:
        # Ottieni il parametro data dalla query string, se presente
        date = request.args.get('date')
        
        history = blockchain.get_car_history(car_id, date)
        return jsonify({
            "car_id": car_id, 
            "history": history,
            "count": len(history),
            "date_filter": date if date else "None"
        })
    except Exception as e:
        return jsonify({"error": f"Errore del server: {str(e)}"}), 500

@app.route('/validate_chain', methods=['GET'])
def validate_chain():
    try:
        is_valid = blockchain.is_chain_valid()
        return jsonify({
            "valid": is_valid,
            "chain_length": len(blockchain.chain)
        })
    except Exception as e:
        return jsonify({"error": f"Errore del server: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def get_status():
    try:
        return jsonify({
            "status": "online",
            "blockchain_size": len(blockchain.chain),
            "genesis_block": blockchain.chain[0].to_dict() if blockchain.chain else None,
            "latest_block": blockchain.get_latest_block().to_dict() if blockchain.chain else None,
            "is_valid": blockchain.is_chain_valid()
        })
    except Exception as e:
        return jsonify({"error": f"Errore del server: {str(e)}"}), 500

if __name__ == "__main__":
    print("Server blockchain avviato su http://localhost:5000")
    print(f"Dimensione blockchain: {len(blockchain.chain)} blocchi")
    app.run(debug=True, port=5000)
