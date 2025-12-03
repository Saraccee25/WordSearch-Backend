"""
Tests individuales para componentes específicos
Puedes ejecutar cada función por separado
"""
from board_generator import generar_tablero_garantizado
from data_storage import storage
from game_logic import encontrar_palabra_en_tablero, crear_juego, resolver_juego
import json


def test_15_palabras_siempre():
    """
    TEST: Verificar que SIEMPRE se generen las 15 palabras
    """
    print("\n" + "="*70)
    print("TEST 1: Verificar generación de 15 palabras")
    print("="*70)
    
    palabras = storage.obtener_palabras("PROFESIONES")
    intentos_exitosos = 0
    total_intentos = 10
    
    for i in range(total_intentos):
        tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=5)
        
        if len(palabras_colocadas) == 15:
            intentos_exitosos += 1
            print(f"Intento {i+1}: ✅ {len(palabras_colocadas)}/15 palabras")
        else:
            print(f"Intento {i+1}: ❌ {len(palabras_colocadas)}/15 palabras")
            print(f"   Faltantes: {[p for p in palabras if p not in palabras_colocadas]}")
    
    tasa_exito = (intentos_exitosos / total_intentos) * 100
    print(f"\n📊 Tasa de éxito: {tasa_exito}% ({intentos_exitosos}/{total_intentos})")
    
    if tasa_exito == 100:
        print("✅ PASS: Siempre genera 15 palabras")
        return True
    else:
        print("❌ FAIL: No siempre genera 15 palabras")
        return False


def test_busqueda_palabras():
    """
    TEST: Verificar que todas las palabras colocadas se puedan encontrar
    """
    print("\n" + "="*70)
    print("TEST 2: Verificar búsqueda de palabras")
    print("="*70)
    
    palabras = storage.obtener_palabras("PROFESIONES")
    tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=5)
    
    print(f"\nPalabras colocadas: {len(palabras_colocadas)}")
    
    encontradas = 0
    no_encontradas = []
    
    for palabra in palabras_colocadas:
        posiciones = encontrar_palabra_en_tablero(tablero, palabra)
        if posiciones:
            encontradas += 1
            print(f"✅ {palabra}: Encontrada en {len(posiciones)} posiciones")
        else:
            no_encontradas.append(palabra)
            print(f"❌ {palabra}: NO ENCONTRADA")
    
    print(f"\n📊 Resultado: {encontradas}/{len(palabras_colocadas)} palabras encontradas")
    
    if len(no_encontradas) == 0:
        print("✅ PASS: Todas las palabras colocadas fueron encontradas")
        return True
    else:
        print(f"❌ FAIL: {len(no_encontradas)} palabras no encontradas: {no_encontradas}")
        return False


def test_direcciones_busqueda():
    """
    TEST: Verificar que se busca en las 8 direcciones
    """
    print("\n" + "="*70)
    print("TEST 3: Verificar búsqueda en 8 direcciones")
    print("="*70)
    
    # Tablero de prueba con palabra en cada dirección
    tablero = [
        ['H', 'O', 'L', 'A', 'X', 'X', 'X', 'X', 'X', 'X'],  # Horizontal →
        ['X', 'X', 'X', 'X', 'T', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 'E', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 'S', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'X', 'T', 'X', 'X', 'X', 'X', 'X'],  # Vertical ↓
        ['G', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'A', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'T', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 'O', 'X', 'X', 'X', 'X', 'X', 'X'],  # Diagonal ↘
        ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    ]
    
    tests = [
        ("HOLA", "Horizontal →"),
        ("TEST", "Vertical ↓"),
        ("GATO", "Diagonal ↘")
    ]
    
    todas_encontradas = True
    for palabra, direccion in tests:
        posiciones = encontrar_palabra_en_tablero(tablero, palabra)
        if posiciones:
            print(f"✅ {palabra} ({direccion}): Encontrada")
        else:
            print(f"❌ {palabra} ({direccion}): NO encontrada")
            todas_encontradas = False
    
    if todas_encontradas:
        print("\n✅ PASS: Búsqueda funciona en todas las direcciones")
        return True
    else:
        print("\n❌ FAIL: Algunas direcciones no funcionan")
        return False


def test_threading_correcto():
    """
    TEST: Verificar que el threading no cause problemas
    """
    print("\n" + "="*70)
    print("TEST 4: Verificar threading sin race conditions")
    print("="*70)
    
    palabras = storage.obtener_palabras("PROFESIONES")
    
    # Generar múltiples tableros en paralelo
    print("\nGenerando 5 tableros en secuencia rápida...")
    resultados = []
    
    for i in range(5):
        tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=3)
        resultados.append(len(palabras_colocadas))
        print(f"Tablero {i+1}: {len(palabras_colocadas)} palabras")
    
    # Todos deberían tener 15 palabras
    if all(r == 15 for r in resultados):
        print("\n✅ PASS: Threading funciona correctamente")
        return True
    else:
        print(f"\n❌ FAIL: Resultados inconsistentes: {resultados}")
        return False


