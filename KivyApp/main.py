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
from functions import callbacklogin, callbackregister

Window.size = (350, 580)

global screen
global firebaseConfig
global firebase2 
global lista2
global HORARIOS_SELECIONADOS

screen = ScreenManager()
firebaseConfig={
  
  #PUT THE KEYS TO YOUR FIRABSE DATABASE HERE
  
};
firebase2 = pyrebase.initialize_app(firebaseConfig)
lista2 = []
HORARIOS_SELECIONADOS = []   


class SplashScreen(Screen):
    pass

class RegisterScreen(Screen):  

  #firebase_url = " "
  #firebase_url2 = " "
  #auth_key = ' ' 
  
  def callbackregister(self, *args):
    callbackregister(self,*args)

  def registro(self, nome, cpf, senha):
    from functions import create_post
    create_post(self, nome, cpf, senha)  


class LoginScreen(Screen):
  #firebase_url = " "
  #auth_key = ' ' 
  
  def callbacklogin(self, *args):
    callbacklogin(self,*args)
    
  def loga(self, cpf, senha):
    from functions import get_post
    get_post(self, cpf, senha)


class ForgetSenhaScreen(Screen):
  #firebase_url = " "    
  #auth_key = ' '  

  def esqueciSenha(self, cpf, senha):
    from functions import redf_passwd
    redf_passwd(self, cpf, senha)
  

class DashboardScreen(Screen):
  def on_enter(self):
    nome = list(open("autenticado.txt", "r"))
    nome = nome[0]
    self.ids.lbdashboard.text = "Olá, " + str(nome)
     

class AboutUserScreen(Screen):
  #firebase_url = " "    
  #auth_key = ' '  

  def on_enter(self):
    from functions import on_enter2
    on_enter2(self)
   

class ChangeAboutScreen(Screen):

  def editaInfo(self, nome, cpf, id):
    from functions import change_screen
    change_screen(self, nome, cpf, id)


class PrecheckScreen(Screen):
  pass


class CheckinScreen(Screen):
  #firebase_url = " "    
  #firebase_url2 = " " 
  #auth_key = ' '

  def consulta(self, especialidade, data, paciente):
    from functions import check
    check(self, especialidade, data, paciente) 

  def on_save(self, instance, value, data_range):
    from functions import on_save
    on_save(self, instance, value, data_range)

  def on_cancel(self, instance, value):
    from functions import on_cancel
    on_cancel(self, instance, value)

  def data(self):
    from functions import show_data_picker
    show_data_picker(self)     

 

class CheckoutScreen(Screen):
  #firebase_url = " "    
  #firebase_url2 = " "
  #firebase_url3 = " "
  #auth_key = ' '

  def retirada(self, med, data, paciente2):
    from functions import checkout
    checkout(self, med, data, paciente2)

  def on_save2(self, instance, value, data_range):
    from functions import on_save2
    on_save2(self, instance, value, data_range)

  def on_cancel2(self, instance, value):
    from functions import on_cancel2
    on_cancel2(self, instance, value)

  def data(self):
    from functions import show_data_picker2
    show_data_picker2(self)     



class MedsScreen(Screen):
  pass


class ControlMedsScreen(Screen):
  #firebase_url = " "  
  #auth_key = ' ' 

  def entradaMeds(self, nome_med, quantidade, id_med):
    from functions import create_post_meds
    create_post_meds(self, nome_med, quantidade, id_med)

  def saidaMeds(self, nome_med, quantidade, id_med):
    from functions import create_delete
    create_delete(self, nome_med, quantidade, id_med)


class VerifyMedsScreen(Screen):
  def on_stop(self):
    from functions import on_stop
    on_stop(self)

  def on_enter(self):
    from functions import on_enter
    on_enter(self) 

  def start_second_thread(self):
    from functions import start_second_thread
    start_second_thread(self)
  
  def load_data(self, *args):
    from functions import load_data
    load_data(self, *args)

  def data_table(self, cols, values):
    from functions import data_table
    data_table(self, cols, values)
    
    
class ActivitiesScreen(Screen):
  pass

class InfoScreen(Screen):
  pass

class RegisterPacients(Screen):
  #firebase_url = " "
  #auth_key = ' ' 
  
  def callbackregisterpacientes(self, *args):
    from functions import callbackregisterpacientes
    callbackregisterpacientes(self, *args)

  def registroPacientes(self, nome2, cpf2, senha2):
    from functions import create_post_pacient
    create_post_pacient(self, nome2, cpf2, senha2)


