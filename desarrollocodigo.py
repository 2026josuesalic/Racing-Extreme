import pygame 
import random 
import json 
import os 

pygame.init() 

ANCHO = 1000 

ALTO = 650 

FPS = 60 

PANTALLA = pygame.display.set_mode((ANCHO, ALTO)) 

pygame.display.set_caption("Moto Racing Extreme") 

RELOJ = pygame.time.Clock() 

FUENTE = pygame.font.Font(None, 30) 

FUENTE_MEDIANA = pygame.font.Font(None, 42) 

FUENTE_GRANDE = pygame.font.Font(None, 70) 

ARCHIVO_GUARDADO = "moto_racing_save.json" 

NEGRO = (15, 15, 20) 

BLANCO = (245, 245, 245) 

GRIS = (100, 100, 110) 

GRIS_OSCURO = (45, 45, 50) 

VERDE = (40, 210, 90) 

ROJO = (220, 55, 55) 

AZUL = (50, 120, 230) 

AMARILLO = (240, 210, 50) 

NARANJA = (240, 130, 40) 

CELESTE = (70, 190, 230) 

MORADO = (150, 70, 220) 

  

MOTOS = { 

    "Inicial": {"velocidad": 7, "aceleracion": 0.12, "manejo": 5, 

                "precio": 0, "color": (40, 120, 230)}, 

    "Rayo": {"velocidad": 9, "aceleracion": 0.15, "manejo": 5, 

             "precio": 500, "color": (230, 60, 50)}, 

    "Furia": {"velocidad": 11, "aceleracion": 0.18, "manejo": 6, 

              "precio": 1000, "color": (240, 150, 30)}, 

    "Extrema": {"velocidad": 13, "aceleracion": 0.22, "manejo": 7, 

                "precio": 2000, "color": (170, 60, 220)} 

} 

  

def cargar_partida(): 

    datos = { 

        "nivel": 1, "monedas": 500, "moto_actual": "Inicial", 

        "motos_desbloqueadas": ["Inicial"], 

        "mejoras": {"velocidad": 0, "aceleracion": 0, "manejo": 0}, 

        "record": 0, "carreras": 0, "logros": [] 

    } 

    if os.path.exists(ARCHIVO_GUARDADO): 

        try: 

            with open(ARCHIVO_GUARDADO, "r", encoding="utf-8") as f: 

                guardado = json.load(f) 

            datos.update(guardado) 

        except Exception: 

            pass 

    return datos 

  

def guardar_partida(datos): 

    with open(ARCHIVO_GUARDADO, "w", encoding="utf-8") as f: 

        json.dump(datos, f, indent=4) 

  

datos = cargar_partida() 

  

def texto(superficie, contenido, fuente, color, x, y, centrado=False): 

    imagen = fuente.render(str(contenido), True, color) 

    rect = imagen.get_rect(center=(x, y) if centrado else (x + imagen.get_width()/2, y)) 

    if not centrado: 

        rect.topleft = (x, y) 

    superficie.blit(imagen, rect) 

  

def boton(superficie, rect, contenido, color=AZUL): 

    pygame.draw.rect(superficie, color, rect, border_radius=12) 

    pygame.draw.rect(superficie, BLANCO, rect, 2, border_radius=12) 

    texto(superficie, contenido, FUENTE, BLANCO, rect.centerx, rect.centery, True) 

  

