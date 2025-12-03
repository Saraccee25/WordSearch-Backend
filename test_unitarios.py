"""
Suite de Tests Unitarios para Sopa de Letras
"""

import unittest
import json

from board_generator import (
    crear_tablero_vacio,
    puede_colocar_palabra,
    colocar_palabra_en_tablero,
    intentar_colocar_palabra,
    generar_tablero_garantizado,
    rellenar_espacios_vacios
)

from data_storage import DataStorage, Palabra, Tablero, Juego

from game_logic import (
    encontrar_palabra_en_tablero,
    crear_juego,
    resolver_juego,
    actualizar_progreso
)

from config import BOARD_SIZE, WORDS


# ================================================================
# TESTS: BOARD GENERATOR
# ================================================================
class TestBoardGenerator(unittest.TestCase):

    # ------------------------------------------------------------
    def test_crear_tablero_vacio(self):
        tablero = crear_tablero_vacio()
        self.assertEqual(len(tablero), BOARD_SIZE)
        self.assertEqual(len(tablero[0]), BOARD_SIZE)
        self.assertTrue(all(cell == ' ' for row in tablero for cell in row))

    # ------------------------------------------------------------
    def test_rellenar_espacios_vacios(self):
        tablero = crear_tablero_vacio()
        rellenar_espacios_vacios(tablero)
        self.assertTrue(all(cell != ' ' for row in tablero for cell in row))
        self.assertTrue(all(cell.isalpha() for row in tablero for cell in row))

    # ------------------------------------------------------------
    def test_puede_colocar_palabra_horizontal(self):
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        self.assertTrue(puede_colocar_palabra(tablero, palabra, 0, 0, 0, 1))
        self.assertFalse(puede_colocar_palabra(tablero, palabra, 0, 13, 0, 1))

    # ------------------------------------------------------------
    def test_puede_colocar_palabra_vertical(self):
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        self.assertTrue(puede_colocar_palabra(tablero, palabra, 0, 0, 1, 0))
        self.assertFalse(puede_colocar_palabra(tablero, palabra, 13, 0, 1, 0))

    # ------------------------------------------------------------
    def test_puede_colocar_palabra_diagonal(self):
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        self.assertTrue(puede_colocar_palabra(tablero, palabra, 0, 0, 1, 1))
        self.assertFalse(puede_colocar_palabra(tablero, palabra, 13, 13, 1, 1))

    # ------------------------------------------------------------
    def test_colocar_palabra_en_tablero(self):
        tablero = crear_tablero_vacio()
        palabra = "HOLA"
        colocar_palabra_en_tablero(tablero, palabra, 0, 0, 0, 1)
        self.assertEqual(tablero[0][0], 'H')
        self.assertEqual(tablero[0][1], 'O')
        self.assertEqual(tablero[0][2], 'L')
        self.assertEqual(tablero[0][3], 'A')

    # ------------------------------------------------------------
    def test_generar_tablero_garantizado(self):
        palabras = ["CASA", "PERRO", "GATO"]
        tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=5)
        self.assertEqual(len(palabras_colocadas), len(palabras))
        self.assertEqual(len(tablero), BOARD_SIZE)


