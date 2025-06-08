# API REST para generación de texto con distilgpt2 en Google Colab

Este proyecto implementa una API REST con Flask que genera texto usando el modelo distilgpt2 de Hugging Face. Está diseñado para ejecutarse en Google Colab, utiliza ngrok para exponer la API públicamente y pytest para pruebas automatizadas. Sigue buenas prácticas con logging, validación de entradas y manejo de errores.

## Características

- **Endpoint `/generate`:** Genera texto a partir de un prompt (POST).
- **Endpoint `/health`:** Verifica el estado del servidor (GET).
- **Modelo:** distilgpt2, ligero y adecuado para Colab.
- **Pruebas:** Pruebas unitarias con pytest para casos exitosos y de error.
- **Entorno:** Google Colab con tunneling via ngrok.

## Requisitos

- Python 3.8+
- Google Colab (gratuito o Pro)
- Cuenta gratuita de ngrok con authtoken (regístrate en el sitio web de ngrok)
- **Dependencias:**
  - flask==2.0.1
  - transformers==4.40.0
  - pytest==7.4.0
  - pyngrok

## Instalación

1. **Abrir Google Colab:**
   - Ve al sitio web de Colab y crea un nuevo notebook.
2. **Instalar dependencias:**
   - Instala las dependencias necesarias ejecutando un comando en una celda de Colab.
3. **Configurar ngrok:**
   - Regístrate en el sitio web de ngrok para obtener una cuenta gratuita.
   - Obtén tu authtoken desde el panel de ngrok.
   - Configura el authtoken en tu código.
4. **Guardar archivos:**
   - Crea los archivos `main.py`, `test_api.py`, `requirements.txt` y `run_tests.sh` en Colab usando celdas específicas para cada uno.
5. **Ejecutar la instalación:**
   - Instala las dependencias desde el archivo `requirements.txt`.

## Uso

- **Iniciar el servidor Flask y el túnel ngrok:**
  - Ejecuta un script en Colab que inicia el servidor Flask en un hilo, verifica su estado y crea un túnel ngrok con tu authtoken.
  - Obtendrás una URL pública de ngrok (e.g., `https://<random>.ngrok-free.app`).
- **Probar la API en vivo:**
  - Usa la URL de ngrok para enviar solicitudes POST al endpoint `/generate` con un prompt y max_length.
  - Prueba interactivamente ingresando prompts en un bucle y visualizando los resultados en tiempo real.
- **Probar con cURL:**
  - Envía solicitudes POST desde Colab usando cURL con la URL de ngrok.
- **Ejecutar pruebas automatizadas:**
  - Corre el script `run_tests.sh` para ejecutar las pruebas unitarias con pytest.

## Solución de problemas

- **Límite de túneles ngrok (ERR_NGROK_324):**
  - Termina procesos ngrok previos con un comando en Colab.
  - Revisa túneles activos en el panel de ngrok y ciérralos.
  - Reinicia el runtime de Colab desde el menú.
- **Servidor Flask no inicia:**
  - Verifica conflictos de puerto con comandos para listar y terminar procesos.
  - Habilita el modo debug temporalmente en `main.py` para logs, luego desactívalo.
- **JSONDecodeError o 502:**
  - Prueba el endpoint `/health` en un navegador con la URL de ngrok.
  - Asegúrate de que el servidor Flask esté activo.
- **Memoria:**
  - Si distilgpt2 no carga, reinicia el runtime o considera Colab Pro para más RAM.

## Ejemplo de salida

![image](https://github.com/user-attachments/assets/41b97883-56a4-48a6-84e7-4d113da447b1)
