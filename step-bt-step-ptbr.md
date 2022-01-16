# Step by step in Portuguese

# 1. Configuração do ambiente

Para criar um ambiente virtual, escolha um diretório onde deseja colocá-lo e execute o módulo venv como um script com o caminho do diretório:

```bash
python3 -m venv tornado-env
```

Isso irá criar o diretório `tornado-env` se ele não existir, e também criará diretórios dentro dele contendo uma cópia do interpretador Python, a biblioteca padrão e diversos arquivos de suporte.

Uma vez criado seu ambiente virtual, você deve ativá-lo.

No Windows, execute:

```bash
tutorial-env\Scripts\activate.bat
```

No Unix ou no MacOS, executa:

```bash
source tutorial-env/bin/activate
```

# 2. R**equirements**

Para este projeto foi criado um arquivo chamado `requirements.txt` contendo o seguinte conteudo:

```bash
tornado
pymongo
bson
```

Para instalar as bibliotecas do arquivo `requirements.txt` basta usar o seguinte comando:

```bash
pip install -r requirements.txt
```

# 3. Criando o servidor Tornado

O primeiro passo é criar uma pasta “*src*” e dentro dela criar um arquivo chamado `app.py`

## 3.1 Hello world in python Tornado

Aqui está um simples exemplo de “Hello, world”  em um web app utilizando o Tornado:

```python
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

## 3.2 Criando nosso primeiro Handler

O primeiro Handler que iremos fazer é o de cadastro de empregados, para isso precisamos inserir as seguintes linhas de código no nosso arquivo `app.py`

```python
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class EmployeeHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("POST")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/employee", EmployeeHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

Primeiramente inserimos um novo endpoint na aplicação ***r”/employee”*** no método `make_app()`:

```python
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/employee", EmployeeHandler) # Aqui!
    ])
```

Feito isso, nos inserimos o EmployeeHandler para lidar com os verbos http, a primeira ação que vamos configurar é a de cadastrar um novo empregado, ou seje, precisamos criar um método POST dentro no nosso Handler:

```python
class EmployeeHandler(tornado.web.RequestHandler):
    def post(self):
        new_employee = json.loads(self.request.body)
        db = database.db_connect()
        x = db.insert_one(new_employee)
        self.write({"Response":"New employee created!"})
```

Vamos explicar um pouco do que está acontecendo nesse método **POST**.

Para que nos possamos ter acesso ao body da requisição onde terá as informações do novo funcionário precisamos fazer o seguinte: (1) foi importado a seguinte biblioteca para ajudar na conversão de json para dict

```python
import json
```

(2) Agora precisamos usar a seguinte linha de código para acessar o body da requisição:

```python
new_employee = json.loads(self.request.body)
```

Pronto! as informações do novo funcionário estão sendo salvas na variável `new_employee` 

Para inserir esse funcionário no banco de dados vamos utilizar o método do `pymongo` chamado `insert_one` depois bastar retornar uma mensagem de sucesso para o usuário.

```python
 x = db.insert_one(new_employee)
 self.write({"Response":"New employee created!"})
```

A gora que já conseguimos adicionar um documento no banco de dados vamos criar um novo método para ler os documentos criados nesse banco de dados:

```python
def get(self):
        db = database.db_connect()
        list_employees = [doc for doc in db.find({},{"_id":0})]
        self.write({"Response": list_employees})
```

Novamente temos que fazer a conecção com o banco de dados com o método `db_connect` , após a contecção ser feita nos precisamos utilizar o método `find()` do `pymongo` para coletar todos os documentos do banco de dados. Depois é só colocar tudo isso em uma lista e mandar para o usuário.

 O próximo passo é criar os métodos GET PUT e DELETE para o endpoint ***r”/employee/:id”*** para isso é necessário criar um novo Handler. Aqui precisamos ter alguns cuidados por conta do “_id” do mongo.

