import json
import threading

import pyrebase
import requests
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.picker import MDDatePicker

global firebaseConfig
global firebase2 
global lista2
global HORARIOS_SELECIONADOS

firebaseConfig={
  
#PUT THE KEYS TO YOUR FIREBASE DATABASE HERE

};


firebase2 = pyrebase.initialize_app(firebaseConfig)
lista2 = []
HORARIOS_SELECIONADOS = []  


# Redireciona para a tela de login
def callbackregister(self, *args):
  MDApp.get_running_app().root.current = 'login'

# Cria o registro do usuario e posta as informações na base de dados do firebase (realtime database)  
def create_post(self, nome, cpf, senha):
  #firebase_url = " "    
  #auth_key = ' '  

  lista = []
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  try:        
    to_database = '{"Nome": 'f'{json.dumps(nome)}'', "CPF" : 'f'{json.dumps(cpf)}'', "Senha" : 'f'{json.dumps(senha)}''}'

    
    if nome == "":
      self.ids.lbregister.text = "Insira nome"

    elif cpf == "":
      self.ids.lbregister.text = "Insira CPF"

    elif senha == "":
      self.ids.lbregister.text = "Insira Senha"  

    elif len(cpf) < 11:
      self.ids.lbregister.text = "CPF inválido, tente novamente"

    elif len(senha) < 10:
      self.ids.lbregister.text = "Senha precisa de pelo menos 10 caracteres"   

    elif cpf in res:
      self.ids.lbregister.text = "CPF já cadastrado"

    else:
      #requests.post(url = self.firebase_url, json = to_database2)
      requests.post(url = self.firebase_url, json = json.loads(to_database))

      self.ids.lbregister.text = "Cadastrado com sucesso! Redirecionando para a tela de login..."
      Clock.schedule_once(self.callbackregister, 3)


      lista.append(nome)
      lista.append(cpf)
      lista.append(senha)

    
      with open(f'{cpf}.txt',"w") as a:
        a.write(str(lista[0]))
        a.write("\n")
        a.write(str(lista[1]))
        a.write("\n")
        a.write(str(lista[2]))
    
  except ValueError:
    pass        

  lista.clear

# Redireciona para o dashboard
def callbacklogin(self, *args):
  MDApp.get_running_app().root.current = 'dashboard'

    
# Autentica o usuario de acordo com as informações que são coletadas do banco de dados firebase
def get_post(self, cpf, senha):
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json())         
  
  
  if (cpf != '' and senha != ''):
    if (len(cpf) == 11 and cpf in res) and (len(senha) >= 10 and senha in res):
      self.ids.lblogin.text = "Logado com sucesso! Redirecionando para a tela inicial..."                
      Clock.schedule_once(self.callbacklogin, 3)
      nome = list(open(f'{cpf}.txt', "r"))
      nome = nome[0]
      id = list(open(f'{cpf}.txt', "r"))
      id = id[2]
      with open("autenticado.txt", "w") as f:    
        f.write(str(nome))
        f.write(str(cpf))
        f.write("\n")
        f.write(str(id))  

    else: 
      self.ids.lblogin.text = "CPF ou senha inválidos, tente novamente"   


  else: 
    if(cpf == ''):
      self.ids.lblogin.text = "Insira o CPF logar"

    elif(senha == ''):
      self.ids.lblogin.text = "Insira a senha para logar"


    elif (cpf == '' and senha == ''):
      self.ids.lblogin.text = "Insira os dados para logar"     


# Redefine senha 

