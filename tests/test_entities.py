from src.chatbot.entity_extractor import extract_entities

def test_order_and_code():
    ents = extract_entities("Order 12345 and product AB-1234", "en")
    kinds = {e.kind for e in ents}
    assert "order_id" in kinds
    assert "product_code" in kinds

def test_date():
    ents = extract_entities("Deliver on 2024-05-01 please", "en")
    assert any(e.kind == "date" for e in ents)

def test_raw_preserved():
    ents = extract_entities("ORD-99887", "en")
    assert any(e.raw == "ORD-99887" for e in ents)