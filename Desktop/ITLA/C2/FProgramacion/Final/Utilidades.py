import json
import os
import re
from geopy.geocoders import Nominatim
from unidecode import unidecode  # Buscar que es


def Limpiar():
    os.system('cls')


def Continuar():
    print('Presione [Enter] para continuar')
    input()


def OpcionInvalida():
    print('Opcion no valida')
    Continuar()


"""
Datos de ejemplo:
San jose de ocoa: 18.5466099, -70.5063095
San Cristóbal: 18.4166698, -70.0999985
Peravia: 18.2796402, -70.3318481
"""
"""
lat: Latitud
lon: Longitud
provincia: Provincia(en lower)
"""


def ValidarCoordenadas(lat, lon, provincia):

    provincia = provincia.lower()

    geolocator = Nominatim(user_agent='ITLA')

    try:
        coordenadas = lat, lon
        localizacion = geolocator.reverse(coordenadas)

        # Obteniendo el nombre del pais
        get_pais = localizacion.raw['address']['country']
        # Obteniendo el nombre de la provincia
        get_provincia = localizacion.raw['address']['state'].lower()

    except KeyError:
        print(f'Tu dirrecion apunta a un area no valida')
        return False
    except Exception as e:
        print('Algo salio mal' + str(e))
        return False

    if not get_pais == 'República Dominicana':
        print('La coordenada que ingreso no pertenece a la Republica Dominciana')
        return False

    # print(get_provincia)
    # print(provincia)

    if not (provincia == get_provincia or provincia == unidecode(get_provincia)):
        print(
            f'La provincia [{provincia}] no coincide con las coordenadas {coordenadas}. Estas pertenecen a {get_provincia}')
        return False

    return True


def ObtenerSignoZodiacal(mm, dd):

    with open('Json/Zodiaco.json') as file:
        Estaciones = json.load(file)

    for i in range(0, len(Estaciones)):
        if (i + 1) == mm:
            if dd <= Estaciones[i]['DiaDeCambio']:
                return Estaciones[i]['Nombres'][0]
            else:
                return Estaciones[i]['Nombres'][1]


# Validación de cédula dominicana en Python por: Freddy Rondon

def ValidarCedula(cedula):

    # La cédula debe tener 11 dígitos
    cedula = cedula.replace('-', '')
    if len(cedula) == 11:
        if (0 < int(cedula[0:3]) < 122 or int(cedula[0:3]) == 402):
            suma = 0
            mutliplicador = 1
            verificador = 0

            # Los dígitos pares valen 2 y los impares 1
            mutliplicador = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
            for i in range(10):

                # Se multiplica cada dígito por su paridad
                digito = int(cedula[i]) * mutliplicador[i]

                # Si la multiplicación da de dos dígitos, se suman entre sí
                if digito > 9:
                    digito = digito // 10 + digito % 10

                # Y se va haciendo la acumulación de esa suma
                suma += digito

            # Al final se obtiene el verificador con la siguiente fórmula
            verificador = (10 - (suma % 10)) % 10

            # Se comprueba que coincidan
            if (verificador == int(cedula[10])):
                return True
            # El dígito verificador no es válido
            else:
                return False
        # La serie no es válida
        else:
            return False
    # No tiene 11 dígitos
    else:
        return False


def ValidarEmail(email):
    if re.match(r'[a-zA-Z0-9._-]+@[a-zA-Z-]+\.([a-zA-Z-]+\.)?(com|net|edu|gov)', email):
        return True
    else:
        return False


def Buscar(valor, listado):

    encontrados = []
    for registro in listado:
        if (registro.nombre + registro.apellido).lower().find(valor) >= 0:
            encontrados.append(registro)
    if len(encontrados) > 0:
        return encontrados
    else:
        print('Ningun registro coicidente')
        Continuar()
        return listado


jsonstr = {
    "Capricornio": {
        "Nombre": "Capricornio",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Acuario": {
        "Nombre": "Acuario",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Piscis": {
        "Nombre": "Piscis",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Aries": {
        "Nombre": "Aries",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Tauro": {
        "Nombre": "Tauro",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Geminis": {
        "Nombre": "Geminis",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Cancer": {
        "Nombre": "Cancer",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Leo": {
        "Nombre": "Leo",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Virgo": {
        "Nombre": "Virgo",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Libra": {
        "Nombre": "Libra",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Escorpio": {
        "Nombre": "Escorpio",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    },

    "Sagitario": {
        "Nombre": "Sagitario",
        "Enfermos": 0,
        "Recuperados": 0,
        "Muertos": 0
    }
}
