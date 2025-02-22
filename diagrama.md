```mermaid
graph TD
    A[Inicio] --> B[Interfaz de Streamlit]
    B --> C[Entrada del Usuario]
    C --> D{¿La pregunta es sobre saldos?}
    D -->|Sí| E[Extraer Nombre del Cliente]
    E --> F[Buscar Saldo en saldo.csv]
    F --> G{¿Encontró el saldo?}
    G -->|Sí| H[Devolver Saldo]
    G -->|No| I[Devolver "No se encontró información"]
    H --> J[Mostrar Respuesta]
    I --> J
    D -->|No| K[Convertir Pregunta en Embedding]
    K --> L[Buscar en Base de Conocimientos con FAISS]
    L --> M[Generar Respuesta con GroqAI]
    M --> J
    J --> N[Fin]



---

### Cómo Visualizarlo

1. **En GitHub**:
   - Copia y pega el código anterior en un archivo `.md` (por ejemplo, `diagrama.md`).
   - GitHub renderizará automáticamente el diagrama usando Mermaid.

2. **En VS Code**:
   - Instala la extensión **Mermaid** para VS Code.
   - Abre el archivo `.md` y verás una vista previa del diagrama.

3. **En un editor Markdown**:
   - Usa un editor que soporte Mermaid (como [Markdown Preview Enhanced](https://shd101wyy.github.io/markdown-preview-enhanced/)).

---

### Explicación del Diagrama

- **Nodos**:
  - `A[Inicio]`: Inicio del flujo.
  - `B[Interfaz de Streamlit]`: La interfaz de usuario.
  - `C[Entrada del Usuario]`: El usuario escribe una pregunta.
  - `D{¿La pregunta es sobre saldos?}`: Decisión sobre el tipo de pregunta.
  - `E[Extraer Nombre del Cliente]`: Extrae el nombre del cliente de la pregunta.
  - `F[Buscar Saldo en saldo.csv]`: Busca el saldo en el archivo CSV.
  - `G{¿Encontró el saldo?}`: Decisión sobre si se encontró el saldo.
  - `H[Devolver Saldo]`: Devuelve el saldo del cliente.
  - `I[Devolver "No se encontró información"]`: Devuelve un mensaje de error.
  - `J[Mostrar Respuesta]`: Muestra la respuesta al usuario.
  - `K[Convertir Pregunta en Embedding]`: Convierte la pregunta en un vector.
  - `L[Buscar en Base de Conocimientos con FAISS]`: Busca información relevante.
  - `M[Generar Respuesta con GroqAI]`: Genera una respuesta usando GroqAI.
  - `N[Fin]`: Fin del flujo.

- **Conectores**:
  - `-->`: Indica el flujo del proceso.
  - `-->|Sí|` y `-->|No|`: Indican decisiones condicionales.

---

### Ejemplo Renderizado

Si usas GitHub o un editor compatible, el diagrama se verá así:

```mermaid
graph TD
    A[Inicio] --> B[Interfaz de Streamlit]
    B --> C[Entrada del Usuario]
    C --> D{¿La pregunta es sobre saldos?}
    D -->|Sí| E[Extraer Nombre del Cliente]
    E --> F[Buscar Saldo en saldo.csv]
    F --> G{¿Encontró el saldo?}
    G -->|Sí| H[Devolver Saldo]
    G -->|No| I[Devolver "No se encontró información"]
    H --> J[Mostrar Respuesta]
    I --> J
    D -->|No| K[Convertir Pregunta en Embedding]
    K --> L[Buscar en Base de Conocimientos con FAISS]
    L --> M[Generar Respuesta con GroqAI]
    M --> J
    J --> N[Fin]