# kon

¡Bienvenido a **Kon**, tu nuevo shooter espacial en Python!

---

## 📝 Descripción

**Kon** es un juego arcade de disparos en 2D desarrollado con **Pygame**. Controlas una nave espacial con dos alas, disparas láseres contra oleadas de enemigos y avanzas de nivel cada vez que alcanzas los puntos necesarios. El juego cuenta con:

* **Menú principal** con opciones de inicio, tutorial y salida
* **Tutorial** rápido sobre controles y objetivos
* **Mecánica de dos láseres** saliendo de cada ala de la nave
* **Sistema de niveles**: cada 200 × *nivel* puntos subes de fase
* **Enemigos variados** y explosiones gráficas al impactar
* **Contador de puntos** y pantalla de Game Over

---

## 🚀 Instalación

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/tuUsuario/kon.git
   cd kon
   ```

2. **Crea y activa un entorno virtual** (recomendado)

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

   > Si no existe `requirements.txt`, simplemente:
   
   ```bash
    ```

   pip install pygame

   ```
   ```

---

## ▶️ Cómo ejecutar

Con el entorno activado y en la carpeta del proyecto:

```bash
python main.py
```

> Asegúrate de que las imágenes (`.png`) y los sonidos (`.mp3`, `.wav`) estén en la misma carpeta que `main.py`.

---

## 📦 Dependencias

* **Python** ≥ 3.8
* **Pygame**

  ```bash
  pip install pygame
  ```

---

## 🎮 Controles

* **←** / **→** : Mover la nave
* **Espacio** : Disparar **dos** láseres (¡uno por cada ala!)
* **ENTER** :

  * En menú → Iniciar partida
  * En tutorial → Volver a menú
  * En Game Over → Reiniciar
* **T** : Abrir tutorial desde el menú
* **ESC** : Salir del juego

---

## ⚙️ Dinámica del juego

1. Al iniciar, verás el **menú principal**.
2. Selecciona **ENTER** para comenzar o **T** para ver el tutorial.
3. En pantalla de juego:

   * Enemigos aparecen en intervalos variables según tu nivel.
   * Cada golpe con un láser otorga **10 puntos**.
   * Al llegar a **200 × *nivel*** puntos subes de fase y los enemigos ganan variedad y velocidad.
4. Si un enemigo choca contra tu nave → **Game Over**.
5. En pantalla de Game Over, presiona **ENTER** para reiniciar o **ESC** para salir.

---

## 🛠 Desarrollado con

* **IDE**: PyCharm
* **Lenguaje**: Python 3.x
* **Motor gráfico**: Pygame

---

¡Disfruta pilotando tu nave y defendiendo el espacio en **Kon**! 🌌✨

> **Tip**: Ajusta tus imágenes y efectos de sonido en la misma carpeta que `main.py` para evitar errores de carga.