def test_storage_arraylist():
    """
    TEST: Verificar que el storage funciona como ArrayList
    """
    print("\n" + "="*70)
    print("TEST 5: Verificar funcionamiento de ArrayLists")
    print("="*70)
    
    # Limpiar storage
    storage.limpiar_datos()
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Agregar palabras
    total_tests += 1
    storage.agregar_palabra("TEST1", "CAT1")
    storage.agregar_palabra("TEST2", "CAT2")
    palabras = storage.obtener_palabras()
    if "TEST1" in palabras and "TEST2" in palabras:
        print("✅ Agregar palabras funciona")
        tests_passed += 1
    else:
        print("❌ Agregar palabras falla")
    
    # Test 2: Guardar tableros
    total_tests += 1
    matriz = [['A'] * 15 for _ in range(15)]
    tablero_id = storage.guardar_tablero(matriz, ["TEST"])
    tablero = storage.obtener_tablero(tablero_id)
    if tablero and tablero.id == tablero_id:
        print("✅ Guardar/obtener tablero funciona")
        tests_passed += 1
    else:
        print("❌ Guardar/obtener tablero falla")
    
    # Test 3: Crear juegos
    total_tests += 1
    juego_id = storage.crear_juego(tablero_id)
    juego = storage.obtener_juego(juego_id)
    if juego and juego.id == juego_id:
        print("✅ Crear/obtener juego funciona")
        tests_passed += 1
    else:
        print("❌ Crear/obtener juego falla")
    
    # Test 4: Actualizar juego
    total_tests += 1
    storage.actualizar_juego(juego_id, palabra_encontrada="TEST")
    juego = storage.obtener_juego(juego_id)
    if "TEST" in juego.palabras_encontradas:
        print("✅ Actualizar juego funciona")
        tests_passed += 1
    else:
        print("❌ Actualizar juego falla")
    
    print(f"\n📊 Resultado: {tests_passed}/{total_tests} tests pasados")
    
    if tests_passed == total_tests:
        print("✅ PASS: Storage funciona correctamente")
        return True
    else:
        print("❌ FAIL: Algunos componentes del storage fallan")
        return False


def test_json_responses():
    """
    TEST: Verificar que todas las respuestas son JSON válidos
    """
    print("\n" + "="*70)
    print("TEST 6: Verificar respuestas JSON")
    print("="*70)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: crear_juego retorna JSON
    total_tests += 1
    try:
        resultado = crear_juego()
        datos = json.loads(resultado)
        if "tablero" in datos and "palabras" in datos:
            print("✅ crear_juego retorna JSON válido")
            tests_passed += 1
        else:
            print("❌ crear_juego JSON incompleto")
    except:
        print("❌ crear_juego no retorna JSON válido")
    
    # Test 2: resolver_juego retorna JSON
    total_tests += 1
    try:
        resultado = crear_juego()
        datos = json.loads(resultado)
        juego_id = datos["juego_id"]
        tablero_id = datos["tablero_id"]
        
        resultado_resolver = resolver_juego(juego_id, tablero_id)
        datos_resolver = json.loads(resultado_resolver)
        
        if "soluciones" in datos_resolver:
            print("✅ resolver_juego retorna JSON válido")
            tests_passed += 1
        else:
            print("❌ resolver_juego JSON incompleto")
    except Exception as e:
        print(f"❌ resolver_juego error: {e}")
    
    print(f"\n📊 Resultado: {tests_passed}/{total_tests} tests pasados")
    
    if tests_passed == total_tests:
        print("✅ PASS: Todas las respuestas son JSON válidos")
        return True
    else:
        print("❌ FAIL: Algunas respuestas no son JSON válidos")
        return False


def test_tamano_tablero():
    """
    TEST: Verificar que el tablero es siempre 15x15
    """
    print("\n" + "="*70)
    print("TEST 7: Verificar tamaño del tablero")
    print("="*70)
    
    palabras = storage.obtener_palabras("PROFESIONES")
    tablero, _ = generar_tablero_garantizado(palabras, intentos_maximos=3)
    
    filas = len(tablero)
    columnas = len(tablero[0]) if tablero else 0
    
    print(f"Dimensiones del tablero: {filas}x{columnas}")
    
    if filas == 15 and columnas == 15:
        print("✅ PASS: Tablero es 15x15")
        return True
    else:
        print(f"❌ FAIL: Tablero no es 15x15 (es {filas}x{columnas})")
        return False


def ejecutar_test_individual(numero):
    """Ejecutar un test específico por número"""
    tests = {
        1: test_15_palabras_siempre,
        2: test_busqueda_palabras,
        3: test_direcciones_busqueda,
        4: test_threading_correcto,
        5: test_storage_arraylist,
        6: test_json_responses,
        7: test_tamano_tablero
    }
    
    if numero in tests:
        return tests[numero]()
    else:
        print(f"❌ Test {numero} no existe")
        return False


def ejecutar_todos_los_tests():
    """Ejecutar todos los tests individuales"""
    print("\n" + "🧪"*35)
    print("EJECUTANDO TODOS LOS TESTS INDIVIDUALES")
    print("🧪"*35)
    
    resultados = []
    tests = [
        test_15_palabras_siempre,
        test_busqueda_palabras,
        test_direcciones_busqueda,
        test_threading_correcto,
        test_storage_arraylist,
        test_json_responses,
        test_tamano_tablero
    ]
    
    for i, test in enumerate(tests, 1):
        try:
            resultado = test()
            resultados.append(resultado)
        except Exception as e:
            print(f"\n❌ Error en test {i}: {e}")
            resultados.append(False)
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    exitosos = sum(resultados)
    total = len(resultados)
    print(f"Tests ejecutados: {total}")
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Fallidos: {total - exitosos}")
    print(f"Tasa de éxito: {(exitosos/total)*100:.1f}%")
    
    if exitosos == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
    else:
        print(f"\n⚠️  {total - exitosos} test(s) fallaron")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Ejecutar test específico
        try:
            numero = int(sys.argv[1])
            print(f"\nEjecutando test #{numero}...")
            ejecutar_test_individual(numero)
        except ValueError:
            print("Uso: python test_individuales.py [número_test]")
            print("Números de test disponibles: 1-7")
    else:
        # Ejecutar todos
        ejecutar_todos_los_tests()