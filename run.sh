op=$1
register_server=register_server
client=client


if [ $op == $register_server ] 
then
   echo ==== Iniciando servidor de registro ====
   python3 register_server/main.py
else
   echo ==== Iniciando cliente ====
   python3 client/client.py
fi 
