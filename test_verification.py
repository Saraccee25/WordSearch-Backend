"""
Script para verificar que el juego funcione correctamente
"""
from board_generator import generar_tablero_garantizado
from data_storage import storage
from game_logic import encontrar_palabra_en_tablero

def test_generacion_y_busqueda():
    """Prueba que todas las palabras se coloquen y encuentren"""
    
    print("\n" + "="*70)
    print("🧪 TEST DE VERIFICACIÓN - SOPA DE LETRAS")
    print("="*70)
    
    palabras = storage.obtener_palabras("PROFESIONES")
    print(f"\n📋 Palabras a colocar: {len(palabras)}")
    print(f"   {palabras}\n")
    
    # Hacer 5 pruebas
    for intento in range(1, 6):
        print(f"\n{'─'*70}")
        print(f"🎲 INTENTO {intento}/5")
        print(f"{'─'*70}")
        
        # Generar tablero
        tablero, palabras_colocadas = generar_tablero_garantizado(palabras, intentos_maximos=10)
        
        print(f"\n📊 Resultado de generación:")
        print(f"   ✓ Palabras colocadas: {len(palabras_colocadas)}/{len(palabras)}")
        
        if len(palabras_colocadas) < len(palabras):
            faltantes = [p for p in palabras if p not in palabras_colocadas]
            print(f"   ❌ Palabras que NO se colocaron: {faltantes}")
        
        # Ahora buscar cada palabra colocada
        print(f"\n🔍 Verificando búsqueda de palabras:")
        palabras_encontradas = []
        palabras_no_encontradas = []
        
        for palabra in palabras_colocadas:
            posiciones = encontrar_palabra_en_tablero(tablero, palabra)
            if posiciones:
                palabras_encontradas.append(palabra)
                print(f"   ✓ {palabra}: Encontrada")
            else:
                palabras_no_encontradas.append(palabra)
                print(f"   ❌ {palabra}: NO ENCONTRADA (ERROR GRAVE)")
        
        print(f"\n📈 Resumen intento {intento}:")
        print(f"   Colocadas: {len(palabras_colocadas)}/{len(palabras)}")
        print(f"   Encontradas: {len(palabras_encontradas)}/{len(palabras_colocadas)}")
        
        if len(palabras_no_encontradas) > 0:
            print(f"   ⚠️  PROBLEMA: {len(palabras_no_encontradas)} palabras colocadas pero no encontradas")
            print(f"      {palabras_no_encontradas}")
            
            # Mostrar tablero para debug
            print("\n📋 Tablero generado:")
            for fila in tablero:
                print("   " + " ".join(fila))
        
        if len(palabras_colocadas) == len(palabras) and len(palabras_encontradas) == len(palabras_colocadas):
            print(f"   ✅ ¡PERFECTO! Todo funciona correctamente")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETADO")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_generacion_y_busqueda()