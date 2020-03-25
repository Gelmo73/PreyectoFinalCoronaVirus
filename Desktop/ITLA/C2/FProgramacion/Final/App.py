import Utilidades
from Utilidades import Limpiar, Continuar, OpcionInvalida
import sys
import os
import telegram
import pickle
import json
import webbrowser
from ClasePersona import Persona
import datetime
from colorama import init, Fore
init()

# ---------------------------------------------------------------------- #
# ------------------------- VARIABLES GLOBALES ------------------------- #
# ---------------------------------------------------------------------- #

upath = os.environ['USERPROFILE'] + '/Desktop/'
registros = list()
provincias = list()
numeros_misticos = dict()
folderstorage = 'C:/RegistrosCorona/'
filestorage = 'store.bin'
misticstorage = 'mistic.bin'
bot_token = '1086161801:AAH6HK3Iu0etpUrG05zVItd3zyAYfSeZfm4'
channel = '-1001447406914'
bot = telegram.Bot(bot_token)

with open('Json/Provincia.json', 'r') as f:
    provincias = json.load(f)

if not os.path.exists(folderstorage):
    os.mkdir('C:/RegistrosCorona/')

if os.path.exists(folderstorage + filestorage):
    with open(folderstorage + filestorage, 'rb') as f:
        registros = pickle.load(f)

if not os.path.exists(folderstorage + misticstorage):
    with open(folderstorage + misticstorage, 'wb') as f:
        pickle.dump(Utilidades.jsonstr, f)

with open(folderstorage + misticstorage, 'rb') as f:
    numeros_misticos = pickle.load(f)


# ---------------------------------------------------------------------- #
# --------------------------- MENU PRINCIPAL --------------------------- #
# ---------------------------------------------------------------------- #


def Menu():

    Limpiar()

    print('------- Agenda de Casos -------')
    print('----- Elija alguna opcion -----\n')
    print('1) Registrar caso')
    print('2) Editar caso')
    print('3) Eliminar caso')
    print('4) Exportar/Mostrar casos')  # Uno o todos
    print('5) Mapa de casos')
    print('6) Estadistica Mistica')
    print('7) Guardar cambios')  # Hacer que pregunte para guardar cambios
    print('8) Salir de Agenda de Casos\n')

    return input()  # Opcion


def OpcionMenu(opcion):

    if opcion == '1':
        Registrar()
        Continuar()

    elif opcion == '2':
        Editar()
        Continuar()

    elif opcion == '3':
        Eliminar()
        Continuar()

    elif opcion == '4':
        Exportar()
        Continuar()

    elif opcion == '5':
        Mapa()
        Continuar()
    elif opcion == '6':
        Estadistica()
        Continuar()
    elif opcion == '7':
        Guardar()
        Continuar()

    elif opcion == '8':
        Salir()
    # Para pruebas personales
    elif opcion == 'getout71':
        Pruebas()
    else:
        print('Opcion no valida')
        Continuar()

# ---------------------------------------------------------------------- #
# ----------------------- FUNCIONES PRINCIPALES ------------------------ #
# ---------------------------------------------------------------------- #


def Registrar():

    Limpiar()

    provincia = Persona.RestriccionProvincia(provincias)
    lat, lon = Persona.RestriccionCoordenadas()

    if not Utilidades.ValidarCoordenadas(lat, lon, provincia):
        return

    documento = Persona.RestriccionDocumento()
    nacionalidad = Persona.RestriccionNacionalidad(documento)
    num_doc = Persona.RestriccionNumeroDocumento(documento)

    if num_doc == '0':
        return

    Limpiar()

    nombre = Persona.RestriccionNombre()
    apellido = Persona.RestriccionApellido()
    tel = Persona.RestriccionTelefono()
    fecha_nacimiento = Persona.RestriccionFecha()
    zodiaco = Utilidades.ObtenerSignoZodiacal(
        fecha_nacimiento.month, fecha_nacimiento.day)
    email = Persona.RestriccionEmail()
    sexo = Persona.RestriccionSexo()

    numeros_misticos[zodiaco]['Enfermos'] += 1

    Limpiar()

    temp = Persona(documento, num_doc, nombre, apellido, nacionalidad,
                   sexo, fecha_nacimiento, zodiaco, tel, email, provincia, lat, lon)

    print('Datos Registrados...\n')
    Mostrar(temp)
    registros.append(temp)
    try:
        Alerta(temp)
    except telegram.error.NetworkError:
        print('Error de Conexion')

    del(temp)


