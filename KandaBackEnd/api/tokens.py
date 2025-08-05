from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generador de tokens para la activación de cuentas de usuario.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Crea un hash único para cada usuario y timestamp.
        """
        # Usamos el ID del usuario, el estado de activación y el timestamp para generar un token único
        return (
            six.text_type(user.id) + 
            six.text_type(timestamp) + 
            six.text_type(user.is_active)
        )

# Instancia global del generador de tokens
account_activation_token = AccountActivationTokenGenerator()