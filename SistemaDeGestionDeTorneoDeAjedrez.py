from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Resultado(ABC):
    @abstractmethod
    def obtenerPuntos(self):
        pass

    @abstractmethod
    def actualizaStats(self, jugador):
        pass


class Victoria(Resultado):
    def obtenerPuntos(self):
        return 1.0

    def actualizaStats(self, jugador):
        jugador.anotarVictoria()


class Empate(Resultado):
    def obtenerPuntos(self):
        return 0.5

    def actualizaStats(self, jugador):
        jugador.anotarEmpate()


class Derrota(Resultado):
    def obtenerPuntos(self):
        return 0.0

    def actualizaStats(self, jugador):
        jugador.anotarDerrota()


class Jugador:
    def __init__(
        self,
        nombre,
        edad,
        elo,
        puntos=0.0,
        partJugadas=0,
        victorias=0,
        empates=0,
        derrotas=0,
        historial=None,
    ):
        self.__nombre = nombre
        self.__edad = edad
        self.__elo = elo
        self.__puntos = puntos
        self.__partJugadas = partJugadas
        self.__victorias = victorias
        self.__empates = empates
        self.__derrotas = derrotas
        self.__historial = historial or [0.0]

    @property
    def nombre(self):
        return self.__nombre

    @property
    def edad(self):
        return self.__edad

    @property
    def elo(self):
        return self.__elo

    @property
    def puntos(self):
        return self.__puntos

    @property
    def partJugadas(self):
        return self.__partJugadas

    @property
    def victorias(self):
        return self.__victorias

    @property
    def empates(self):
        return self.__empates

    @property
    def derrotas(self):
        return self.__derrotas

    @property
    def historial(self):
        return self.__historial

    def registrarRes(self, resultadoObj, ronda):
        if self.__nombre == "BYE":
            return

        puntosObtenidos = resultadoObj.obtenerPuntos()
        self.__puntos += puntosObtenidos
        self.__partJugadas += 1

        while len(self.__historial) <= ronda:
            self.__historial.append(self.__historial[-1])
        self.__historial[ronda] = self.__puntos

        resultadoObj.actualizaStats(self)

    def anotarVictoria(self):
        self.__victorias += 1

    def anotarEmpate(self):
        self.__empates += 1

    def anotarDerrota(self):
        self.__derrotas += 1

    def reiniciarStats(self):
        self.__puntos = 0.0
        self.__partJugadas = 0
        self.__victorias = 0
        self.__empates = 0
        self.__derrotas = 0
        self.__historial = [0.0]

    def __str__(self):
        return f"Nombre: {self.__nombre}, ELO: {self.__elo}, Pts: {self.__puntos}"


class Partida:
    def __init__(self, J1, J2, ronda, resJ1=None):
        self.__jugadores = [J1, J2]
        self.__ronda = ronda
        self.__resJ1 = resJ1

    @property
    def J1(self):
        return self.__jugadores[0]

    @property
    def J2(self):
        return self.__jugadores[1]

    @property
    def resultJ1(self):
        return self.__resJ1

    @property
    def ronda(self):
        return self.__ronda

    def setResultado(self, valorRes):
        self.__resJ1 = valorRes

        if valorRes == 1.0:
            resultadoUno = Victoria()
            resultadoDos = Derrota()
        elif valorRes == 0.5:
            resultadoUno = Empate()
            resultadoDos = Empate()
        else:
            resultadoUno = Derrota()
            resultadoDos = Victoria()

        self.__jugadores[0].registrarRes(resultadoUno, self.__ronda)
        self.__jugadores[1].registrarRes(resultadoDos, self.__ronda)

    def obtenerDatos(self):
        return [
            self.__ronda,
            self.__jugadores[0].nombre,
            self.__jugadores[1].nombre,
            self.__resJ1,
        ]


class Ronda:
    def __init__(self, numero):
        self.__numero = numero
        self.__partidas = []

    @property
    def numero(self):
        return self.__numero

    @property
    def partidas(self):
        return self.__partidas

    def agregarPartida(self, partida):
        self.__partidas.append(partida)


