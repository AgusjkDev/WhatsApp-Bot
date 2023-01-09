from classes.Language import Language


class German(Language):
    MAIN_STARTING = "WhatsApp Bot v{} starten..."
    MAIN_UNEXPECTED_ERROR = "Es ist ein unerwarteter Fehler aufgetreten!"
    DB_NO_CREDENTIALS = (
        "Bitte fügen Sie die Datenbankanmeldeinformationen in der '.env'-Datei hinzu!"
    )
    DB_INITIALIZING = "Datenbank wird initialisiert..."
    DB_INITIALIZED = "Datenbank initialisiert."
    DB_CLOSING = "Datenbanksitzung wird geschlossen..."
    BOT_DRIVER_NOT_FOUND_DOWNLOADING = "Treiber nicht gefunden! Herunterladen..."
    BOT_DRIVER_COULDNT_DOWNLOAD = "Der Treiber konnte nicht heruntergeladen werden!"
    BOT_DRIVER_DOWNLOADED = "Treiber erfolgreich heruntergeladen."
    BOT_DRIVER_INITIALIZING = "Treiber initialisieren..."
    BOT_DRIVER_INVALID_VERSION_DOWNLOADING = (
        "Ungültige Treiberversion! Richtiges herunterladen..."
    )
    BOT_DRIVER_INITIALIZED = "Treiber initialisiert.."
    BOT_PINNED_CHAT_COULDNT_FIND_RETRYING = "Es konnte kein angehefteter Chat gefunden werden, auf den Sie sich konzentrieren können! Versuchen Sie es in {} Sekunden erneut... ({}/{})"
    BOT_PINNED_CHAT_COULDNT_FIND = "Es konnte kein angehefteter Chat gefunden werden, auf den man sich konzentrieren könnte. ({}/{})"
    BOT_LOGIN_TRYING = "Versuchen sich einzuloggen..."
    BOT_LOGIN_ALREADY_LOGGED = "Bereits angemeldet"
    BOT_LOGIN_AWAITING_QR_SCAN = "Warten auf QR-Code-Scan..."
    BOT_LOGIN_QR_SCANNED = "Gescannt, Einloggen..."
    BOT_LOGIN_LOGGED = "Eingeloggt."
    BOT_LOGIN_QR_ERROR = (
        "Beim QR-Code ist ein Fehler aufgetreten! Versuch es nochmal..."
    )
    BOT_LOGIN_COULDNT_LOGIN_RETRYING = (
        "Anmeldung nicht möglich! Versuchen Sie es in {} Sekunden erneut... ({}/{})"
    )
    BOT_LOGIN_COULDNT_LOGIN = "Anmeldung nicht möglich."
    BOT_MESSAGE_HANDLING = "Nachrichten bearbeiten..."
    BOT_MESSAGE_HANDLING_ERROR = (
        "Beim Bearbeiten einer Nachricht ist ein Fehler aufgetreten!"
    )
    BOT_MESSAGE_HANDLING_SPAMMING = "{} spammt wahrscheinlich Nachrichten!"
    BOT_CLOSE_CLOSING = "Treiberinstanz wird geschlossen..."
    COMMAND_HANDLER_REGISTERING = "Registrieren des {} Befehls: {}..."
    COMMAND_HANDLER_EXECUTED_COMMAND = "{} ({}) hat einen Befehl in {}s ausgeführt: {}"
    COMMAND_HANDLER_EXECUTING_ERROR = (
        "Beim Ausführen des Befehls ist ein Fehler aufgetreten: {}"
    )

    def __repr__(self) -> str:
        return "German"
