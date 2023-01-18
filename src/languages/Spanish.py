from classes.Language import Language


class Spanish(Language):
    MAIN_STARTING = "Iniciando Bot de WhatsApp v{}..."
    MAIN_UNEXPECTED_ERROR = "¡Ha ocurrido un error inesperado!"
    DB_NO_CREDENTIALS = (
        "¡Por favor, añade las credenciales de la bases de datos en el archivo '.env'!"
    )
    DB_INITIALIZING = "Inicializando base de datos..."
    DB_COULDNT_INITIALIZE = "¡No se pudo inicializar la base de datos!"
    DB_INITIALIZED = "Base de datos inicializada."
    DB_CLOSING = "Cerrando sesión de la base de datos..."
    BOT_DRIVER_NOT_FOUND_DOWNLOADING = (
        "¡No se ha encontrado el controlador! Descargándolo..."
    )
    BOT_DRIVER_COULDNT_DOWNLOAD = "¡No se pudo descargar el controlador!"
    BOT_DRIVER_DOWNLOADED = "Controlador descargado satisfactoriamente."
    BOT_DRIVER_INITIALIZING = "Inicializando controlador..."
    BOT_DRIVER_INVALID_VERSION_DOWNLOADING = (
        "¡Version inválida de controlador! Descargando la correcta..."
    )
    BOT_DRIVER_INITIALIZED = "Controlador inicializado."
    BOT_PINNED_CHAT_COULDNT_FIND_RETRYING = "¡No se pudo encontrar un chat fijado en el que enfocarse! Intentando nuevamente en {} segundos... ({}/{})"
    BOT_PINNED_CHAT_COULDNT_FIND = (
        "No se pudo encontrar un chat fijado en el que enfocarse. ({}/{})"
    )
    BOT_LOGIN_TRYING = "Intentando iniciar sesión..."
    BOT_LOGIN_ALREADY_LOGGED = "Sesión ya iniciada."
    BOT_LOGIN_AWAITING_QR_SCAN = "Esperando escaneo de código QR..."
    BOT_LOGIN_QR_SCANNED = "Escaneado, iniciando sesión..."
    BOT_LOGIN_LOGGED = "Sesión iniciada."
    BOT_LOGIN_QR_ERROR = (
        "Ha ocurrido un error inesperado con el código QR! Intentando nuevamente..."
    )
    BOT_LOGIN_COULDNT_LOGIN_RETRYING = (
        "¡No se pudo iniciar sesión! Intentando nuevamente en {} segundos... ({}/{})"
    )
    BOT_LOGIN_COULDNT_LOGIN = "No se pudo iniciar sesión."
    BOT_MESSAGE_HANDLING = "Controlando mensajes..."
    BOT_MESSAGE_HANDLING_ERROR = "¡Ha ocurrido un error controlando un mensaje!"
    BOT_MESSAGE_HANDLING_SPAMMING = "¡Probablemente {} está spammeando!"
    BOT_CLOSE_CLOSING = "Cerrando sesión del controlador..."
    COMMAND_HANDLER_REGISTERING = "Registrando comando {}: {}..."
    COMMAND_HANDLER_EXECUTED_COMMAND = "{} ({}) ejecutó un comando en {}s: {}"
    COMMAND_HANDLER_EXECUTING_ERROR = "Ocurrió un error ejecutando el comando: {}"

    def __repr__(self) -> str:
        return "Spanish"
