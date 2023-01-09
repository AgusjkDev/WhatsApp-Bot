from classes.Language import Language


class Italian(Language):
    MAIN_STARTING = "Avvio WhatsApp Bot v{}..."
    MAIN_UNEXPECTED_ERROR = "Si è verificato un errore imprevisto!"
    DB_NO_CREDENTIALS = "Aggiungi le credenziali del database nel file '.env'!"
    DB_INITIALIZING = "Inizializzazione del database..."
    DB_INITIALIZED = "Database inizializzato."
    DB_CLOSING = "Chiusura della sessione del database..."
    BOT_DRIVER_NOT_FOUND_DOWNLOADING = "Driver non trovato! Scaricandolo..."
    BOT_DRIVER_COULDNT_DOWNLOAD = "Impossibile scaricare il driver!"
    BOT_DRIVER_DOWNLOADED = "Driver scaricato correttamente."
    BOT_DRIVER_INITIALIZING = "Inizializzazione driver..."
    BOT_DRIVER_INVALID_VERSION_DOWNLOADING = (
        "Versione del driver non valida! Download di quello corretto..."
    )
    BOT_DRIVER_INITIALIZED = "Driver inizializzato."
    BOT_PINNED_CHAT_COULDNT_FIND_RETRYING = "Impossibile trovare una chat bloccata su cui concentrarsi! Riprovo tra {} secondi... ({}/{})"
    BOT_PINNED_CHAT_COULDNT_FIND = (
        "Impossibile trovare una chat bloccata su cui concentrarsi. ({}/{})"
    )
    BOT_LOGIN_TRYING = "Tentativo di accesso..."
    BOT_LOGIN_ALREADY_LOGGED = "Ha già effettuato il login."
    BOT_LOGIN_AWAITING_QR_SCAN = "In attesa di scansione del codice QR..."
    BOT_LOGIN_QR_SCANNED = "Scansionato, accesso..."
    BOT_LOGIN_LOGGED = "Connesso."
    BOT_LOGIN_QR_ERROR = "Si è verificato un errore con il codice QR! Riprovare..."
    BOT_LOGIN_COULDNT_LOGIN_RETRYING = (
        "Impossibile accedere! Riprovo tra {} secondi... ({}/{})"
    )
    BOT_LOGIN_COULDNT_LOGIN = "Impossibile accedere."
    BOT_MESSAGE_HANDLING = "Gestione dei messaggi..."
    BOT_MESSAGE_HANDLING_ERROR = (
        "Si è verificato un errore durante la gestione di un messaggio!"
    )
    BOT_MESSAGE_HANDLING_SPAMMING = "Probabilmente {} sta inviando messaggi di spam!"
    BOT_CLOSE_CLOSING = "Chiusura dell'istanza del driver..."
    COMMAND_HANDLER_REGISTERING = "Registrazione del comando {}: {}..."
    COMMAND_HANDLER_EXECUTED_COMMAND = "{} ({}) ha eseguito un comando in {}s: {}"
    COMMAND_HANDLER_EXECUTING_ERROR = (
        "Si è verificato un errore durante l'esecuzione del comando: {}"
    )

    def __repr__(self) -> str:
        return "Italian"
