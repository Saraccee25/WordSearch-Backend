from typing import List, Dict, Optional
from datetime import datetime
import json

class Palabra:
    """Representa una palabra del juego"""
    def __init__(self, texto: str, categoria: str = "PROFESIONES"):
        self.texto = texto.upper()
        self.categoria = categoria
    
    def to_dict(self):
        return {
            "texto": self.texto,
            "categoria": self.categoria
        }

class Tablero:
    """Representa un tablero generado"""
    def __init__(self, tablero_id: int, matriz: List[List[str]], palabras: List[str]):
        self.id = tablero_id
        self.matriz = matriz
        self.palabras = palabras
        self.fecha_creacion = datetime.now()
    
    def to_dict(self):
        return {
            "id": self.id,
            "matriz": self.matriz,
            "palabras": self.palabras,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

class Juego:
    """Representa una sesión de juego"""
    def __init__(self, juego_id: int, tablero_id: int):
        self.id = juego_id
        self.tablero_id = tablero_id
        self.tiempo_inicio = datetime.now()
        self.tiempo_fin = None
        self.palabras_encontradas = []  # ArrayList de palabras encontradas
        self.completado = False
    
    def agregar_palabra_encontrada(self, palabra: str):
        """Agrega una palabra a la lista de encontradas"""
        if palabra not in self.palabras_encontradas:
            self.palabras_encontradas.append(palabra)
    
    def finalizar(self):
        """Marca el juego como completado"""
        self.completado = True
        self.tiempo_fin = datetime.now()
    
    def get_tiempo_transcurrido(self):
        """Retorna el tiempo transcurrido en segundos"""
        if self.tiempo_fin:
            return (self.tiempo_fin - self.tiempo_inicio).total_seconds()
        return (datetime.now() - self.tiempo_inicio).total_seconds()
    
    def to_dict(self):
        return {
            "id": self.id,
            "tablero_id": self.tablero_id,
            "tiempo_inicio": self.tiempo_inicio.isoformat(),
            "tiempo_fin": self.tiempo_fin.isoformat() if self.tiempo_fin else None,
            "palabras_encontradas": self.palabras_encontradas,
            "completado": self.completado,
            "tiempo_transcurrido": self.get_tiempo_transcurrido()
        }

class DataStorage:
    """Simula una base de datos usando ArrayLists (listas de Python)"""
    
    def __init__(self):
       
        self.palabras: List[Palabra] = []
        self.tableros: List[Tablero] = []
        self.juegos: List[Juego] = []
        
       
        self._next_tablero_id = 1
        self._next_juego_id = 1
        
        
        self._inicializar_palabras()
    
    def _inicializar_palabras(self):
        """Inicializa el ArrayList de palabras"""
        palabras_default = [
            "TRADUCTOR", "CAMARERA", "EMPLEADO",
            "RELOJERO", "APICULTOR", "ATLETA",
            "ASTRONAUTA", "CONDUCTOR", "JOYERO",
            "CIRUJANO", "FOTOGRAFO", "MODISTA",
            "GEOLOGO", "JUEZ", "MODELO"
        ]
        
        for palabra_texto in palabras_default:
            palabra = Palabra(palabra_texto, "PROFESIONES")
            self.palabras.append(palabra)
    
    
    
    def agregar_palabra(self, texto: str, categoria: str = "PROFESIONES"):
        """Agrega una palabra al ArrayList"""
       
        if not any(p.texto == texto.upper() for p in self.palabras):
            palabra = Palabra(texto, categoria)
            self.palabras.append(palabra)
            return True
        return False
    
    def obtener_palabras(self, categoria: str = None) -> List[str]:
        """Obtiene palabras del ArrayList, opcionalmente filtradas por categoría"""
        if categoria:
            return [p.texto for p in self.palabras if p.categoria == categoria]
        return [p.texto for p in self.palabras]
    
    def buscar_palabra(self, texto: str) -> Optional[Palabra]:
        """Busca una palabra en el ArrayList"""
        for palabra in self.palabras:
            if palabra.texto == texto.upper():
                return palabra
        return None
    
   
    
    def guardar_tablero(self, matriz: List[List[str]], palabras: List[str]) -> int:
        """Guarda un tablero en el ArrayList y retorna su ID"""
        tablero = Tablero(self._next_tablero_id, matriz, palabras)
        self.tableros.append(tablero)
        self._next_tablero_id += 1
        return tablero.id
    
    def obtener_tablero(self, tablero_id: int) -> Optional[Tablero]:
        """Busca un tablero por ID en el ArrayList"""
        for tablero in self.tableros:
            if tablero.id == tablero_id:
                return tablero
        return None
    
    def listar_tableros(self) -> List[Tablero]:
        """Retorna todos los tableros del ArrayList"""
        return self.tableros
    
    
    
    def crear_juego(self, tablero_id: int) -> int:
        """Crea un nuevo juego en el ArrayList y retorna su ID"""
        juego = Juego(self._next_juego_id, tablero_id)
        self.juegos.append(juego)
        self._next_juego_id += 1
        return juego.id
    
    def obtener_juego(self, juego_id: int) -> Optional[Juego]:
        """Busca un juego por ID en el ArrayList"""
        for juego in self.juegos:
            if juego.id == juego_id:
                return juego
        return None
    
    def actualizar_juego(self, juego_id: int, palabra_encontrada: str = None, finalizar: bool = False):
        """Actualiza el estado de un juego"""
        juego = self.obtener_juego(juego_id)
        if juego:
            if palabra_encontrada:
                juego.agregar_palabra_encontrada(palabra_encontrada)
            if finalizar:
                juego.finalizar()
            return True
        return False
    
    def listar_juegos(self) -> List[Juego]:
        """Retorna todos los juegos del ArrayList"""
        return self.juegos
    
   
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del storage"""
        return {
            "total_palabras": len(self.palabras),
            "total_tableros": len(self.tableros),
            "total_juegos": len(self.juegos),
            "juegos_completados": sum(1 for j in self.juegos if j.completado)
        }
    
    def exportar_datos(self, archivo: str = "datos_juego.json"):
        """Exporta todos los datos a un archivo JSON"""
        datos = {
            "palabras": [p.to_dict() for p in self.palabras],
            "tableros": [t.to_dict() for t in self.tableros],
            "juegos": [j.to_dict() for j in self.juegos]
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Datos exportados a {archivo}")
    
    def limpiar_datos(self):
        """Limpia todos los ArrayLists (útil para testing)"""
        self.palabras.clear()
        self.tableros.clear()
        self.juegos.clear()
        self._next_tablero_id = 1
        self._next_juego_id = 1
        self._inicializar_palabras()



storage = DataStorage()