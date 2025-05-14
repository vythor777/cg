import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math

class TransformadorPoligono:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title("Transformador de Polígonos")
        
        # Configurações iniciais do polígono
        self.num_lados = 3
        self.fator_escala = 1.0
        self.angulo_rotacao = 0
        self.deslocamento_x = 0
        self.deslocamento_y = 0
        self.cisalhamento_x = 0
        self.cisalhamento_y = 0
        
        # Configuração da área de visualização
        self.configurar_area_grafica()
        
        # Configuração dos controles da interface
        self.configurar_controles()
        
        # Inicializar o polígono
        self.var_lados.trace("w", self.atualizar_lados)
        self.desenhar_poligono()
    
    def configurar_area_grafica(self):
        """Configura a área gráfica para exibição do polígono"""
        self.figura = Figure(figsize=(6, 6))
        self.grafico = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.janela_principal)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=10)
    
    def configurar_controles(self):
        """Configura os controles da interface do usuário"""
        painel_controles = ttk.Frame(self.janela_principal)
        painel_controles.grid(row=0, column=0, sticky="n", padx=10)
        
        # Controle do número de lados
        ttk.Label(painel_controles, text="Número de lados:").pack()
        self.var_lados = tk.StringVar(value="3")
        ttk.Entry(painel_controles, textvariable=self.var_lados).pack()
        
        # Controles de translação
        ttk.Label(painel_controles, text="\nTranslação").pack()
        ttk.Button(painel_controles, text="↑", command=lambda: self.transladar(0, 0.1)).pack()
        ttk.Button(painel_controles, text="↓", command=lambda: self.transladar(0, -0.1)).pack()
        ttk.Button(painel_controles, text="←", command=lambda: self.transladar(-0.1, 0)).pack()
        ttk.Button(painel_controles, text="→", command=lambda: self.transladar(0.1, 0)).pack()
        
        # Controles de rotação
        ttk.Label(painel_controles, text="\nRotação").pack()
        ttk.Button(painel_controles, text="Girar +", command=lambda: self.rotacionar(10)).pack()
        ttk.Button(painel_controles, text="Girar -", command=lambda: self.rotacionar(-10)).pack()
        
        # Controles de escala
        ttk.Label(painel_controles, text="\nEscala").pack()
        ttk.Button(painel_controles, text="Aumentar", command=lambda: self.escalar(1.1)).pack()
        ttk.Button(painel_controles, text="Diminuir", command=lambda: self.escalar(0.9)).pack()
        
        # Controles de cisalhamento
        ttk.Label(painel_controles, text="\nCisalhamento").pack()
        ttk.Button(painel_controles, text="X +", command=lambda: self.cisalhar(0.1, 0)).pack()
        ttk.Button(painel_controles, text="X -", command=lambda: self.cisalhar(-0.1, 0)).pack()
        ttk.Button(painel_controles, text="Y +", command=lambda: self.cisalhar(0, 0.1)).pack()
        ttk.Button(painel_controles, text="Y -", command=lambda: self.cisalhar(0, -0.1)).pack()
        
        # Botão para criar círculo
        ttk.Button(painel_controles, text="Criar Círculo (100 lados)", 
                  command=lambda: self.definir_lados(100)).pack(pady=10)
    
    def calcular_pontos_poligono(self):
        """Calcula os pontos do polígono regular com base no número de lados"""
        pontos = []
        raio = 1
        for i in range(self.num_lados):
            angulo = 2 * math.pi * i / self.num_lados  
            x = raio * math.cos(angulo)
            y = raio * math.sin(angulo)
            pontos.append([x, y, 1])  # Coordenadas homogêneas
        return np.array(pontos)
    
    def aplicar_transformacao(self, pontos):
        """Aplica as transformações geométricas aos pontos do polígono"""
        # Matriz de rotação 
        angulo_rad = math.radians(self.angulo_rotacao)
        cos_ang = math.cos(angulo_rad)
        sen_ang = math.sin(angulo_rad)
        matriz_rotacao = np.array([
            [cos_ang, -sen_ang, 0],
            [sen_ang, cos_ang, 0],
            [0, 0, 1]
        ])
        
        # Matriz de translação
        matriz_translacao = np.array([
            [1, 0, self.deslocamento_x],
            [0, 1, self.deslocamento_y],
            [0, 0, 1]
        ])
        
        # Matriz de escala
        matriz_escala = np.array([
            [self.fator_escala, 0, 0],
            [0, self.fator_escala, 0],
            [0, 0, 1]
        ])
        
        # Matriz de cisalhamento
        matriz_cisalhamento = np.array([
            [1, self.cisalhamento_x, 0],
            [self.cisalhamento_y, 1, 0],
            [0, 0, 1]
        ])
        
        # Aplicar transformações em sequência
        pontos_transformados = pontos.dot(matriz_rotacao.T).dot(matriz_escala.T).dot(matriz_cisalhamento.T).dot(matriz_translacao.T)
        return pontos_transformados
    
    def desenhar_poligono(self):
        """Desenha o polígono na área gráfica"""
        self.grafico.clear()
        
        # Calcula os pontos do polígono
        pontos = self.calcular_pontos_poligono()
        
        # Aplica as transformações
        pontos_transformados = self.aplicar_transformacao(pontos)
        
        # Extrair coordenadas x e y
        x = pontos_transformados[:, 0]
        y = pontos_transformados[:, 1]
        
        # Fechar o polígono conectando o último ponto ao primeiro
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        
        # Desenhar o polígono
        self.grafico.plot(x, y, 'b-')
        
        # Configurar visualização
        self.grafico.set_xlim(-3, 3)
        self.grafico.set_ylim(-3, 3)
        self.grafico.set_aspect('equal')
        self.grafico.grid(True)
        self.canvas.draw()
    
    def transladar(self, dx, dy):
        """Translada o polígono nas direções x e y"""
        self.deslocamento_x += dx
        self.deslocamento_y += dy
        self.desenhar_poligono()
    
    def rotacionar(self, angulo):
        """Rotaciona o polígono pelo ângulo especificado em graus"""
        self.angulo_rotacao += angulo
        self.desenhar_poligono()
    
    def escalar(self, fator):
        """Escala o polígono pelo fator especificado"""
        self.fator_escala *= fator
        self.desenhar_poligono()
    
    def cisalhar(self, sx, sy):
        """Aplica cisalhamento ao polígono nas direções x e y"""
        self.cisalhamento_x += sx
        self.cisalhamento_y += sy
        self.desenhar_poligono()
    
    def definir_lados(self, numero):
        """Define o número de lados do polígono"""
        self.var_lados.set(str(numero))
    
    def atualizar_lados(self, *args):
        """Atualiza o número de lados do polígono quando o valor é alterado"""
        try:
            novos_lados = int(self.var_lados.get())
            if novos_lados >= 3:
                self.num_lados = novos_lados
                self.desenhar_poligono()
        except ValueError:
            pass

if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = TransformadorPoligono(janela_principal)
    janela_principal.mainloop()