def redf_passwd(self, cpf, senha):
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  if cpf == "":
    self.ids.lbredfsenha.text = "Insira o cpf"
  elif cpf not in res:
    self.ids.lbredfsenha.text = "CPF não cadastrado"
  elif len(cpf) < 11:
    self.ids.lbredfsenha.text = "CPF Inválido"
  elif senha == "": 
    self.ids.lbredfsenha.text = "Insira a nova senha"
  elif len(senha) < 10:
    self.ids.lbredfsenha.text = "Senha precisa ter pelo menos 10 caracteres"
    
  else:
    db = firebase2.database()
    user = db.child("Users").get()
    for usuario in user.each():
      if usuario.val()['CPF'] == f'{cpf}' :
        db.child("Users").child(usuario.key()).update({'Senha': f'{senha}'})
        a = open(f'{cpf}.txt', "r")
        list_of_lines = a.readlines()    
        list_of_lines[2] = f'{senha}'
        a = open(f'{cpf}.txt', "w")
        a.writelines(list_of_lines) 
        a.close()
    
    self.ids.lbredfsenha.text = "Senha redefinida com sucesso!"


# Edita as informações do usuário  

def change_screen(self, nome, cpf, id):
  nome2 = list(open("autenticado.txt", "r"))
  nome2 = nome2[0]
  cpf2 = list(open("autenticado.txt", "r"))
  cpf2 = cpf2[1]
  id2 = list(open("autenticado.txt", "r"))
  id2 = id2[2]
    

  db = firebase2.database()
  user = db.child("Users").get()
  for usuario in user.each():
    if usuario.val()['Nome'] in nome2:
      if f'{nome}' != "":
        db.child("Users").child(usuario.key()).update({'Nome': f'{nome}'})
        
        f = open("autenticado.txt", "r")
        list_of_lines = f.readlines()    
        list_of_lines[0] = f'{nome}\n'
        f = open("autenticado.txt", "w")
        f.writelines(list_of_lines) 
        f.close()
        self.ids.lbchange.text = "Nome alterado com sucesso!"

          
    if usuario.val()['CPF'] in cpf2:
      if f'{cpf}' != "":
        db.child("Users").child(usuario.key()).update({'CPF': f'{cpf}'})

        a = open("autenticado.txt", "r")
        list_of_lines = a.readlines()    
        list_of_lines[1] = f'{cpf}\n'
        a = open("autenticado.txt", "w")
        a.writelines(list_of_lines) 
        a.close()
        self.ids.lbchange.text = "CPF alterado com sucesso!"
        

    if usuario.val()['Senha'] in id2:
      if f'{id}' != "":
        db.child("Users").child(usuario.key()).update({'Senha': f'{id}'})

        b = open("autenticado.txt", "r")
        list_of_lines = b.readlines()    
        list_of_lines[2] = f'{id}\n'
        b = open("autenticado.txt", "w")
        b.writelines(list_of_lines) 
        b.close()
        self.ids.lbchange.text = "ID alterado com sucesso!"

    self.ids.lbchange.text = "Dados alterados com sucesso!"
    
    with open(f'{cpf}.txt', "w") as op:
        op.write(str(nome))
        op.write("\n")
        op.write(str(cpf))
        op.write("\n")
        op.write(str(id))


# Salva a data escolhida pelo usuario
def on_save(self, instance, value, date_range):
  self.ids.data.text = str(value)  

# Mostra a mensagem quando o usuario cancela a data
def on_cancel(self, instance, value):
  self.ids.data.text = "Você cliclou em cancelar"

# Cria o calendario
def show_data_picker(self):
  date_dialog = MDDatePicker(year=2022, month=6, day=17)
  date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
  date_dialog.open()     


# Cria a consulta e salva no banco de dados firebase
def check(self, especialidade, data, paciente):
  #firebase_url = " "    
  #firebase_url2 = " " 

  #auth_key = ' '

  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 

  request2 = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res2 = json.dumps(request2.json()) 

  if especialidade == "":
    self.ids.lbcheckin.text = "Insira a especialidade"
  elif paciente not in res2:
    self.ids.lbcheckin.text = "Paciente não registrado"
  elif paciente == "":
    self.ids.lbcheckin.text = "Insira ID do paciente"

  else:
    to_database = '{"Especialidade": 'f'{json.dumps(especialidade)}'', "Data": 'f'{json.dumps(data)}'', "ID do paciente": 'f'{json.dumps(paciente)}''}' 
    db = firebase2.database()
    pacients = db.child("Pacients").get()
    for paciente2 in pacients.each():
      if paciente2.val()['ID Paciente'] == f'{paciente}':
        db.child("Pacients").child(paciente2.key()).update({'Tipo de tratamento' : f'{especialidade}'}) 

    try:
      
      requests.post(url = self.firebase_url, json = json.loads(to_database))
      self.ids.lbcheckin.text = "Consultada agendada com sucesso!"


    except ValueError:
      pass  


