from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Header, Footer, DataTable, Button, Label, Static
import random

# Drugs & initial prices
DRUGS = ["Weed", "Cocaine", "Heroin", "Ecstasy", "Meth"]
LOCATIONS = ["New York", "Miami", "Chicago", "Los Angeles"]
STARTING_CASH = 2000
MAX_QUANTITY = 10  # Max units per drug per market reset

class TextWars(App):
    CSS = """
    Screen {
        align: center middle;
    }
    .buttons {
        width: 20%;
    }
    """

    def __init__(self):
        super().__init__()
        self.cash = STARTING_CASH
        self.inventory = {drug: 0 for drug in DRUGS}
        self.prices = {}
        self.location = "New York"
        self.update_market()

    def update_market(self):
        """Generate random drug prices."""
        self.prices = {drug: random.randint(50, 1000) for drug in DRUGS}

    def on_mount(self):
        """Set up UI components."""
        self.title = "TextWars - A Dopewars Clone"
        self.query_one(DataTable).add_columns("Drug", "Price", "Owned")
        self.refresh_market()

    def refresh_market(self):
        """Update the UI with the latest drug prices and inventory."""
        table = self.query_one(DataTable)
        table.clear()
        for drug in DRUGS:
            table.add_row(drug, f"${self.prices[drug]}", str(self.inventory[drug]))

        self.query_one("#cash_label").update(f"Cash: ${self.cash}")
        self.query_one("#location_label").update(f"Location: {self.location}")

    def buy(self, drug):
        """Buy a unit of the drug if affordable."""
        if self.cash >= self.prices[drug]:
            self.cash -= self.prices[drug]
            self.inventory[drug] += 1
            self.refresh_market()

    def sell(self, drug):
        """Sell a unit of the drug if owned."""
        if self.inventory[drug] > 0:
            self.cash += self.prices[drug]
            self.inventory[drug] -= 1
            self.refresh_market()

    def travel(self):
        """Move to a random new location and refresh market."""
        self.location = random.choice([loc for loc in LOCATIONS if loc != self.location])
        self.update_market()
        self.refresh_market()

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with VerticalScroll():
                yield Static("Inventory & Market", classes="buttons")
                yield DataTable()
                yield Label(f"Cash: ${self.cash}", id="cash_label")
                yield Label(f"Location: {self.location}", id="location_label")
            with VerticalScroll(classes="buttons"):
                yield Static("Actions")
                for drug in DRUGS:
                    yield Button(f"Buy {drug}", id=f"buy_{drug}")
                    yield Button(f"Sell {drug}", id=f"sell_{drug}")
                yield Button("Travel", id="travel_button")
        yield Footer()

    def on_button_pressed(self, event):
        """Handle button presses."""
        button_id = event.button.id
        if button_id.startswith("buy_"):
            self.buy(button_id[4:])
        elif button_id.startswith("sell_"):
            self.sell(button_id[5:])
        elif button_id == "travel_button":
            self.travel()

if __name__ == "__main__":
    TextWars().run()