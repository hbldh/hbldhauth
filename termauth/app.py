from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, Button, Static
import datetime

from termauth.utils import read_tokens, now

class TOTPTable(DataTable):
    """Widget to display TOTP codes in a table."""

    def __init__(self, tokens_path, **kwargs):
        super().__init__(**kwargs)
        self.tokens_path = tokens_path
        self.tokens = read_tokens(tokens_path)

    def on_mount(self):
        """Initialize the table and populate it."""
        self.add_columns("Issuer", "Account", "TOTP Code", "Valid For")
        self.update_totp()

    def update_totp(self):
        """Update the TOTP codes in the table."""
        self.clear()  # Clear existing rows
        valid_for = 30 - datetime.datetime.now().second % 30
        for issuer, account, token in self.tokens:
            otp = now(token)
            self.add_row(issuer, account, otp, f"{valid_for} seconds")


class AuthenticatorApp(App):
    """Main TUI application."""

    CSS = """
    Screen {
        align: center middle;
    }
    Static#header {
        color: #00FF00;
        text-align: center;
        margin-bottom: 1;
    }
    DataTable {
        margin: 1 0;
        width: 100%;
        align: center middle;
    }
    """

    def __init__(self, tokens_path, **kwargs):
        super().__init__(**kwargs)
        self.tokens_path = tokens_path

    def compose(self) -> ComposeResult:
        """Compose the layout."""
        with Vertical():
            yield Static("--- TermAuth ---", id="header")  # Large static header
            self.totp_table = TOTPTable(self.tokens_path)
            yield self.totp_table
            yield Button("Exit", id="exit")

    def on_mount(self):
        """Set up periodic refresh."""
        self.set_interval(0.5, self.refresh_totp)

    def refresh_totp(self):
        """Refresh the TOTP table."""
        self.totp_table.update_totp()

    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        if event.button.id == "exit":
            self.exit()

    def on_key(self, event):
        """Handle key presses."""
        if event.key == "escape":
            self.exit()


def main():
    import pathlib
    tokens_path = str(pathlib.Path.home().joinpath('.hbldhauth'))
    app = AuthenticatorApp(tokens_path)
    app.run()

if __name__ == "__main__":
    main()