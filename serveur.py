import socket
import threading
from hashlib import sha256
import string

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = "127.0.0.1", 9001
serveur.bind((host, port))
serveur.listen()
clients = []
pseudos = []

all_letters = list(string.ascii_letters + string.punctuation + string.digits + ' ')
alphabets = {}
i = 0

while i != len(all_letters):
	alphabets[i] = all_letters[i]
	i+=1

def crypt(message):
	key = 24
	message_crypt = ''
	for letter in message:

		for index, letter_alpha in alphabets.items():

			if letter == letter_alpha:
				index += key
				message_crypt+= alphabets[index]

			return message_crypt.encode('utf-8')

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			print(f"{pseudos[clients.index(client)]} a envoyer {message}")
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			pseudo = pseudos[index]
			pseudos.remove(pseudo)
			break

def receive():
	while True:
		client, address = serveur.accept()
		print(f"conneter avec {str(address)}")

		client.send("pseudo".encode('utf-8'))
		pseudo = client.recv(1024)

		pseudos.append(pseudo)
		clients.append(client)

		print(f"pseudo du client est {pseudo}")
		broadcast(f"{pseudo} c'est connecter\n".encode('utf-8'))
		client.send("Connecter au serveur\n".encode('utf-8'))

		tread = threading.Thread(target=handle, args=(client,))
		tread.start()

print("serveur running")
receive()