def Editar():
    Limpiar()
    Mostrar(registros)
    print('Seleccione el registro:')

    try:
        nregistro = int(input()) - 1

        if not (0 <= nregistro < len(registros)):
            print('Opcion no valida')
            return
    except:
        print('Algo salio mal')

    while True:
        Limpiar()
        persona = registros[nregistro]
        Mostrar(persona)
        print('''Elija el campo a modificar [S] Salida

 1) Documento            2) Nacionalidad     3) Numero de Documento
 4) Nombre               5) Apellido         6) Telefono
 7) Fecha de Nacimiento  8) Email            9) Sexo
 10) Estado              11) Ubicacion
        ''')

        opcion = input().upper()

        if opcion == '1':
            documento = Persona.RestriccionDocumento()

            if documento == 'Cedula de Identidad':
                if not Utilidades.ValidarCedula(persona.num_doc):
                    while True:
                        Limpiar()
                        print(
                            'Su numero no coincide con una cedula valida. Debe cambiarla\n\n')
                        Continuar()
                        num_doc = Persona.RestriccionNumeroDocumento(documento)

                        if not (num_doc == '0'):
                            break

                    persona.num_doc = num_doc

            persona.documento = documento

        elif opcion == '2':
            persona.nacionalidad = Persona.RestriccionNacionalidad(documento)

        elif opcion == '3':

            num_doc = Persona.RestriccionNumeroDocumento(documento)

            if not (num_doc == '0'):
                persona.num_doc = num_doc

        elif opcion == '4':
            persona.nombre = Persona.RestriccionNombre()

        elif opcion == '5':
            persona.apellido = Persona.RestriccionApellido()

        elif opcion == '6':
            persona.tel = Persona.RestriccionTelefono()

        elif opcion == '7':
            persona.fecha = Persona.RestriccionFecha()
            persona.zodiaco = Utilidades.ObtenerSignoZodiacal(
                persona.fecha.month, persona.fecha.day)

        elif opcion == '8':
            persona.email = Persona.RestriccionEmail()

        elif opcion == '9':
            persona.sexo = Persona.RestriccionSexo()

        elif opcion == '10':
            numeros_misticos = persona.setEstado(numeros_misticos)
        elif opcion == '11':
            provincia = Persona.RestriccionProvincia(provincias)
            lat, lon = Persona.RestriccionCoordenadas()

            if Utilidades.ValidarCoordenadas(lat, lon, provincia):
                persona.provincia = provincia
                persona.coordenadas = lat, lon
        elif opcion == 'S':
            break
        else:
            print('Opcion no Valida')
    print('Cambios Realizados\n')
    Mostrar(persona)
    try:
        Alerta(persona)
    except telegram.error.NetworkError:
        print('Error de Conexion')


def Eliminar():
    Limpiar()
    Mostrar(registros)
    print('Seleccione el registro a modificar:')

    try:
        nregistro = int(input()) - 1

        if not (0 <= nregistro < len(registros)):
            print('Opcion no valida')
            return
    except:
        print('Algo salio mal')

    Limpiar()
    persona = registros[nregistro]
    Mostrar(persona)

    print('\nEsta a punto de eliminar este registro...')
    print('Escriba: CONFIRMAR')

    if input() == 'CONFIRMAR':
        numeros_misticos[persona.zodiaco][persona.estado + 's'] -= 1
        registros.pop(persona)
        print('Registro Eliminado')
    else:
        print('Eliminacion cancelada')


def Exportar():

    while True:
        Limpiar()
        print('Desea exportar todos o un solo registro?')
        print('[T] Todos')
        print('[U] Uno')
        print('[C] Cancelar')

        opcion = input().upper()

        if opcion == 'T':
            with open('Html/casos.html', 'r') as f:
                html = f.read()
            for persona in registros:
                temp = '''
            <tr>
          <td>'''+persona.num_doc+'''</td>
          <td>'''+persona.documento+'''</td>
          <td>'''+persona.nombre+'''</td>
          <td>'''+persona.apellido+'''</td>
          <td>'''+persona.nacionalidad+'''</td>
          <td>'''+persona.tel+'''</td>
          <td>'''+datetime.date.strftime(persona.fecha, '%d/%m/$Y')+'''</td>
          <td>'''+persona.zodiaco+'''</td>
          <td class="'''+persona.sexo+'''">'''+persona.sexo+'''</td>
          <td class="'''+persona.estado+'''">'''+persona.estado+'''</td>
          <td>'''+persona.email+'''</td>
          <td>'''+persona.provincia+'''</td>
          <td>'''+str(persona.coordenadas)+'''</td>
        </tr>
                '''
            html = html.replace('<!-- REGISTROS -->', temp)
            break
        elif opcion == 'U':
            while True:

                Limpiar()
                Mostrar(registros)

                print('Seleccione el registro:')

                try:
                    nregistro = int(input()) - 1

                    if not (0 <= nregistro < len(registros)):
                        OpcionInvalida()
                    else:
                        persona = registros[nregistro]
                        break
                except:
                    print('Algo salio mal')

            with open('Html/caso.html', 'r') as f:
                html = f.read()

            html = html.replace('<!--NoDocumento-->', persona.num_doc)
            html = html.replace('<!--Documento-->', persona.documento)
            html = html.replace('<!--Nombre-->', persona.nombre)
            html = html.replace('<!--Apellido-->', persona.apellido)
            html = html.replace('<!--Nacionalidad-->', persona.nacionalidad)
            html = html.replace('<!--Telefono-->', persona.tel)
            html = html.replace('<!--FechaNacimiento-->', datetime.date.strftime(persona.fecha,
                                                                                 '%d/%m/$Y'))
            html = html.replace('<!--SignoZodiacal-->', persona.zodiaco)
            html = html.replace('<!--Sexo-->', persona.sexo)
            html = html.replace('<!--Estado-->', persona.estado)
            html = html.replace('<!--Email-->', persona.email)
            html = html.replace('<!--Provincia-->', persona.provincia)
            html = html.replace('<!--Coordenadas-->', (persona.coordenadas))

            break

        elif opcion == 'C':
            return
        else:
            pass

    print('Pongale un nombre: ')
    nombre = input().strip()
    if nombre == '':
        nombre = 'AfectadosCoronavirus'
    file = upath + nombre + '.html'
    if os.path.exists(file):
        print('Este archivo ya existe...')
        print('[S] Para reemplazar')
        if not input().upper().strip() == 'S':
            return
    html = html.replace('Caso', nombre)
    with open(file, 'w') as f:
        f.write(html)
        print(nombre, ' ahora se encuentra en el escritorio')
    print('Escriba [A] si desea visualizar inmediatamente: ')
    if input().upper().strip() == 'A':
        webbrowser.open(file)
    return