def on_save2(self, instance, value, date_range):
  self.ids.data.text = str(value)  

def on_cancel2(self, instance, value):
  self.ids.data.text = "Você cliclou em cancelar"

def show_data_picker2(self):
  date_dialog = MDDatePicker(year=2022, month=6, day=17)
  date_dialog.bind(on_save=self.on_save2, on_cancel=self.on_cancel2)
  date_dialog.open()          

# Cria a retirada de medicamentos 

def checkout(self, med, data, paciente2):
  #firebase_url = " "    
  #firebase_url2 = " "
  #firebase_url3 = " "
  #auth_key = ' '
  
  request = requests.get(self.firebase_url3 + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  request2 = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res2 = json.dumps(request2.json()) 

  if med not in res2:
    self.ids.lbcheckout.text = "Medicamento fora de estoque"
  elif med == "":
    self.ids.lbcheckout.text = "Insira nome do medicamento "
  elif paciente2 not in res:
    self.ids.lbcheckout.text = "Paciente não registrado"
  elif paciente2 == "":
    self.ids.lbcheckout.text = "Insira ID do paciente"

  else:
    to_database = '{"Medicamento": 'f'{json.dumps(med)}'', "Data": 'f'{json.dumps(data)}'', "ID Paciente": 'f'{json.dumps(paciente2)}''}'
    #to_database1 = '{"Data": 'f'{data}''}'

    try:
      requests.post(url = self.firebase_url, json = json.loads(to_database))
      self.ids.lbcheckout.text = "Retirada agendada com sucesso!"
      #requests.post(url = self.firebase_url, json = json.dumps(to_database1))

    except ValueError:
      pass  


# Cria o estoque de medicamentos (entrada e saida dos mesmos)

def create_post_meds(self, nome_med, quantidade, id_med):
  #firebase_url = " "  
  #auth_key = ' ' 
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  if nome_med == "":
    self.ids.lbmeds.text = "Insira medicamento"
  elif quantidade == "":
    self.ids.lbmeds.text = "Insira quantidade maior que 0"
  elif id_med == "":
    self.ids.lbmeds.text = "Insira o id do med"  

  else:
    try:        
      to_database = '{"Nome do medicamento": 'f'{json.dumps(nome_med)}'', "Quantidade" : 'f'{json.dumps(quantidade)}'', "ID medicamento" : 'f'{json.dumps(id_med)}''}'

      requests.post(url = self.firebase_url, json = json.loads(to_database))

      self.ids.lbmeds.text = "Medicamento adicionado ao estoque!"        

    except ValueError:
      pass  

    lista2.append(int(quantidade))  

  with open("meds.txt", "a") as fp:
    for item in lista2:
      fp.write("%d\n" % item)     


def create_delete(self, nome_med, quantidade, id_med):
  #firebase_url = " "  
  #auth_key = ' '
    
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  to_database = '{"Nome do medicamento": 'f'{json.dumps(nome_med)}'', "Quantidade" : 'f'{json.dumps(quantidade)}'', "ID medicamento" : 'f'{json.dumps(id_med)}''}'

  if nome_med == "":
    self.ids.lbmeds.text = "Insira medicamento"
  elif quantidade == "":
    self.ids.lbmeds.text = "Insira quantidade maior que 0"
  elif id_med == "":
    self.ids.lbmeds.text = "Insira o id do med"  

  else:

    with open("meds.txt", "r") as fp:
      conteudo = fp.readlines()
      for conteudos in conteudo:
        lista2.append(int(conteudos))          
    fp.close()    

    new_quant = (lista2[int(id_med)] - int(quantidade)) 

    db = firebase2.database()
    meds = db.child("Meds").get()
    for meds2 in meds.each():
      if meds2.val()['ID medicamento'] == f'{id_med}':
        db.child("Meds").child(meds2.key()).update({'Quantidade' : f'{new_quant}'}) 

      a = open("meds.txt", "r")
      list_of_lines = a.readlines()    
      list_of_lines[int(id_med)] = f'{new_quant}\n'
      a = open("meds.txt", "w")
      a.writelines(list_of_lines) 
      a.close()

    self.ids.lbmeds.text = "Medicamento retirado do estoque"   


# Cria tabela e lista os medicamentos

stop = threading.Event()

def on_stop(self):
  self.stop.set()

def on_enter(self):
  self.start_second_thread()

def start_second_thread(self):
  threading.Thread(target=self.load_data).start()

def load_data(self, *args): 
  get_request = requests.get(f' ')
  consultas_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for consultas, dado in consultas_data.items():
    lista = []
    lista.append(consultas)

    for key, info in dado.items():
      lista.append(info)
      
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)   

  
@mainthread
def data_table(self, cols, values):    
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables)

