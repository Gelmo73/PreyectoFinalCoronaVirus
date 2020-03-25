from colorama import init, Fore
import Utilidades
import datetime
from Utilidades import Limpiar, Continuar, OpcionInvalida


init()


class Persona:

    def __init__(self, doc, numdoc, nom, ape, nac, sexo, fecha, zodiaco, tel, email, prov, lat, lon):
        self.documento = doc
        self.num_doc = numdoc
        self.nombre = nom
        self.apellido = ape
        self.estado = 'Enfermo'
        self.nacionalidad = nac
        self.sexo = sexo
        self.fecha = fecha
        self.zodiaco = zodiaco
        self.tel = tel
        self.email = email
        self.provincia = prov
        self.coordenadas = lat, lon

    def __repr__(self):
        return f'''
{Fore.RED} Documento: {Fore.WHITE} {self.documento} [{self.num_doc}]
{Fore.RED} Nacionalidad: {Fore.WHITE} {self.nacionalidad}
{Fore.RED} Nombre: {Fore.WHITE} {self.nombre} {self.apellido}  {Fore.RED} Sexo: {Fore.WHITE} {self.sexo}
{Fore.RED} Fecha de Nacimiento: {Fore.WHITE} {datetime.date.strftime(self.fecha,'%d/%m/$Y')}
{Fore.RED} Signo Zodiacal: {Fore.WHITE} {self.zodiaco}
{Fore.RED} Estado: {Fore.GREEN} {self.estado}
{Fore.RED} Telefono: {Fore.WHITE} {self.tel}  {Fore.RED} Email: {Fore.WHITE} {self.email}
{Fore.RED} Provincia: {Fore.WHITE} {self.provincia}  {Fore.RED} Coordenadas: {Fore.WHITE} {self.coordenadas}       
        '''

    def setEstado(self, listado_mistico):
        Limpiar()

        if self.estado == 'Recuperado' or self.estado == 'Muerto':
            print(f'Su estado no puede ser cambiado de {self.estado}')
            return listado_mistico

        while True:
            print('Seleccione el estado:\n')
            print('[R] Recuperado')
            print('[M] Muerto')
            print('[NO] No Cambiar')

            opcion = input().upper()

            if opcion == 'R':
                self.estado = 'Recuperado'
                listado_mistico[self.zodiaco]['Recuperados'] += 1
                listado_mistico[self.zodiaco]['Enfermos'] -= 1
                break
            elif opcion == 'M':
                self.estado = 'Muerto'
                listado_mistico[self.zodiaco]['Muertos'] += 1
                listado_mistico[self.zodiaco]['Enfermos'] -= 1
                break
            elif opcion == 'NO':
                break
            else:
                OpcionInvalida()

        return listado_mistico

# ---------------------------------------------------------------------- #
# --------------------------- RESTRICCIONES ---------------------------- #
# ---------------------------------------------------------------------- #

    @staticmethod
    def RestriccionProvincia(listadoProvincia):

        while True:
            Limpiar()
            # Mostrar Provincias
            for i in range(len(listadoProvincia)):
                print(str(i + 1) + ': ' + listadoProvincia[i]['name'])

            print('Escoja el numero de la provincia a la que pertenece:')

            try:
                dato = listadoProvincia[int(input()) - 1]['name']
                break
            except:
                print('Opcion no valida')
                input()

        return dato

    @staticmethod
    def RestriccionCoordenadas():
        while True:
            Limpiar()

            try:
                print('Escriba la Latitud')
                lat = float(input())

                print('Escriba la Longitud')
                lon = float(input())
                break

            except Exception as e:
                print(f'Algo salio mal {e}')
                input()

        return lat, lon

    @staticmethod
    def RestriccionDocumento():

        while True:
            Limpiar()
            print('¿Eres [1] nativo o [2] extranjero?')
            opcion = input()
            if opcion == '1':
                return 'Cedula de Identidad'
            elif opcion == '2':
                return 'Pasaporte Extranjero'
            else:
                print('Opcion no valida')
                input()

    @staticmethod
    def RestriccionNacionalidad(documento):

        if documento == 'Cedula de Identidad':
            print('Le correnponde la nacionalidad dominicana por el tipo de su documento')
            return 'Dominicana'
        elif documento == 'Pasaporte Extranjero':
            print('Escriba su nacionalidad:')
            return input()

    @staticmethod
    def RestriccionNumeroDocumento(documento):

        print('Escriba el numero de su documento:')
        num_doc = input()

        if documento == 'Cedula de Identidad':

            if not Utilidades.ValidarCedula(num_doc):
                print('Documento Invalido')
                return '0'

        return num_doc

    @staticmethod
    def RestriccionNombre():
        print('Escriba su nombre:')
        return input()

    @staticmethod
    def RestriccionApellido():
        print('Escriba su apellido:')
        return input()

    @staticmethod
    def RestriccionTelefono():
        print('Escriba su telefono:')
        return input()

    @staticmethod
    def RestriccionFecha():

        while True:
            Limpiar()
            try:
                print('Escriba su dia, mes y año de nacimiento (en numeros)')
                dd = int(input())
                mm = int(input())
                yy = int(input())
                return datetime.date(yy, mm, dd)
            except Exception as e:
                print('Algo salio mal' + str(e))
                input()

    @staticmethod
    def RestriccionEmail():
        while True:
            Limpiar()

            print('Escriba su email:')
            email = input()

            if Utilidades.ValidarEmail(email):
                return email
            else:
                print('Email no valido')
                input()

    @staticmethod
    def RestriccionSexo():
        while True:
            Limpiar()
            print('Seleccione su sexo:\n')
            print('[M] Masculino')
            print('[F] Femenino')
            print('[O] Otro')
            print()
            sexo = input().upper()

            if sexo == 'M':
                break
            elif sexo == 'F':
                break
            elif sexo == 'O':
                break
            else:
                print('Opcion no valida')
                input()

        return sexo