def Mapa():
    Limpiar()

    with open('Html/mapa.html', 'r') as f:
        html = f.read()

    markers = []
    for persona in registros:
        tmp = '''
 L.marker(['''+str(persona.coordenadas[0])+''', '''+str(persona.coordenadas[1])+'''])
        .addTo(map)
        .bindPopup("'''+str(persona)+'''")
        .openPopup();    
        '''
        markers.append(tmp)

    html = html.replace('//MARCADORES', '\n'.join(markers))

    nombre = input('Pongale un nombre: ')
    if nombre == '':
        nombre = 'MapaAfectadosCoronavirus'
    file = upath + nombre + '.html'

    if os.path.exists(file):
        print('Este archivo ya existe...')
        print('[S] Para reemplazar')
        if not input().upper().strip() == 'S':
            return

    with open(file, 'w') as f:
        f.write(html)
        print(nombre, 'ahora se encuentra en el escritorio')

    if input('Escriba [A] si desea visualizar su mapa inmediatamente: ').upper().strip() == 'A':
        webbrowser.open(file)


def Estadistica():

    temp = ''
    for signo in numeros_misticos:
        temp += f'''
 --- {signo["Nombre"]} ---
 Enfermos: {signo["Enfermos"]}
 Recuperados: {signo["Recuperados"]}
 Muertos: {signo["Muertos"]} 
 \n         
        '''
    bot.send_message(channel, 'Estadistica Mistica\n' + temp)

    print('Mensaje enviado al canal de Telegram')


def Alerta(persona):
    bot.send_message(
        channel, 'Actualizacion Datos Coronavirus\n' + persona.ExportarTelegram())
    Estadistica()
    pass


def Guardar():
    Limpiar()

    while True:
        print('Guardar cambios [S/N]')
        opcion = input().upper()

        if opcion == 'S':
            with open(folderstorage + filestorage, 'wb') as f:
                pickle.dump(registros, f)

            with open(folderstorage + misticstorage, 'wb') as f:
                pickle.dump(numeros_misticos, f)

            print('Datos guardados')
            return

        elif opcion == 'N':
            print('Datos no guardados')
            return
        else:
            OpcionInvalida()


def Salir():

    print('Tenga buen dia')
    sys.exit()

# ---------------------------------------------------------------------- #
# ------------------------ FUNCIONES DE APOYO -------------------------- #
# ---------------------------------------------------------------------- #


def Mostrar(objeto):
    Limpiar()
    if type(objeto) is list:
        for i in range(len(objeto)):
            print(Fore.YELLOW + 'Registro: ' + str(i + 1))
            print(str(objeto[i]))
            print()
    elif type(objeto) is Persona:
        print(str(objeto))

# Para pruebas personales


def Pruebas():
    MiClase = Persona('Cedula', '40200753321', 'Alejandro', 'Germosen', 'Dominicano', 'M', datetime.date(
        2001, 9, 17), 'Virgo', '8295648234', '20197867@itla.com', 'Santo Domingo', 18.4801, -70.0169)
    try:
        Alerta(MiClase)
    except telegram.error.NetworkError:
        print('Error de Conexion')


# ---------------------------------------------------------------------- #
# ------------------------ INICIO DE EJECUCION ------------------------- #
# ---------------------------------------------------------------------- #


while True:
    OpcionMenu(Menu())