# Mostra os dados sobre o usuário

def on_enter2(self):
  #firebase_url = " "    
  auth_key = ' '  
  
  nome = list(open('autenticado.txt', 'r'))
  nome = nome[0]
  cpf = list(open('autenticado.txt', 'r'))
  cpf = cpf[1]
  id = list(open('autenticado.txt', 'r')) 
  id = id[2]
  self.ids.cpffuncionario.text = cpf    
  self.ids.nomefuncionario.text = nome
  self.ids.idfuncionario.text = id


# Registra os pacientes e coloca os dados diretamente no banco de dados firebase

def callbackregisterpacientes(self, *args):
  MDApp.get_running_app().root.current = 'login'

def create_post_pacient(self, nome2, cpf2, senha2):
  #firebase_url = " "
  #auth_key = ' ' 
  request = requests.get(self.firebase_url + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  try:        
    to_database = '{"Nome": 'f'{json.dumps(nome2)}'', "CPF" : 'f'{json.dumps(cpf2)}'', "ID Paciente" : 'f'{json.dumps(senha2)}''}'


    if len(cpf2) != 11:
      self.ids.lbregister_pacient.text = "CPF inválido, tente novamente"

    elif len(cpf2) < 10:
      self.ids.lbregister_pacient.text = "Senha precisa de pelo menos 10 caracteres"   

    elif cpf2 in res:
      self.ids.lbregister_pacient.text = "CPF já cadastrado"

    else:
      #requests.post(url = self.firebase_url, json = to_database2)
      requests.post(url = self.firebase_url, json = json.loads(to_database))

      self.ids.lbregister_pacient.text = "Paciente cadastrado com sucesso!"

  except ValueError:
    pass  

# Registra horários de plantão e coloca os dados diretamente no banco de dados firebase

def callbackplantao(self, *args):
  MDApp.get_running_app().root.current = 'login'

def on_save3(self, instance, value, date_range):
  self.ids.data2.text = f'{str(date_range[0])} - {str(date_range[-1])}'

def on_cancel3(self, instance, value):
  self.ids.data2.text = "Você cliclou em cancelar"

def show_data_picker3(self):
  date_dialog = MDDatePicker(mode="range")
  date_dialog.bind(on_save=self.on_save3, on_cancel=self.on_cancel3)
  date_dialog.open()   

def create_post_hour(self, cpf_funcionario, data2, horario):
  request = requests.get(self.firebase_url2 + '?auth=' + self.auth_key)
  res = json.dumps(request.json()) 
  
  if cpf_funcionario not in res:
    self.ids.lbregister_hour.text = "CPF não cadastrado"  

  elif horario == "":
    self.ids.lbregister_hour.text = "Insira horário"

  else:

    try:        
      to_database = '{"CPF funcionario": 'f'{json.dumps(cpf_funcionario)}'', "Data" : 'f'{json.dumps(data2)}'', "Horario" : 'f'{json.dumps(horario)}''}'


      
      requests.post(url = self.firebase_url, json = json.loads(to_database))
      self.ids.lbregister_hour.text = "Horario adicionado com sucesso!"

    except ValueError:
      pass  


# Cria tabela que mostra consultadas agendadas 

stop2 = threading.Event()

def on_stop2(self):
  self.stop2.set()

def on_enter4(self):
  self.start_second_thread()

def start_second_thread2(self):
  threading.Thread(target=self.load_data).start()

def load_data2(self, *args): 
  #get_request = requests.get(f' ')
  consultas_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for consultas, dado in consultas_data.items():
    lista = []
    lista.append(consultas)

    for key, info in dado.items():
      lista.append(info)
      
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)   

  
@mainthread
def data_table2(self, cols, values):    
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables)


