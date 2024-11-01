from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

class ThrowingErrorListener(ErrorListener):
    INSTANCE = None

    def __init__(self):
        super(ThrowingErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Aquí simplemente lanzamos el error con el mensaje original que ANTLR nos proporciona
        full_message = f'SYNTAX ERROR -> Line {line}:{column} {msg}'
        raise ParseCancellationException(full_message)

# Crear una instancia de la clase para reutilizarla
ThrowingErrorListener.INSTANCE = ThrowingErrorListener()
