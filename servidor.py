from flask import Flask, request, jsonify, send_file
import subprocess
from pathlib import Path
import logging
import threading
import time
import base64
import os

app = Flask(__name__)

# Configurações de log
logging.basicConfig(level=logging.INFO)

# Diretório de saída e configurações
OUTPUT_DIR = Path("/app/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MAX_CHAR = 100000
VOICES = {
    "faber": "pt_BR-faber-medium",
    "edresson": "pt_BR-edresson-low"
}

# Carrega a API Key e tempo de expiração do arquivo do ambiente
API_KEY = os.getenv("API_KEY")

try:
    # Carrega e converte o tempo de expiração para um inteiro, com valor padrão de 30 minutos
    DELETE_FILE_MINUTES = int(os.getenv("DELETE_FILE_MINUTES", "30"))
except ValueError:
    logging.warning("DELETE_FILE_MINUTES inválido, usando 30 minutos como padrão.")
    DELETE_FILE_MINUTES = 30  # Valor padrão em caso de erro na conversão

DELETE_FILE_SECONDS = DELETE_FILE_MINUTES * 60  # Conversão para segundos
logging.info(f"Tempo de expiração definido: {DELETE_FILE_MINUTES} minutos")

def validate_request_data(data):
    """Valida e sanitiza os parâmetros recebidos na requisição."""
    texto = data.get("texto")
    saida = data.get("saida")
    voz = data.get("voz", "faber").lower()
    base64_encode = data.get("base64", "false").lower() == "true"
    formato = data.get("formato", "mp3").lower()

    errors = []
    if not texto or not saida:
        errors.append("Parâmetros 'texto' e 'saida' são obrigatórios.")
    if voz not in VOICES:
        errors.append(f"Voz inválida. Opções: {', '.join(VOICES.keys())}")
    if len(texto) > MAX_CHAR:
        errors.append(f"O 'texto' excede o limite de {MAX_CHAR} caracteres.")
    
    # Retorna os dados sanitizados ou os erros
    return {
        "texto": texto,
        "saida": Path(saida).stem,
        "voz": VOICES[voz],
        "base64_encode": base64_encode,
        "formato": formato
    }, errors

@app.route('/audio', methods=['POST'])
def generate_audio():
    # Validação da API Key
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Acesso negado: API Key inválida"}), 403

    # Valida e sanitiza os dados
    data, errors = validate_request_data(request.get_json())
    if errors:
        return jsonify({"error": " ".join(errors)}), 400

    output_path = OUTPUT_DIR / f"{data['saida']}.{data['formato']}"
    
    # Geração do áudio usando o subprocess com parâmetros seguros
    command = [
        "piper", "--model", data["voz"], "--output_file", str(output_path)
    ]
    try:
        subprocess.run(command, input=data["texto"], text=True, check=True, capture_output=True)
        logging.info(f"Áudio gerado: {output_path}")

        # Manipulação base64 ou retorno direto do arquivo
        if data["base64_encode"]:
            with open(output_path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
            threading.Thread(target=delete_file_after_delay, args=(output_path,)).start()
            return jsonify({"message": "Áudio gerado com sucesso", "audio": audio_base64}), 200

        threading.Thread(target=delete_file_after_delay, args=(output_path,)).start()
        return send_file(output_path, mimetype=f"audio/{data['formato']}", as_attachment=False)

    except subprocess.CalledProcessError as e:
        logging.error(f"Erro na geração do áudio: {e.stderr}")
        return jsonify({"error": "Erro ao gerar o áudio", "details": e.stderr}), 500

def delete_file_after_delay(file_path):
    """Remove o arquivo após o tempo especificado em DELETE_FILE_SECONDS."""
    logging.info(f"Aguardando {DELETE_FILE_SECONDS} segundos para deletar o arquivo.")
    time.sleep(DELETE_FILE_SECONDS)
    try:
        file_path.unlink(missing_ok=True)
        logging.info(f"Arquivo removido após {DELETE_FILE_MINUTES} minutos: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao remover o arquivo: {e}")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