# Cria tabela que mostra retirada de medicamentos agendadas

stop3 = threading.Event()

def on_stop3(self):
  self.stop3.set()

def on_enter5(self):
  self.start_second_thread()

def start_second_thread3(self):
  threading.Thread(target=self.load_data).start()

def load_data3(self, *args): 
  get_request = requests.get(f' ')
  consultas_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for consultas, data in consultas_data.items():
    lista = []
    lista.append(consultas)

    for key, info in data.items():
      lista.append(info)
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)  

@mainthread
def data_table3(self, cols, values):
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables) 


# Cria tabela que mostra horarios de plantão e remove horarios


stop4 = threading.Event()

def on_stop4(self):
  self.stop4.set()

def on_enter6(self):
  self.start_second_thread()

def start_second_thread4(self):
  threading.Thread(target=self.load_data).start()

def load_data4(self, *args): 
  #firebase_url = " "
  #auth_key = ' '     
  if HORARIOS_SELECIONADOS:
    for h_horarios in HORARIOS_SELECIONADOS:
      post_request = requests.delete(f'/{h_horarios}/.json')

  get_request = requests.get(f' ')
  horarios_dado = json.loads(get_request.content.decode())     
  count = 0
  cols = ["Código"]
  values = []
  try:

    for horarios, dado in horarios_dado.items():
      lista = []
      lista.append(horarios)

      for key, info in dado.items():
        lista.append(info)
        if count == 0:
          cols.append(key)        
      count+=1  
      values.append(lista)
      
  except AttributeError:
    pass    

  self.data_table(cols, values)  

def on_check_press(self, instance_table, current_row):

  '''Called when the check box in the table row is checked.'''
  if current_row[0] in HORARIOS_SELECIONADOS:
      HORARIOS_SELECIONADOS.remove(current_row[0])
  else:
      HORARIOS_SELECIONADOS.append(current_row[0])


@mainthread
def data_table4(self, cols, values):  

  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.data_tables.bind(on_check_press=self.on_check_press)
  self.add_widget(self.data_tables) 


# Cria tabela que mostra os pacientes registrados

stop5 = threading.Event()

def on_stop(self):
  self.stop5.set()

def on_enter7(self):
  self.start_second_thread()

def start_second_thread5(self):
  threading.Thread(target=self.load_data).start()

def load_data5(self, *args): 
  get_request = requests.get(f' ')
  pacientes_data = json.loads(get_request.content.decode())

  count = 0
  cols = ["Código"]
  values = []
  for pacientes, data in pacientes_data.items():
    lista = []
    lista.append(pacientes)

    for key, info in data.items():
      lista.append(info)
      if count == 0:
        cols.append(key)        
    count+=1  
    values.append(lista)

  self.data_table(cols, values)  

@mainthread
def data_table5(self, cols, values):
  self.data_tables = MDDataTable(    
    pos_hint={'center_y': 0.5, 'center_x': 0.5},
    size_hint=(0.9, 0.6),
    column_data=[
      (col, dp(40))
      for col in cols       
    ],
    row_data=values,
    check=True
  )    

  self.add_widget(self.data_tables) 
