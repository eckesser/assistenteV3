# Importando as bibliotecas necessárias
import json
import time
import random

# Importando a classe 'KeyPresser' do módulo 'keypresser'
from .keypresser import KeyPresser

# Definindo a classe 'KeyManager720'
class KeyManager720:
    # Método de inicialização
    def __init__(self, json_path):
        # Armazenando o caminho do arquivo JSON
        self.json_path = json_path
        # Carregando os dados do arquivo JSON
        self.key_data = self.load_json()
    
    # Método para carregar os dados do arquivo JSON
    def load_json(self):
        with open(self.json_path, 'r') as f:
            return json.load(f)

    # Método para pressionar as teclas com base nos dados carregados
    def press_keys(self):
        for key, value in self.key_data.items():
            if value:  # Verifica se o valor não é nulo
                # Criando uma instância da classe 'KeyPresser'
                key_presser_instance = KeyPresser(key, self.key_data)
                # Pressionando a tecla usando a instância
                key_presser_instance.press()
                # Adicionando um atraso de 0.5 segundos entre as execuções
                time.sleep(0.5)
                # Verifica se a chave é 'weapon_poison_key' ou 'necro_mage_key'
                if key in ['weapon_poison_key', 'necro_mage_key']:
                    self.wait_random_time(720)

    # Método para esperar um tempo aleatório com base em 'base_time'
    def wait_random_time(self, base_time):
        # Calculando um atraso aleatório
        random_delay = base_time * 0.1
        # Calculando o tempo total de espera
        wait_time = base_time + random.uniform(-random_delay, random_delay)
        # Espera pelo tempo calculado
        time.sleep(wait_time)

    # Método principal para executar a classe
    def run(self):
        # Pressionando as teclas uma vez
        self.press_keys()
        # Loop infinito para continuar pressionando as teclas
        while True:
            self.press_keys()

# Criando uma instância da classe 'KeyManager720' e iniciando-a
manager = KeyManager720('Json/ulti.json')  # Caminho atualizado para o arquivo JSON
manager.run()