class HourScreen(Screen):
  #firebase_url = " "
  #firebase_url2 = " "
  #auth_key = ' ' 
  
  def callbackplantao(self, *args):
    from functions import callbackplantao
    callbackplantao(self, *args)

  def on_save3(self, instance, value, date_range):
    from functions import on_save3
    on_save3(self, instance, value, date_range)

  def on_cancel3(self, instance, value):
    from functions import on_cancel3
    on_cancel3(self, instance, value)

  def show_data_picker3(self):
    from functions import show_data_picker3
    show_data_picker3(self)

  def registraPlantao(self, cpf_funcionario, data2, horario):
    from functions import create_post_hour  
    create_post_hour(self, cpf_funcionario, data2, horario)


class ScheduleScreen(Screen):
  def on_stop(self):
    from functions import on_stop2
    on_stop2(self)

  def on_enter(self):
    from functions import on_enter4
    on_enter4(self) 

  def start_second_thread(self):
    from functions import start_second_thread2
    start_second_thread2(self)
  
  def load_data(self, *args):
    from functions import load_data2
    load_data2(self, *args)

  def data_table(self, cols, values):
    from functions import data_table2
    data_table2(self, cols, values)
    

class TakeoffScreen(Screen):
  def on_stop(self):
    from functions import on_stop3
    on_stop3(self)

  def on_enter(self):
    from functions import on_enter5
    on_enter5(self) 

  def start_second_thread(self):
    from functions import start_second_thread3
    start_second_thread3(self)
  
  def load_data(self, *args):
    from functions import load_data3
    load_data3(self, *args)

  def data_table(self, cols, values):
    from functions import data_table3
    data_table3(self, cols, values)


class DutyScreen(Screen):
  #firebase_url = " "
  #auth_key = ' '     

  def on_stop(self):
    from functions import on_stop4
    on_stop4(self)

  def on_enter(self):
    from functions import on_enter6
    on_enter6(self) 

  def start_second_thread(self):
    from functions import start_second_thread4
    start_second_thread4(self)
  
  def load_data(self, *args):
    from functions import load_data4
    load_data4(self, *args)

  def on_check_press(self, instance_table, current_row):
    from functions import on_check_press
    on_check_press(self, instance_table, current_row)

  def data_table(self, cols, values):
    from functions import data_table4
    data_table4(self, cols, values)


class PacientScreen(Screen):
  def on_stop(self):
    from functions import on_stop5
    on_stop5(self)

  def on_enter(self):
    from functions import on_enter7
    on_enter7(self) 

  def start_second_thread(self):
    from functions import start_second_thread5
    start_second_thread5(self)
  
  def load_data(self, *args):
    from functions import load_data5
    load_data5(self, *args)

  def data_table(self, cols, values):
    from functions import data_table5
    data_table5(self, cols, values)
  
  
screen.add_widget(SplashScreen(name='splash'))
screen.add_widget(LoginScreen(name='login'))
screen.add_widget(ForgetSenhaScreen(name='esqueci'))
screen.add_widget(RegisterScreen(name='register'))
screen.add_widget(DashboardScreen(name='dashboard'))
screen.add_widget(PrecheckScreen(name='precheck'))
screen.add_widget(CheckinScreen(name='checkin'))
screen.add_widget(CheckoutScreen(name='checkout'))
screen.add_widget(MedsScreen(name='meds'))
screen.add_widget(VerifyMedsScreen(name='verifymeds'))
screen.add_widget(ControlMedsScreen(name='controlmeds'))
screen.add_widget(ActivitiesScreen(name='activities'))
screen.add_widget(RegisterPacients(name='cadastropacientes'))
screen.add_widget(HourScreen(name='hour'))
screen.add_widget(InfoScreen(name='info'))
screen.add_widget(ScheduleScreen(name='schedule'))
screen.add_widget(TakeoffScreen(name='takeoff'))
screen.add_widget(DutyScreen(name='duty'))
screen.add_widget(PacientScreen(name='pacients'))


class HealthApp(MDApp):

  def build(self):
    kv = Builder.load_file("telas.kv")
    screen = kv
    return screen


if __name__ == "__main__":
    HealthApp().run()
