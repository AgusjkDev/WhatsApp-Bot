from classes.Language import Language


class Portuguese(Language):
    MAIN_STARTING = "Iniciando o WhatsApp Bot v{}..."
    MAIN_UNEXPECTED_ERROR = "Ocorreu um erro inesperado!"
    DB_NO_CREDENTIALS = "Adicione as credenciais do banco de dados no arquivo '.env'!"
    DB_INITIALIZING = "Inicializando banco de dados..."
    DB_COULDNT_INITIALIZE = "Não foi possível inicializar o banco de dados!"
    DB_INITIALIZED = "Banco de dados inicializado."
    DB_CLOSING = "Fechando a sessão do banco de dados..."
    BOT_DRIVER_NOT_FOUND_DOWNLOADING = "Driver não encontrado! Baixando..."
    BOT_DRIVER_COULDNT_DOWNLOAD = "Não foi possível baixar o driver!"
    BOT_DRIVER_DOWNLOADED = "Driver baixado com sucesso."
    BOT_DRIVER_INITIALIZING = "Inicializando driver..."
    BOT_DRIVER_INVALID_VERSION_DOWNLOADING = (
        "Versão do driver inválida! Baixando o correto..."
    )
    BOT_DRIVER_INITIALIZED = "Driver inicializado."
    BOT_PINNED_CHAT_COULDNT_FIND_RETRYING = "Não foi possível encontrar um bate-papo fixado para focar! Tentando novamente em {} segundos... ({}/{})"
    BOT_PINNED_CHAT_COULDNT_FIND = (
        "Não foi possível encontrar um bate-papo fixado para focar. ({}/{})"
    )
    BOT_LOGIN_TRYING = "Tentando logar..."
    BOT_LOGIN_ALREADY_LOGGED = "Já logado."
    BOT_LOGIN_AWAITING_QR_SCAN = "Aguardando leitura do código QR..."
    BOT_LOGIN_QR_SCANNED = "Verificado, logando..."
    BOT_LOGIN_LOGGED = "Logado."
    BOT_LOGIN_QR_ERROR = "Ocorreu um erro com o código QR! Tentando novamente..."
    BOT_LOGIN_COULDNT_LOGIN_RETRYING = (
        "Não foi possível fazer login! Tentando novamente em {} segundos... ({}/{})"
    )
    BOT_LOGIN_COULDNT_LOGIN = "Não foi possível fazer login."
    BOT_MESSAGE_HANDLING = "Gerenciando mensagens..."
    BOT_MESSAGE_HANDLING_ERROR = "Ocorreu um erro ao processar uma mensagem!"
    BOT_MESSAGE_HANDLING_SPAMMING = "{} provavelmente está enviando mensagens de spam!"
    BOT_CLOSE_CLOSING = "Fechando instância do driver..."
    COMMAND_HANDLER_REGISTERING = "Registrando o comando {}: {}..."
    COMMAND_HANDLER_EXECUTED_COMMAND = "{} ({}) executou um comando em {}s: {}"
    COMMAND_HANDLER_EXECUTING_ERROR = "Ocorreu um erro ao executar o comando: {}"

    def __repr__(self) -> str:
        return "Portuguese"