```python
class EmployeesHandler(tornado.web.RequestHandler):
    def get(self, _id):
        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.find_one({"_id":objInstance})

        self.write({"res": json.loads(json_util.dumps(x))})
    
    def put(self, _id):
        newvalues = json.loads(self.request.body)

        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.update_one({"_id": objInstance}, {"$set": newvalues})

        self.write({"res": "Employee updated"})
    
    def delete(self, _id):
        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.delete_one({"_id": objInstance})

        self.write({"res":"Employee deleted"})
```

## 3.3 Conectando o banco de dados do mongodb

Usamos anteriormente uma função para acessar o banco de dados, segue abaixo como isso pode ser feito utilizando o pymongo. Primeiramente criamos um arquivo `db.py` e inserimos as seguintes linhas de código:

```python
import pymongo

def db_connect(collection="employees"):
	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["mydatabase"]
	
	mycol = mydb[collection]
	return mycol
```

Pronto, a função que conecta uma determinada coleçao no seu banco de dados está pronta!

# 3.4 Validação e tratamento de erros

Primeiramente vamos validar se os campos do payload estão chegando com as keys obrigatórias, para isso vamos criar um novo arquivo chamado `[utils.py](http://utils.py)` com o seguinte código:

```python
def mandatory_keys_check(list_mandatory, list_dict_keys):
  """
    Check if the payload json file have the mandatory keys
    :param list_mandatory: list
    :param list_dict_keys: list
    :return True or False
  """
  check = all(item in list_dict_keys for item in list_mandatory)
  return check
```

Vamos colocar essa nova função criada no nosso arquivo `[app.py](http://app.py)` primeiramente precisamos importar as funções do arquivo `utils.py`

```python
import utils
```

Depois adicionamos a função no post no nosso handler:

```python
class EmployeeHandler(tornado.web.RequestHandler):
    def post(self):

        list_mandatory = ['name','birth_date','gender','email','cpf','start_date']

        new_employee = json.loads(self.request.body)

        list_dict_keys = list(new_employee.keys())

        if not(utils.mandatory_keys_check(list_mandatory, list_dict_keys)):
            self.set_status(400)
            self.write('Fail to create an Employee. Please check your data')
            return None

        db = database.db_connect()

        x = db.insert_one(new_employee)

        self.write("New employee created!")
...
```

A segunda validação é caso o banco de dados esteja vazio, novamente no método get do EmployeeHandler

```python
def get(self):
        db = database.db_connect()

        list_employees = [doc for doc in db.find({})]

        if(len(list_employees)>0):
            self.write({"Response": json.loads(json_util.dumps(list_employees))})
        else:
            self.write("Empty database")
```

o código completo ficou assim:

```python
import tornado.ioloop
import tornado.web

import json
from bson import json_util
from bson.objectid import ObjectId

import database
import utils

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

class EmployeeHandler(tornado.web.RequestHandler):
    def post(self):

        list_mandatory = ['name','birth_date','gender','email','cpf','start_date']

        new_employee = json.loads(self.request.body)

        list_dict_keys = list(new_employee.keys())

        if not(utils.mandatory_keys_check(list_mandatory, list_dict_keys)):
            self.set_status(400)
            self.write('Fail to create an Employee. Please check your data')
            return None

        db = database.db_connect()

        x = db.insert_one(new_employee)

        self.write("New employee created!")
    
    def get(self):
        db = database.db_connect()

        list_employees = [doc for doc in db.find({})]

        if(len(list_employees)>0):
            self.write({"Response": json.loads(json_util.dumps(list_employees))})
        else:
            self.write("Empty database")

class EmployeesHandler(tornado.web.RequestHandler):
    def get(self, _id):
        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.find_one({"_id":objInstance})

        self.write({"res": json.loads(json_util.dumps(x))})
    
    def put(self, _id):
        newvalues = json.loads(self.request.body)

        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.update_one({"_id": objInstance}, {"$set": newvalues})

        self.write({"res": "Employee updated"})
    
    def delete(self, _id):
        objInstance = ObjectId(_id)

        db = database.db_connect()

        x = db.delete_one({"_id": objInstance})

        self.write({"res":"Employee deleted"})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/employee", EmployeeHandler),
        (r"/employee/([^/]+)?", EmployeesHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

...