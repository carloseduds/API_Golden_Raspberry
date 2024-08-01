from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Configuração da aplicação 'app'.
    """
    name = 'app'

    def ready(self):
        """
        Registra os sinais para verificação do arquivo CSV.
        """
        import app.signals