class Torneo:
    def __init__(self):
        self.__inscritos = {}
        self.__rondas = {}
        self.__fixGenerado = False
        self.__bye = Jugador("BYE", 0, 0)

    def regJugador(self):
        if self.__fixGenerado:
            print("Fixture ya generado.")
            return

        nombreJugador = input("Nombre: ")

        if nombreJugador.upper() == "BYE":
            print("No se puede asignar ese nombre a un jugador.")
            return

        if nombreJugador in self.__inscritos:
            print("El nombre ya existe.")
            return

        try:
            edadJugador = int(input("Edad: "))
            eloJugador = int(input("ELO: "))

            if edadJugador < 0 or eloJugador < 0:
                print("Se debe ingresar valores positivos.")
                return

            self.__inscritos[nombreJugador] = Jugador(
                nombreJugador, edadJugador, eloJugador
            )
            print("Registrado.")
        except ValueError:
            print("Ingrese números enteros válidos.")

    def generarFixture(self):
        if self.__fixGenerado:
            print("Fixture ya generado.")
            return

        listaJugadores = list(self.__inscritos.values())

        if len(listaJugadores) % 2 != 0:
            listaJugadores.append(self.__bye)

        cantJugadores = len(listaJugadores)
        numeroRondas = cantJugadores - 1
        partxRonda = cantJugadores // 2

        if cantJugadores < 2:
            print("Se necesitan al menos 2 jugadores.")
            return

        print(f"Generando torneo ({numeroRondas} rondas)...")

        for r in range(numeroRondas):
            numRondActual = r + 1
            objetoRonda = Ronda(numRondActual)

            for i in range(partxRonda):
                J1 = listaJugadores[i]
                J2 = listaJugadores[cantJugadores - 1 - i]

                nuevaPartida = None
                if r % 2 == 0:
                    nuevaPartida = Partida(J1, J2, numRondActual)
                else:
                    nuevaPartida = Partida(J2, J1, numRondActual)

                objetoRonda.agregarPartida(nuevaPartida)

            self.__rondas[numRondActual] = objetoRonda

            jugadorFijo = listaJugadores[0]
            restoJugadores = listaJugadores[1:]
            restoJugadores.insert(0, restoJugadores.pop())
            listaJugadores = [jugadorFijo] + restoJugadores

        self.__fixGenerado = True
        print("Fixture generado.")

    def registrarRes(self):
        if not self.__fixGenerado:
            print("Genere el fixture primero.")
            return

        for numRondActual in sorted(self.__rondas.keys()):
            print(f"\n--- RONDA {numRondActual} ---")

            objRonda = self.__rondas[numRondActual]

            for partida in objRonda.partidas:
                if partida.J1 == self.__bye:
                    if str(partida.resultJ1) == "nan" or partida.resultJ1 is None:
                        partida.setResultado(0.0)
                        print(f"{partida.J2.nombre} recibe punto por BYE.")
                    else:
                        print(f"{partida.J2.nombre} ya tiene su punto por BYE.")
                    continue

                if partida.J2 == self.__bye:
                    if str(partida.resultJ1) == "nan" or partida.resultJ1 is None:
                        partida.setResultado(1.0)
                        print(f"{partida.J1.nombre} recibe punto por BYE.")
                    else:
                        print(f"{partida.J1.nombre} ya tiene su punto por BYE.")
                    continue

                print(f"{partida.J1.nombre} VS {partida.J2.nombre}")

                if str(partida.resultJ1) != "nan" and partida.resultJ1 is not None:
                    print(f"Ya registrado: {partida.resultJ1}")
                    continue

                entValida = False
                while not entValida:
                    try:
                        valInput = float(
                            input(f"Resultado de {partida.J1.nombre} (1.0, 0.5, 0.0):")
                        )
                        if valInput in [1.0, 0.5, 0.0]:
                            partida.setResultado(valInput)
                            entValida = True
                        else:
                            print("Valor inválido. Use 1.0, 0.5 o 0.0")
                    except ValueError:
                        print("Debe ingresar un número.")

        print("\n--- Registro finalizado ---")

    def verClasif(self):
        datosTabla = []
        for jugador in self.__inscritos.values():
            if jugador != self.__bye:
                datosTabla.append(
                    [
                        jugador.nombre,
                        jugador.elo,
                        jugador.puntos,
                        jugador.partJugadas,
                        jugador.victorias,
                        jugador.empates,
                        jugador.derrotas,
                    ]
                )

        if not datosTabla:
            print("Sin datos.")
            return

        dfTabla = pd.DataFrame(
            datosTabla, columns=["Jugador", "ELO", "Pts", "PJ", "PG", "PE", "PP"]
        )

        print("\n--- TABLA DE POSICIONES ---\n")
        print(dfTabla.sort_values(by="Pts", ascending=False).to_string(index=False))
        print("\n")

    def verFixture(self):
        if not self.__fixGenerado:
            return
        for numeroRonda in sorted(self.__rondas.keys()):
            print(f"\n--- RONDA {numeroRonda} ---")

            for partida in self.__rondas[numeroRonda].partidas:
                if partida.J1 == self.__bye or partida.J2 == self.__bye:
                    continue

                res = str(partida.resultJ1)
                if res == "nan" or res == "None":
                    resultadoStr = "vs"
                else:
                    resultadoStr = f"{partida.resultJ1} - {1.0 - partida.resultJ1}"

                print(
                    f"{partida.J1.nombre:<15} {resultadoStr:^7} {partida.J2.nombre:>15}"
                )

    def verEstadisticas(self):
        if not self.__inscritos:
            return
        jugValidos = [
            jugador for jugador in self.__inscritos.values() if jugador != self.__bye
        ]
        if not jugValidos:
            return

        arrayNombres = np.array([jugador.nombre for jugador in jugValidos])
        arrayVictorias = np.array([jugador.victorias for jugador in jugValidos])
        arrayEmpates = np.array([jugador.empates for jugador in jugValidos])
        arrayDerrotas = np.array([jugador.derrotas for jugador in jugValidos])
        arrayPuntos = np.array([jugador.puntos for jugador in jugValidos])

        print("\n1. Ranking\n2. Victorias\n3. Evolución Puntos\n4. Desempeño\n5. Salir")
        opcUsuario = input("Opción: ")

        if opcUsuario == "1":
            plt.bar(arrayNombres, arrayPuntos, color="#46BFC7")
            plt.xlabel("Jugadores")
            plt.ylabel("Puntos")
            plt.title("Tabla de Posiciones")
            plt.show()

        elif opcUsuario == "2":
            totalVictorias = sum(arrayVictorias)
            if totalVictorias == 0:
                print("Aún no hay victorias.")
            else:
                cls = ["#C75FB5", "#4858B8", "#DEDB57", "#B85862", "#70E657"]
                plt.pie(
                    arrayVictorias, labels=arrayNombres, autopct="%1.1f%%", colors=cls
                )
                plt.title("Porcentaje de Victorias por Jugador")
                plt.show()

        elif opcUsuario == "3":
            colores = [
                "#0C0BD6",
                "#42992E",
                "#E31010",
                "#5CBFD6",
                "#C90A79",
                "#F8FA00",
                "#080707",
                "#FF7600",
            ]

            for i, jugador in enumerate(jugValidos):
                x = range(len(jugador.historial))
                y = jugador.historial
                color_actual = colores[i % len(colores)]
                plt.plot(x, y, marker="o", label=jugador.nombre, color=color_actual)

            plt.xlabel("Rondas")
            plt.ylabel("Puntos Acumulados")
            plt.title("Evolución de Puntos por Ronda")
            plt.legend()
            plt.grid(True)
            plt.show()

        elif opcUsuario == "4":
            x = np.arange(len(arrayNombres))
            width = 0.25

            plt.bar(
                x - width, arrayVictorias, width, label="Victorias", color="#74D162"
            )
            plt.bar(x, arrayEmpates, width, label="Empates", color="#6273D1")
            plt.bar(x + width, arrayDerrotas, width, label="Derrotas", color="#A6391E")
            plt.xlabel("Jugadores")
            plt.ylabel("Cantidad")
            plt.title("Desempeño por Jugador")
            plt.xticks(x, arrayNombres)
            plt.legend()
            plt.show()

    def guardarDatos(self):
        datosJugadores = []
        for jugador in self.__inscritos.values():
            if jugador != self.__bye:
                datosJugadores.append(
                    [
                        jugador.nombre,
                        jugador.edad,
                        jugador.elo,
                        jugador.puntos,
                        jugador.partJugadas,
                        jugador.victorias,
                        jugador.empates,
                        jugador.derrotas,
                        str(jugador.historial),
                    ]
                )

        if datosJugadores:
            pd.DataFrame(
                datosJugadores,
                columns=["Nom", "Edad", "Elo", "Pts", "PJ", "V", "E", "D", "Hist"],
            ).to_excel("jugadores.xlsx", index=False)

        datosPartidas = []
        for ronda in self.__rondas.values():
            for partida in ronda.partidas:
                datosPartidas.append(partida.obtenerDatos())

        if datosPartidas:
            pd.DataFrame(datosPartidas, columns=["Ronda", "J1", "J2", "Res"]).to_excel(
                "partidas.xlsx", index=False
            )
        print("Datos guardados.")

    def cargarDatos(self):
        dfJugadores = pd.read_excel("jugadores.xlsx")
        dfJugadores = dfJugadores.dropna(subset=["Nom"])

        for i in range(len(dfJugadores)):
            fila = dfJugadores.iloc[i]
            historialStr = str(fila["Hist"])
            listaHistorial = [0.0]

            if "[" in historialStr and "]" in historialStr:
                contenido = historialStr.replace("[", "").replace("]", "")
                if len(contenido) > 0:
                    partes = contenido.split(",")
                    listaHistorial = []
                    for p in partes:
                        if p.strip() != "":
                            listaHistorial.append(float(p))

            jugadorObj = Jugador(
                fila["Nom"],
                int(fila["Edad"]),
                int(fila["Elo"]),
                float(fila["Pts"]),
                int(fila["PJ"]),
                int(fila["V"]),
                int(fila["E"]),
                int(fila["D"]),
                listaHistorial,
            )
            self.__inscritos[jugadorObj.nombre] = jugadorObj

        dfPartidas = pd.read_excel("partidas.xlsx")
        dfPartidas = dfPartidas.dropna(subset=["Ronda", "J1", "J2"])

        if len(dfPartidas) > 0:
            self.__fixGenerado = True
            self.__rondas = {}
            valoresPartidas = dfPartidas.values

            for filaP in valoresPartidas:
                numRonda = int(filaP[0])

                if numRonda not in self.__rondas:
                    self.__rondas[numRonda] = Ronda(numRonda)

                J1 = self.__inscritos.get(str(filaP[1]), self.__bye)
                J2 = self.__inscritos.get(str(filaP[2]), self.__bye)

                resultadoRaw = filaP[3]
                resultado = None
                if str(resultadoRaw) != "nan" and str(resultadoRaw).strip() != "":
                    resultado = float(resultadoRaw)

                self.__rondas[numRonda].agregarPartida(
                    Partida(J1, J2, numRonda, resultado)
                )

        print("Datos cargados.")

    def reiniciar(self):
        confirmacion = input("Confirmar reinicio (S/N): ")
        if confirmacion == "S" or confirmacion == "s":
            self.__inscritos = {}
            self.__rondas = {}
            self.__fixGenerado = False
            print("Reiniciado.")


def menu():
    torneo = Torneo()

    while True:
        print("\n--- TORNEO DE AJEDREZ  ---")
        print("1. Registrar Jugador")
        print("2. Generar Fixture")
        print("3. Registrar Resultados")
        print("4. Ver Tabla")
        print("5. Ver Fixture")
        print("6. Gráficos")
        print("7. Reiniciar")
        print("8. Guardar y Salir")
        print("9. Cargar Datos")
        opcionMenu = input("Opción: ")

        if opcionMenu == "1":
            torneo.regJugador()
        elif opcionMenu == "2":
            torneo.generarFixture()
        elif opcionMenu == "3":
            torneo.registrarRes()
        elif opcionMenu == "4":
            torneo.verClasif()
        elif opcionMenu == "5":
            torneo.verFixture()
        elif opcionMenu == "6":
            torneo.verEstadisticas()
        elif opcionMenu == "7":
            torneo.reiniciar()
        elif opcionMenu == "8":
            torneo.guardarDatos()
            break
        elif opcionMenu == "9":
            torneo.cargarDatos()
        else:
            print("Opción inválida.")


menu()
