"""
Suite de Tests Unitarios para Sopa de Letras
Ejecutar con: python test_unitarios.py
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


class TestBoardGenerator(unittest.TestCase):
    """Tests para el generador de tableros"""
    
    def test_crear_tablero_vacio(self):
        """Test: Crear tablero vacío con espacios"""
        tablero = crear_tablero_vacio()
        
        self.assertEqual(len(tablero), BOARD_SIZE)
        self.assertEqual(len(tablero[0]), BOARD_SIZE)
        self.assertTrue(all(cell == ' ' for row in tablero for cell in row))
        print("✓ Test crear_tablero_vacio: PASS")
    
    def test_rellenar_espacios_vacios(self):
        """Test: Rellenar espacios con letras aleatorias"""
        tablero = crear_tablero_vacio()
        rellenar_espacios_vacios(tablero)
        
        # No debe haber espacios vacíos
        self.assertTrue(all(cell != ' ' for row in tablero for cell in row))
        # Todas deben ser letras
        self.assertTrue(all(cell.isalpha() for row in tablero for cell in row))
        print("✓ Test rellenar_espacios_vacios: PASS")
    
    def test_puede_colocar_palabra_horizontal(self):
        """Test: Verificar colocación horizontal"""
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        
        # Debe poder colocar en posición válida
        self.assertTrue(puede_colocar_palabra(tablero, palabra, 0, 0, 0, 1))
        
        # No debe poder colocar fuera de límites
        self.assertFalse(puede_colocar_palabra(tablero, palabra, 0, 13, 0, 1))
        print("✓ Test puede_colocar_palabra_horizontal: PASS")
    
    def test_puede_colocar_palabra_vertical(self):
        """Test: Verificar colocación vertical"""
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        
        # Debe poder colocar en posición válida
        self.assertTrue(puede_colocar_palabra(tablero, palabra, 0, 0, 1, 0))
        
        # No debe poder colocar fuera de límites
        self.assertFalse(puede_colocar_palabra(tablero, palabra, 13, 0, 1, 0))
        print("✓ Test puede_colocar_palabra_vertical: PASS")
    
    def test_puede_colocar_palabra_diagonal(self):
        """Test: Verificar colocación diagonal"""
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        
        # Debe poder colocar en diagonal
        self.assertTrue(puede_colocar_palabra(tablero, palabra, 0, 0, 1, 1))
        
        # No debe poder colocar fuera de límites
        self.assertFalse(puede_colocar_palabra(tablero, palabra, 13, 13, 1, 1))
        print("✓ Test puede_colocar_palabra_diagonal: PASS")
    
    def test_colocar_palabra_en_tablero(self):
        """Test: Colocar palabra físicamente"""
        tablero = crear_tablero_vacio()
        palabra = "HOLA"
        
        colocar_palabra_en_tablero(tablero, palabra, 0, 0, 0, 1)
        
        self.assertEqual(tablero[0][0], 'H')
        self.assertEqual(tablero[0][1], 'O')
        self.assertEqual(tablero[0][2], 'L')
        self.assertEqual(tablero[0][3], 'A')
        print("✓ Test colocar_palabra_en_tablero: PASS")
    
    def test_intentar_colocar_palabra(self):
        """Test: Intentar colocar palabra con reintentos"""
        tablero = crear_tablero_vacio()
        palabra = "TEST"
        
        resultado = intentar_colocar_palabra(tablero, palabra, max_intentos=50)
        
        self.assertTrue(resultado)
        # Verificar que la palabra está en el tablero
        tablero_str = ''.join([''.join(row) for row in tablero])
        self.assertIn('TEST', tablero_str + ''.join([''.join(row[::-1]) for row in tablero]))
        print("✓ Test intentar_colocar_palabra: PASS")
    
    def test_generar_tablero_garantizado(self):
        """Test: Generar tablero con TODAS las palabras"""
        palabras = ["CASA", "PERRO", "GATO"]
        
        tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=5)
        
        self.assertEqual(len(palabras_colocadas), len(palabras))
        self.assertEqual(len(tablero), BOARD_SIZE)
        print(f"✓ Test generar_tablero_garantizado: PASS ({len(palabras_colocadas)}/{len(palabras)} palabras)")


class TestDataStorage(unittest.TestCase):
    """Tests para el almacenamiento con ArrayLists"""
    
    def setUp(self):
        """Crear storage limpio antes de cada test"""
        self.storage = DataStorage()
        self.storage.limpiar_datos()
    
    def test_palabra_clase(self):
        """Test: Clase Palabra"""
        palabra = Palabra("test", "CATEGORIA")
        
        self.assertEqual(palabra.texto, "TEST")
        self.assertEqual(palabra.categoria, "CATEGORIA")
        
        dict_palabra = palabra.to_dict()
        self.assertIn("texto", dict_palabra)
        self.assertIn("categoria", dict_palabra)
        print("✓ Test Palabra clase: PASS")
    
    def test_tablero_clase(self):
        """Test: Clase Tablero"""
        matriz = [['A', 'B'], ['C', 'D']]
        palabras = ["AB", "CD"]
        tablero = Tablero(1, matriz, palabras)
        
        self.assertEqual(tablero.id, 1)
        self.assertEqual(tablero.matriz, matriz)
        self.assertEqual(tablero.palabras, palabras)
        self.assertIsNotNone(tablero.fecha_creacion)
        print("✓ Test Tablero clase: PASS")
    
    def test_juego_clase(self):
        """Test: Clase Juego"""
        juego = Juego(1, 1)
        
        self.assertEqual(juego.id, 1)
        self.assertEqual(juego.tablero_id, 1)
        self.assertEqual(len(juego.palabras_encontradas), 0)
        self.assertFalse(juego.completado)
        
        # Agregar palabra
        juego.agregar_palabra_encontrada("TEST")
        self.assertEqual(len(juego.palabras_encontradas), 1)
        
        # No duplicar
        juego.agregar_palabra_encontrada("TEST")
        self.assertEqual(len(juego.palabras_encontradas), 1)
        
        # Finalizar
        juego.finalizar()
        self.assertTrue(juego.completado)
        self.assertIsNotNone(juego.tiempo_fin)
        print("✓ Test Juego clase: PASS")
    
    def test_agregar_palabra(self):
        """Test: Agregar palabra al ArrayList"""
        resultado = self.storage.agregar_palabra("NUEVA", "TEST")
        
        self.assertTrue(resultado)
        self.assertIn("NUEVA", self.storage.obtener_palabras())
        
        # No duplicar
        resultado2 = self.storage.agregar_palabra("NUEVA", "TEST")
        self.assertFalse(resultado2)
        print("✓ Test agregar_palabra: PASS")
    
    def test_obtener_palabras(self):
        """Test: Obtener palabras del ArrayList"""
        self.storage.agregar_palabra("PALABRA1", "CAT1")
        self.storage.agregar_palabra("PALABRA2", "CAT2")
        
        todas = self.storage.obtener_palabras()
        cat1 = self.storage.obtener_palabras("CAT1")
        
        self.assertGreaterEqual(len(todas), 2)
        self.assertIn("PALABRA1", cat1)
        self.assertNotIn("PALABRA2", cat1)
        print("✓ Test obtener_palabras: PASS")
    
    def test_guardar_y_obtener_tablero(self):
        """Test: Guardar y recuperar tablero"""
        matriz = [['A'] * 15 for _ in range(15)]
        palabras = ["TEST"]
        
        tablero_id = self.storage.guardar_tablero(matriz, palabras)
        tablero = self.storage.obtener_tablero(tablero_id)
        
        self.assertIsNotNone(tablero)
        self.assertEqual(tablero.id, tablero_id)
        self.assertEqual(tablero.palabras, palabras)
        print("✓ Test guardar_y_obtener_tablero: PASS")
    
    def test_crear_y_obtener_juego(self):
        """Test: Crear y recuperar juego"""
        juego_id = self.storage.crear_juego(1)
        juego = self.storage.obtener_juego(juego_id)
        
        self.assertIsNotNone(juego)
        self.assertEqual(juego.id, juego_id)
        self.assertEqual(juego.tablero_id, 1)
        print("✓ Test crear_y_obtener_juego: PASS")
    
    def test_actualizar_juego(self):
        """Test: Actualizar estado de juego"""
        juego_id = self.storage.crear_juego(1)
        
        # Agregar palabra encontrada
        self.storage.actualizar_juego(juego_id, palabra_encontrada="TEST")
        juego = self.storage.obtener_juego(juego_id)
        self.assertIn("TEST", juego.palabras_encontradas)
        
        # Finalizar
        self.storage.actualizar_juego(juego_id, finalizar=True)
        juego = self.storage.obtener_juego(juego_id)
        self.assertTrue(juego.completado)
        print("✓ Test actualizar_juego: PASS")
    
    def test_obtener_estadisticas(self):
        """Test: Obtener estadísticas"""
        stats = self.storage.obtener_estadisticas()
        
        self.assertIn("total_palabras", stats)
        self.assertIn("total_tableros", stats)
        self.assertIn("total_juegos", stats)
        self.assertIn("juegos_completados", stats)
        print("✓ Test obtener_estadisticas: PASS")


class TestGameLogic(unittest.TestCase):
    """Tests para la lógica del juego"""
    
    def test_encontrar_palabra_horizontal(self):
        """Test: Encontrar palabra horizontal"""
        tablero = [
            ['H', 'O', 'L', 'A', 'X'],
            ['X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X']
        ]
        
        posiciones = encontrar_palabra_en_tablero(tablero, "HOLA")
        
        self.assertIsNotNone(posiciones)
        self.assertEqual(len(posiciones), 4)
        self.assertEqual(posiciones[0], [0, 0])
        self.assertEqual(posiciones[3], [0, 3])
        print("✓ Test encontrar_palabra_horizontal: PASS")
    
    def test_encontrar_palabra_vertical(self):
        """Test: Encontrar palabra vertical"""
        tablero = [
            ['H', 'X', 'X', 'X', 'X'],
            ['O', 'X', 'X', 'X', 'X'],
            ['L', 'X', 'X', 'X', 'X'],
            ['A', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X']
        ]
        
        posiciones = encontrar_palabra_en_tablero(tablero, "HOLA")
        
        self.assertIsNotNone(posiciones)
        self.assertEqual(len(posiciones), 4)
        self.assertEqual(posiciones[0], [0, 0])
        self.assertEqual(posiciones[3], [3, 0])
        print("✓ Test encontrar_palabra_vertical: PASS")
    
    def test_encontrar_palabra_diagonal(self):
        """Test: Encontrar palabra diagonal"""
        tablero = [
            ['H', 'X', 'X', 'X', 'X'],
            ['X', 'O', 'X', 'X', 'X'],
            ['X', 'X', 'L', 'X', 'X'],
            ['X', 'X', 'X', 'A', 'X'],
            ['X', 'X', 'X', 'X', 'X']
        ]
        
        posiciones = encontrar_palabra_en_tablero(tablero, "HOLA")
        
        self.assertIsNotNone(posiciones)
        self.assertEqual(len(posiciones), 4)
        self.assertEqual(posiciones[0], [0, 0])
        self.assertEqual(posiciones[3], [3, 3])
        print("✓ Test encontrar_palabra_diagonal: PASS")
    
    def test_encontrar_palabra_no_existe(self):
        """Test: Palabra que no existe en el tablero"""
        tablero = [['X'] * 5 for _ in range(5)]
        
        posiciones = encontrar_palabra_en_tablero(tablero, "HOLA")
        
        self.assertIsNone(posiciones)
        print("✓ Test encontrar_palabra_no_existe: PASS")
    
    def test_crear_juego_json(self):
        """Test: Crear juego retorna JSON válido"""
        resultado = crear_juego()
        
        # Debe ser JSON válido
        datos = json.loads(resultado)
        
        self.assertIn("juego_id", datos)
        self.assertIn("tablero_id", datos)
        self.assertIn("tablero", datos)
        self.assertIn("palabras", datos)
        self.assertIn("total_palabras", datos)
        
        # Verificar que tiene las 15 palabras
        self.assertEqual(len(datos["palabras"]), 15)
        print(f"✓ Test crear_juego_json: PASS (15 palabras)")


class TestIntegracion(unittest.TestCase):
    """Tests de integración completa"""
    
    def test_flujo_completo_juego(self):
        """Test: Flujo completo - crear juego, buscar palabras, resolver"""
        print("\n" + "="*60)
        print("🧪 TEST DE INTEGRACIÓN COMPLETO")
        print("="*60)
        
        # 1. Crear juego
        resultado_crear = crear_juego()
        datos_juego = json.loads(resultado_crear)
        
        juego_id = datos_juego["juego_id"]
        tablero_id = datos_juego["tablero_id"]
        tablero = datos_juego["tablero"]
        palabras = datos_juego["palabras"]
        
        print(f"\n1. ✓ Juego creado - ID: {juego_id}")
        print(f"   Palabras en el juego: {len(palabras)}")
        
        # Verificar que son las 15 palabras correctas
        self.assertEqual(len(palabras), 15)
        for palabra in palabras:
            self.assertIn(palabra, WORDS)
        
        # 2. Verificar que cada palabra está en el tablero
        print(f"\n2. Verificando que todas las palabras están en el tablero:")
        palabras_verificadas = 0
        for palabra in palabras:
            posiciones = encontrar_palabra_en_tablero(tablero, palabra)
            if posiciones:
                palabras_verificadas += 1
                print(f"   ✓ {palabra}: Encontrada")
            else:
                print(f"   ❌ {palabra}: NO encontrada (ERROR)")
        
        self.assertEqual(palabras_verificadas, len(palabras), 
                        f"Solo {palabras_verificadas}/{len(palabras)} palabras encontradas")
        
        # 3. Resolver juego
        print(f"\n3. Resolviendo juego...")
        resultado_resolver = resolver_juego(juego_id, tablero_id)
        datos_resolver = json.loads(resultado_resolver)
        
        soluciones = datos_resolver["soluciones"]
        print(f"   ✓ Soluciones encontradas: {len(soluciones)}/{len(palabras)}")
        
        self.assertEqual(len(soluciones), len(palabras))
        
        # 4. Verificar cada solución
        print(f"\n4. Verificando cada solución:")
        for solucion in soluciones:
            palabra = solucion["palabra"]
            posiciones = solucion["posiciones"]
            
            # Reconstruir palabra desde posiciones
            palabra_reconstruida = ''.join([
                tablero[pos[0]][pos[1]] for pos in posiciones
            ])
            
            self.assertEqual(palabra, palabra_reconstruida)
            print(f"   ✓ {palabra}: Verificada")
        
        print("\n" + "="*60)
        print("✅ TEST DE INTEGRACIÓN COMPLETADO EXITOSAMENTE")
        print("="*60 + "\n")


def run_all_tests():
    """Ejecutar todos los tests con reporte detallado"""
    print("\n" + "="*70)
    print("🧪 EJECUTANDO SUITE COMPLETA DE TESTS UNITARIOS")
    print("="*70 + "\n")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de tests
    suite.addTests(loader.loadTestsFromTestCase(TestBoardGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestDataStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Reporte final
    print("\n" + "="*70)
    print("📊 REPORTE FINAL")
    print("="*70)
    print(f"Tests ejecutados: {resultado.testsRun}")
    print(f"✅ Exitosos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"❌ Fallidos: {len(resultado.failures)}")
    print(f"💥 Errores: {len(resultado.errors)}")
    
    if resultado.wasSuccessful():
        print("\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON - Revisar arriba para detalles")
    
    print("="*70 + "\n")
    
    return resultado.wasSuccessful()


if __name__ == "__main__":
    # Ejecutar todos los tests
    exito = run_all_tests()
    
    # Código de salida para CI/CD
    exit(0 if exito else 1)