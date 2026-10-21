import re

class LanguagePack:
    def __init__(self, code, script_re, lexicon, translit, intent_kw):
        self.code = code
        self.script_re = re.compile(script_re) if script_re else None
        self.lexicon = set(lexicon)
        self.translit = translit
        self.intent_kw = intent_kw

PACKS = {
    "en": LanguagePack(
        "en", r"[A-Za-z]",
        ["order","status","cancel","refund","address","change","thanks","hello","help","track","return","money"],
        {},
        {"order_status": {"order","status","track","where","when"},
         "cancel":       {"cancel","stop","abort"},
         "refund":       {"refund","money","return"},
         "greet":        {"hello","hi","hey","greetings"},
         "thanks":       {"thanks","thank","appreciate"}},
    ),
    "hi": LanguagePack(
        "hi", r"[\u0900-\u097F]",
        ["ऑर्डर","स्थिति","रद्द","धन्यवाद","नमस्ते","पता","कितना","कब","कहाँ"],
        {"order":"ऑर्डर","kitna":"कितना","dhanyavad":"धन्यवाद","namaste":"नमस्ते",
         "stithi":"स्थिति","radd":"रद्द","pata":"पता","kab":"कब","kahan":"कहाँ"},
        {"order_status": {"ऑर्डर","स्थिति","कितना","कब","कहाँ"},
         "cancel":       {"रद्द"},
         "refund":       {"वापस","पैसा"},
         "greet":        {"नमस्ते"},
         "thanks":       {"धन्यवाद"}},
    ),
    "ta": LanguagePack(
        "ta", r"[\u0B80-\u0BFF]",
        ["ஆர்டர்","நிலை","ரத்து","நன்றி","வணக்கம்","எப்போது","எங்கே"],
        {"order":"ஆர்டர்","nandri":"நன்றி","vanakkam":"வணக்கம்",
         "nilai":"நிலை","eppo":"எப்போது","enge":"எங்கே"},
        {"order_status": {"ஆர்டர்","நிலை","எப்போது","எங்கே"},
         "cancel":       {"ரத்து"},
         "refund":       {"பணம்","திரும்ப"},
         "greet":        {"வணக்கம்"},
         "thanks":       {"நன்றி"}},
    ),
    "es": LanguagePack(
        "es", r"[A-Za-zÁÉÍÓÚÑáéíóúñ]",
        ["pedido","estado","cancelar","gracias","hola","dirección","cuándo","dónde","reembolso"],
        {},
        {"order_status": {"pedido","estado","cuándo","dónde"},
         "cancel":       {"cancelar"},
         "refund":       {"reembolso","dinero","devolver"},
         "greet":        {"hola"},
         "thanks":       {"gracias"}},
    ),
}