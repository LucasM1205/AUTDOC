from werkzeug.security import generate_password_hash

# Passwort, das gehasht werden soll
password = "sektretariat123"

# Hash generieren und ausgeben
print(generate_password_hash(password))

#student123
#sektretariat123
#ausschuss123