# ================================================================
# TESTS: DATA STORAGE
# ================================================================
class TestDataStorage(unittest.TestCase):

    def setUp(self):
        self.storage = DataStorage()
        self.storage.limpiar_datos()

    # ------------------------------------------------------------
    def test_palabra_clase(self):
        palabra = Palabra("test", "CATEGORIA")
        self.assertEqual(palabra.texto, "TEST")
        self.assertEqual(palabra.categoria, "CATEGORIA")

    # ------------------------------------------------------------
    def test_tablero_clase(self):
        matriz = [['A', 'B'], ['C', 'D']]
        palabras = ["AB", "CD"]
        tablero = Tablero(1, matriz, palabras)
        self.assertEqual(tablero.id, 1)
        self.assertEqual(tablero.matriz, matriz)

    # ------------------------------------------------------------
    def test_juego_clase(self):
        juego = Juego(1, 1)
        self.assertFalse(juego.completado)
        juego.agregar_palabra_encontrada("TEST")
        self.assertIn("TEST", juego.palabras_encontradas)

    # ------------------------------------------------------------
    def test_agregar_palabra(self):
        resultado = self.storage.agregar_palabra("NUEVA", "TEST")
        self.assertTrue(resultado)
        self.assertIn("NUEVA", self.storage.obtener_palabras())

    # ------------------------------------------------------------
    def test_obtener_palabras(self):
        self.storage.agregar_palabra("PALABRA1", "CAT1")
        self.storage.agregar_palabra("PALABRA2", "CAT2")
        cat1 = self.storage.obtener_palabras("CAT1")
        self.assertIn("PALABRA1", cat1)

    # ------------------------------------------------------------
    def test_guardar_y_obtener_tablero(self):
        matriz = [['A'] * 15 for _ in range(15)]
        palabras = ["TEST"]
        tablero_id = self.storage.guardar_tablero(matriz, palabras)
        tablero = self.storage.obtener_tablero(tablero_id)
        self.assertEqual(tablero.palabras, palabras)

    # ------------------------------------------------------------
    def test_crear_y_obtener_juego(self):
        juego_id = self.storage.crear_juego(1)
        juego = self.storage.obtener_juego(juego_id)
        self.assertEqual(juego.tablero_id, 1)

    # ------------------------------------------------------------
    def test_actualizar_juego(self):
        juego_id = self.storage.crear_juego(1)
        self.storage.actualizar_juego(juego_id, palabra_encontrada="TEST")
        juego = self.storage.obtener_juego(juego_id)
        self.assertIn("TEST", juego.palabras_encontradas)

    # ------------------------------------------------------------
    def test_obtener_estadisticas(self):
        stats = self.storage.obtener_estadisticas()
        self.assertIn("total_palabras", stats)


# ================================================================
# TESTS: GAME LOGIC
# ================================================================
class TestGameLogic(unittest.TestCase):

    # ------------------------------------------------------------
    def test_encontrar_palabra_horizontal(self):
        tablero = [['H','O','L','A','X']] + [['X']*5 for _ in range(4)]
        pos = encontrar_palabra_en_tablero(tablero, "HOLA")
        self.assertEqual(pos[0], [0,0])
        self.assertEqual(pos[3], [0,3])

    # ------------------------------------------------------------
    def test_encontrar_palabra_vertical(self):
        tablero = [
            ['H','X','X','X','X'],
            ['O','X','X','X','X'],
            ['L','X','X','X','X'],
            ['A','X','X','X','X'],
            ['X','X','X','X','X']
        ]
        pos = encontrar_palabra_en_tablero(tablero, "HOLA")
        self.assertEqual(pos[3], [3,0])

    # ------------------------------------------------------------
    def test_encontrar_palabra_diagonal(self):
        tablero = [
            ['H','X','X','X','X'],
            ['X','O','X','X','X'],
            ['X','X','L','X','X'],
            ['X','X','X','A','X'],
            ['X','X','X','X','X']
        ]
        pos = encontrar_palabra_en_tablero(tablero, "HOLA")
        self.assertEqual(pos[3], [3,3])

    # ------------------------------------------------------------
    def test_encontrar_palabra_no_existe(self):
        tablero = [['X']*5 for _ in range(5)]
        self.assertIsNone(encontrar_palabra_en_tablero(tablero, "HOLA"))

    # ------------------------------------------------------------
    def test_crear_juego_json(self):
        datos = json.loads(crear_juego())
        self.assertIn("juego_id", datos)
        self.assertEqual(len(datos["palabras"]), 15)


# ================================================================
# TESTS: INTEGRACIÓN
# ================================================================
class TestIntegracion(unittest.TestCase):

    # ------------------------------------------------------------
    def test_flujo_completo_juego(self):
        datos_juego = json.loads(crear_juego())
        juego_id = datos_juego["juego_id"]
        tablero_id = datos_juego["tablero_id"]
        tablero = datos_juego["tablero"]
        palabras = datos_juego["palabras"]

        self.assertEqual(len(palabras), 15)

        for palabra in palabras:
            posiciones = encontrar_palabra_en_tablero(tablero, palabra)
            self.assertIsNotNone(posiciones)

        datos_resolver = json.loads(resolver_juego(juego_id, tablero_id))
        soluciones = datos_resolver["soluciones"]
        self.assertEqual(len(soluciones), len(palabras))


# ================================================================
# RUNNER
# ================================================================
def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestBoardGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))

    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite).wasSuccessful()


if __name__ == "__main__":
    exito = run_all_tests()
    exit(0 if exito else 1)
