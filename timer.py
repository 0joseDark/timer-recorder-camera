import cv2
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

def detectar_camera():
    for i in range(10):  # Verifica até 10 portas USB
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return i
    return None

def criar_pastas():
    os.makedirs("imagens", exist_ok=True)
    os.makedirs("videos", exist_ok=True)

def calcular_tempo():
    try:
        semanas = int(entrada_semanas.get()) * 604800
        dias = int(entrada_dias.get()) * 86400
        horas = int(entrada_horas.get()) * 3600
        minutos = int(entrada_minutos.get()) * 60
        segundos = int(entrada_segundos.get())
        decimos = int(entrada_decimos.get()) * 0.1
        return semanas + dias + horas + minutos + segundos + decimos
    except ValueError:
        messagebox.showerror("Erro", "Introduza valores numéricos válidos.")
        return None

def gravar_video():
    tempo_gravacao = calcular_tempo()
    if tempo_gravacao is None:
        return
    
    camera_porta = detectar_camera()
    if camera_porta is None:
        messagebox.showerror("Erro", "Nenhuma câmara encontrada.")
        return
    
    cap = cv2.VideoCapture(camera_porta)
    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20  # Ajustável
    caminho_video = os.path.join("videos", entrada_nome.get() + ".mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(caminho_video, fourcc, fps, (largura, altura))
    
    inicio = time.time()
    while (time.time() - inicio) < tempo_gravacao:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        caminho_frame = os.path.join("imagens", f"frame_{int(time.time())}.jpg")
        cv2.imwrite(caminho_frame, frame)
    
    cap.release()
    out.release()
    messagebox.showinfo("Info", f"Vídeo guardado em {caminho_video}")

def iniciar_gravacao():
    Thread(target=gravar_video, daemon=True).start()

# Interface Gráfica
root = tk.Tk()
root.title("Gravador de Câmara USB")

criar_pastas()

tk.Label(root, text="Nome do Ficheiro:").grid(row=0, column=0)
entrada_nome = tk.Entry(root)
entrada_nome.grid(row=0, column=1)

campos = ["Semanas", "Dias", "Horas", "Minutos", "Segundos", "Décimos"]
entradas = []
for i, campo in enumerate(campos):
    tk.Label(root, text=campo + ":").grid(row=i+1, column=0)
    entrada = tk.Entry(root, width=5)
    entrada.grid(row=i+1, column=1)
    entrada.insert(0, "0")
    entradas.append(entrada)

entrada_semanas, entrada_dias, entrada_horas, entrada_minutos, entrada_segundos, entrada_decimos = entradas

botao_gravar = tk.Button(root, text="Iniciar Gravação", command=iniciar_gravacao)
botao_gravar.grid(row=7, column=0, columnspan=2)

root.mainloop()
