from classes.Language import Language


class French(Language):
    MAIN_STARTING = "Démarrage du Bot WhatsApp v{}..."
    MAIN_UNEXPECTED_ERROR = "Une erreur inattendue s'est produite !"
    DB_NO_CREDENTIALS = "Veuillez ajouter les informations d'identification de la base de données dans le fichier '.env' !"
    DB_INITIALIZING = "Initialisation de la base de données..."
    DB_COULDNT_INITIALIZE = "Impossible d'initialiser la base de données!"
    DB_INITIALIZED = "Base de données initialisée."
    DB_CLOSING = "Fermeture de la session de base de données..."
    BOT_DRIVER_NOT_FOUND_DOWNLOADING = "Pilote introuvable! Le télécharger..."
    BOT_DRIVER_COULDNT_DOWNLOAD = "Impossible de télécharger le pilote!"
    BOT_DRIVER_DOWNLOADED = "Le pilote a été téléchargé avec succès."
    BOT_DRIVER_INITIALIZING = "Initialisation du pilote..."
    BOT_DRIVER_INVALID_VERSION_DOWNLOADING = (
        "Version de pilote invalide! Téléchargement du bon..."
    )
    BOT_DRIVER_INITIALIZED = "Pilote initialisé."
    BOT_PINNED_CHAT_COULDNT_FIND_RETRYING = "Impossible de trouver un chat épinglé sur lequel se concentrer ! Réessayer dans {} secondes... ({}/{})"
    BOT_PINNED_CHAT_COULDNT_FIND = "Impossible de trouver une conversation épinglée sur laquelle se concentrer. ({}/{})"
    BOT_LOGIN_TRYING = "Tentative de connexion..."
    BOT_LOGIN_ALREADY_LOGGED = "Déjà connecté."
    BOT_LOGIN_AWAITING_QR_SCAN = "En attente de scan du code QR..."
    BOT_LOGIN_QR_SCANNED = "Scanné, connexion..."
    BOT_LOGIN_LOGGED = "Connecté."
    BOT_LOGIN_QR_ERROR = "Il y a eu une erreur avec le code QR! Essayer à nouveau..."
    BOT_LOGIN_COULDNT_LOGIN_RETRYING = (
        "Impossible de se connecter ! Réessayer dans {} secondes..."
    )
    BOT_LOGIN_COULDNT_LOGIN = "Impossible de se connecter."
    BOT_MESSAGE_HANDLING = "Traitement des messages..."
    BOT_MESSAGE_HANDLING_ERROR = (
        "Une erreur s'est produite lors de la gestion d'un message!"
    )
    BOT_MESSAGE_HANDLING_SPAMMING = (
        "{} est probablement en train de spammer des messages!"
    )
    BOT_CLOSE_CLOSING = "Fermeture de l'instance de pilote..."
    COMMAND_HANDLER_REGISTERING = "Enregistrement de la commande {}: {}..."
    COMMAND_HANDLER_EXECUTED_COMMAND = "{} ({}) a exécuté une commande en {}s: {}"
    COMMAND_HANDLER_EXECUTING_ERROR = (
        "Une erreur s'est produite lors de l'exécution de la commande: {}"
    )

    def __repr__(self) -> str:
        return "French"
