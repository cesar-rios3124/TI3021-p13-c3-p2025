import bcrypt

# 1
inconming_password = input("Ingresa tu contraseña: ").encode("UTD-8")
# 2
salt = bcrypt.gensalt(rounds=12)
# 3
hashed_password = bcrypt.hashpw(password=inconming_password,salt=salt)
print("Contraseña hasheada", hashed_password)
# 4
confirm_password = input("Ingresa nuevamente la contraseña: ").encode("UTF-8")
# 5
if bcrypt.checkpw(confirm_password,hashed_password):
    print("contraseña correcta")
else:
    print("contreaseña incorrecta")
    