# cliente-servidor-redesII-20222

Trabalho Prático de Redes de Computadores II - 2022.2

# Objetivo: 

Desenvolver uma aplicação baseada no paradigma cliente-servidor utilizando socket de rede.

# Configuração do ambiente:

## Requisitos

- Instalar [PyAudio](https://pypi.org/project/PyAudio/).
  - Linux: ```sudo apt install python3-pyaudio```
  
## Configuração
- Criação do ambiente virtual:
  - ```virtualenv venv```
- Ativação do ambiente virtual:
  - ```source venv/bin/activate```
- Desativação do ambiente virtual:
  - ```deactivate```
- Instalação dos requisitos:
  - ```pip install -r requirements.txt```
    - Somente para Windows, caso contrário seguir instalação dos requisitos. 

# Execução 

- Configurar ```PYTHONPATH``` para apontar para raiz do projeto.
- Executar ```./run.sh <option>```.
  - Permissão (Linux): ```chmod +x ./run.sh```.
  - Opções: 
    - 1º: ```./run.sh register_server```: para executar o servidor de registro.
    - 2º: ```./run.sh client```: para executar o cliente/servidor de voz.

# Descrição geral:

O trabalho prático da disciplina consiste em desenvolver uma aplicação que simula uma sala virtual de conversa, onde os diferentes usuários registrados podem realizar ligações de voz entre eles. Qualquer usuário registrado pode ligar para outro usuário registrado, permitindo somente conversação entre dois usuários. Para isso, a aplicação deve ter um módulo servidor de registros que contém uma tabela atualizada com dados dos usuários registrados.  

## Descrição do registro de usuários:

Esta parte da aplicação conta com um módulo servidor onde estarão relacionados os dados dos clientes registrados. Segundo mostrado na tabela abaixo, o registro deve conter o nome do usuário, endereço IP e porta que cada um utiliza para a ligação de voz.

| NOME  | ENDEREÇO IP   | PORTA |
| ------- | -------- | -------- |
| João   | 192.168.0.101  | 6000 |  
| Maria   | 192.168.0.121    | 6050 |

## Inicialização e registro do cliente:
 
- Uma vez iniciado o servidor de registro, ele fica aguardando pedidos de conexão dos clientes.
- A aplicação cliente depois de inicializada e estabelecida a conexão com o servidor de registro, envia uma mensagem de registro informando o seu nome, IP e porta.
- Quando o servidor recebe os dados do novo usuário:
  - se o usuário não está registrado, adiciona o novo usuário à tabela de registro, e envia uma mensagem de confirmação de registro para o novo usuário.
  - caso o usuário indique um nome que já está registrado, o servidor deve notificar ao usuário.

### Consulta de registro:

- O módulo cliente deve permitir consultar ao servidor de registros o endereço IP e porta relativos a um usuário conhecido. Para isso, o módulo cliente envia uma mensagem de consulta com o nome do usuário desejado e recebe do servidor de registro uma mensagem resposta informando o endereço IP e porta associados ao nome indicado.
- Caso um usuário indique um nome que não está no servidor de registros, o servidor deve notificar ao usuário.

### Encerramento da conexão e atualização da tabela de registro:

- Quando o cliente deseja encerrar sua execução, primeiro avisa ao servidor enviando uma mensagem de fechamento da conexão com sua identificação e depois finaliza a execução.
- O servidor quando recebe a mensagem de fechamento da conexão, identifica o nome do emissor e apaga os seus dados da tabela de registro.

### Outros requisitos da aplicação para o registro:

- A identificação do servidor de registro (endereço IP) deverá ser informada ao módulo cliente pelo usuário da aplicação. Ou seja, você conhece o endereço IP e vai passá-lo ao cliente.
- O servidor de registros deve usar a porta 5000 para a comunicação com os clientes.
- A troca de mensagens deve ser feita utilizando o protocolo TCP.
- A conexão TCP deve permanecer aberta até fechar a aplicação.
- O servidor deve listar na tela os usuários registrados, sempre que adicionar um novo usuário.
- Os módulos cliente e servidor devem imprimir na tela todas as mensagens enviadas e recebidas.

## Descrição do serviço de ligação de áudio:

- A aplicação de ligação também deve ser desenvolvida seguindo o paradigma cliente-servidor, então contém um módulo servidor e um cliente. O módulo cliente deve consultar o servidor de registro para conhecer os dados de conexão do usuário destino de uma ligação de áudio. Ou seja, o módulo cliente atua como cliente tanto do servidor de registro quanto do servidor de ligação.
- Qualquer usuário registrado pode ligar para outro usuário registrado, permitindo somente conversação entre dois usuários.
- Qualquer um dos usuários que participam de uma ligação pode encerrar a ligação.
- O estabelecimento da ligação deve ser feito utilizando-se o protocolo UDP.
- Os módulos cliente e servidor devem imprimir na tela todas as mensagens enviadas e recebidas (“convite”, “resposta_ao_convite”, “encerrar_ligação”).

### O módulo cliente deve:

- Ao iniciar, deve inicializar o socket UDP através do qual enviará as mensagens UDP para o módulo servidor de ligações do usuário com o qual se deseja realizar a ligação.
- O módulo cliente usa sua funcionalidade do cliente de registro para consultar o endereço IP do outro usuário.  Para isso, deve usar a facilidade “consulta” do módulo cliente de registro especificando o destinatário da ligação.
- Quando o cliente recebe a resposta com o endereço IP destino, é estabelecida uma chamada UDP com o par da ligação e é enviada uma mensagem de “convite”. Essa chamada UDP é realizada para o módulo servidor de ligação que está aguardando a chegada de mensagens UDP. Na mensagem “convite” é enviado o nome de usuário de quem está iniciando a ligação, além de seu próprio endereço IP e a porta usada para receber as mensagens UDP. 
- Quando recebe uma “resposta_ao_convite”, caso seja “rejeitado”, imprimir na tela a mensagem  “usuário destino ocupado”, caso seja “aceito”, inicia a coleta e transmissão do sinal de áudio pela porta UDP.
- Quando um usuário deseja encerrar a ligação envia uma mensagem “encerrar_ligação” para o servidor de ligação e para de transmitir áudio.
- Quando recebe a mensagem “encerrar_ligação”, para a transmissão de áudio.


### O módulo servidor deve:
- Ao iniciar, o módulo servidor da aplicação de ligação inicializa um servidor de socket UDP usando a porta 6000 e fica esperando pela chegada de mensagens UDP.
- Quando o servidor recebe um “convite” de ligação, é mostrado o convite na tela e o usuário pode aceitar ou recusar a ligação. 
- O módulo servidor responde ao “convite” com uma mensagem “resposta_ao_convite” e nela envia a palavra “aceito” ou “rejeitado” segundo indicado pelo usuário.
- Também, caso receba um convite de ligação e já esteja em uma conversa com outro cliente, não é mostrado o convite ao usuário e envia uma “resposta_ao_convite” com a palavra “rejeitado”, assim quem inicia a ligação é notificado de que o usuário destino está ocupado. A mensagem “resposta_ao_convite” é enviada usando os dados de endereço recebidos no “convite”. 
- Quando um usuário deseja encerrar a ligação envia uma mensagem “encerrar_ligação” para o cliente da aplicação de ligação e para de transmitir áudio.
- Quando recebe a mensagem “encerrar_ligação”, para a transmissão de áudio.

