from app import agente_atencion_al_cliente

def test_saldo_cliente():
    respuesta = agente_atencion_al_cliente("¿Cuál es el saldo de Juan Pérez?")
    assert "1250.50" in respuesta

def test_pregunta_conocimiento():
    respuesta = agente_atencion_al_cliente("¿Cómo puedo abrir una cuenta bancaria?")
    assert "abrir una cuenta" in respuesta.lower()

def test_cliente_no_encontrado():
    respuesta = agente_atencion_al_cliente("¿Cuál es el saldo de Ana López?")
    assert "no se encontró información" in respuesta.lower()