def dibujar_moto(superficie, x, y, color, escala=1): 

    ancho = int(28 * escala) 

    alto = int(55 * escala) 

    pygame.draw.ellipse(superficie, NEGRO, 

                        (x-ancho//2, y-alto//2, ancho, int(18*escala))) 

    pygame.draw.ellipse(superficie, NEGRO, 

                        (x-ancho//2, y+alto//3, ancho, int(18*escala))) 

    pygame.draw.polygon(superficie, color, [ 

        (x, y-alto//2), (x+ancho//2, y), 

        (x+ancho//3, y+alto//2), 

        (x-ancho//3, y+alto//2), (x-ancho//2, y) 

    ]) 

    pygame.draw.circle(superficie, (220,180,140), 

                       (x, y-int(10*escala)), max(4,int(6*escala))) 

  

def menu_principal(): 

    opciones = ["NUEVO JUEGO","CONTINUAR","GARAJE","TIENDA","CONFIGURACION","SALIR"] 

    seleccion = 0 

    while True: 

        PANTALLA.fill(GRIS_OSCURO) 

        pygame.draw.rect(PANTALLA,(50,50,55),(300,0,400,ALTO)) 

        for y in range(-50,ALTO,80): 

            pygame.draw.rect(PANTALLA,BLANCO,(495,y,10,45)) 

        texto(PANTALLA,"MOTO RACING",FUENTE_GRANDE,AMARILLO,ANCHO//2,80,True) 

        texto(PANTALLA,"EXTREME",FUENTE_GRANDE,ROJO,ANCHO//2,140,True) 

        for i,opcion in enumerate(opciones): 

            boton(PANTALLA,pygame.Rect(350,220+i*60,300,48),opcion, 

                  AZUL if i==seleccion else GRIS_OSCURO) 

        texto(PANTALLA,f"Monedas: {datos['monedas']}   Nivel: {datos['nivel']}", 

              FUENTE,BLANCO,20,20) 

        pygame.display.flip() 

        for evento in pygame.event.get(): 

            if evento.type == pygame.QUIT: 

                guardar_partida(datos); pygame.quit(); raise SystemExit 

            if evento.type == pygame.KEYDOWN: 

                if evento.key == pygame.K_UP: seleccion=(seleccion-1)%len(opciones) 

                elif evento.key == pygame.K_DOWN: seleccion=(seleccion+1)%len(opciones) 

                elif evento.key == pygame.K_RETURN: 

                    if seleccion in (0,1): configuracion_carrera() 

                    elif seleccion==2: garage() 

                    elif seleccion==3: tienda() 

                    elif seleccion==4: configuracion() 

                    elif seleccion==5: 

                        guardar_partida(datos); pygame.quit(); raise SystemExit 

  

def garage(): 

    motos=list(MOTOS.keys()) 

    seleccion=motos.index(datos["moto_actual"]) 

    while True: 

        PANTALLA.fill((25,25,35)) 

        texto(PANTALLA,"GARAJE",FUENTE_GRANDE,AMARILLO,ANCHO//2,60,True) 

        moto=motos[seleccion]; info=MOTOS[moto] 

        dibujar_moto(PANTALLA,500,230,info["color"],3) 

        texto(PANTALLA,moto,FUENTE_MEDIANA,BLANCO,500,340,True) 

        texto(PANTALLA,f"Velocidad: {info['velocidad']+datos['mejoras']['velocidad']}", 

              FUENTE,BLANCO,390,400) 

        texto(PANTALLA,f"Aceleracion: {info['aceleracion']+datos['mejoras']['aceleracion']:.2f}", 

              FUENTE,BLANCO,390,435) 

        texto(PANTALLA,f"Manejo: {info['manejo']+datos['mejoras']['manejo']}", 

              FUENTE,BLANCO,390,470) 

        texto(PANTALLA,"← → Seleccionar   ENTER Elegir   ESC Volver", 

              FUENTE,GRIS,ANCHO//2,580,True) 

        pygame.display.flip() 

        for evento in pygame.event.get(): 

            if evento.type==pygame.QUIT: 

                guardar_partida(datos); pygame.quit(); raise SystemExit 

            if evento.type==pygame.KEYDOWN: 

                if evento.key==pygame.K_LEFT: seleccion=(seleccion-1)%len(motos) 

                elif evento.key==pygame.K_RIGHT: seleccion=(seleccion+1)%len(motos) 

                elif evento.key==pygame.K_RETURN and moto in datos["motos_desbloqueadas"]: 

                    datos["moto_actual"]=moto; guardar_partida(datos) 

                elif evento.key==pygame.K_ESCAPE: return 

  

def tienda(): 

    seleccion=0 

    opciones=["Mejorar velocidad - 300","Mejorar aceleracion - 300","Mejorar manejo - 300"] 

    while True: 

        PANTALLA.fill((25,25,35)) 

        texto(PANTALLA,"TIENDA",FUENTE_GRANDE,AMARILLO,ANCHO//2,60,True) 

        texto(PANTALLA,f"Monedas disponibles: {datos['monedas']}", 

              FUENTE_MEDIANA,VERDE,ANCHO//2,130,True) 

        for i,opcion in enumerate(opciones): 

            boton(PANTALLA,pygame.Rect(300,220+i*75,400,55),opcion, 

                  AZUL if i==seleccion else GRIS_OSCURO) 

        texto(PANTALLA,"ESC - Volver",FUENTE,GRIS,ANCHO//2,500,True) 

        pygame.display.flip() 

        for evento in pygame.event.get(): 

            if evento.type==pygame.QUIT: 

                guardar_partida(datos); pygame.quit(); raise SystemExit 

            if evento.type==pygame.KEYDOWN: 

                if evento.key==pygame.K_UP: seleccion=(seleccion-1)%3 

                elif evento.key==pygame.K_DOWN: seleccion=(seleccion+1)%3 

                elif evento.key==pygame.K_RETURN and datos["monedas"]>=300: 

                    datos["monedas"]-=300 

                    if seleccion==0: datos["mejoras"]["velocidad"]+=1 

                    elif seleccion==1: datos["mejoras"]["aceleracion"]+=0.02 

                    else: datos["mejoras"]["manejo"]+=1 

                    guardar_partida(datos) 

                elif evento.key==pygame.K_ESCAPE: return 

  

def configuracion(): 

    while True: 

        PANTALLA.fill((25,25,35)) 

        texto(PANTALLA,"CONFIGURACION",FUENTE_GRANDE,AMARILLO,ANCHO//2,100,True) 

        lineas=["Controles:","Flecha izquierda / derecha = mover", 

                "ESPACIO = turbo","ESC = salir de menus","ENTER = seleccionar"] 

        for i,linea in enumerate(lineas): 

            texto(PANTALLA,linea,FUENTE_MEDIANA if i==0 else FUENTE, 

                  BLANCO,200,230+i*45) 

        texto(PANTALLA,"Presiona ESC para volver",FUENTE,GRIS,ANCHO//2,550,True) 

        pygame.display.flip() 

        for evento in pygame.event.get(): 

            if evento.type==pygame.QUIT: 

                guardar_partida(datos); pygame.quit(); raise SystemExit 

            if evento.type==pygame.KEYDOWN and evento.key==pygame.K_ESCAPE: return 

  

def configuracion_carrera(): 

    modos=["Carrera","Contrarreloj","Supervivencia"] 

    climas=["Dia","Noche","Lluvia"] 

    modo=clima=0 

    while True: 

        PANTALLA.fill((25,25,35)) 

        texto(PANTALLA,"CONFIGURAR CARRERA",FUENTE_GRANDE,AMARILLO,ANCHO//2,70,True) 

        texto(PANTALLA,f"Modo: {modos[modo]}",FUENTE_MEDIANA,BLANCO,ANCHO//2,200,True) 

        texto(PANTALLA,f"Clima: {climas[clima]}",FUENTE_MEDIANA,BLANCO,ANCHO//2,270,True) 

        texto(PANTALLA,f"Nivel: {datos['nivel']}",FUENTE_MEDIANA,BLANCO,ANCHO//2,340,True) 

        boton(PANTALLA,pygame.Rect(350,420,300,60),"INICIAR CARRERA",VERDE) 

        texto(PANTALLA,"M = modo | C = clima | ENTER = iniciar | ESC = volver", 

              FUENTE,GRIS,ANCHO//2,530,True) 

        pygame.display.flip() 

        for evento in pygame.event.get(): 

            if evento.type==pygame.QUIT: 

                guardar_partida(datos); pygame.quit(); raise SystemExit 

            if evento.type==pygame.KEYDOWN: 

                if evento.key==pygame.K_m: modo=(modo+1)%len(modos)