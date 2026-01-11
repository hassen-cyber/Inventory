
import datetime

class Medicine:
    def __init__(self, drug_id, name, dosage, price, quantity, expiry_date):
        self.drug_id = drug_id
        self.name = name
        self.dosage = dosage  # e.g., "500mg"
        self.price = price
        self.quantity = quantity
        self.expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d").date()

    def is_expired(self):
        """Checks if the medicine is past its expiry date."""
        return datetime.date.today() > self.expiry_date

    def __str__(self):
        return f"[{self.drug_id}] {self.name} ({self.dosage}) - Stock: {self.quantity} - Exp: {self.expiry_date}"

class PharmacySystem:
    def __init__(self):
        self.inventory = {}
        self.sales_log = []

    def add_medicine(self, medicine):
        """Adds a new medicine object to the inventory."""
        self.inventory[medicine.drug_id] = medicine
        print(f"SUCCESS: Added {medicine.name} to inventory.")

    def check_stock(self, drug_id):
        """Returns stock level for a specific drug."""
        if drug_id in self.inventory:
            return self.inventory[drug_id]
        return None

    def dispense_medicine(self, drug_id, quantity_needed):
        """
        Processes a transaction with safety checks:
        1. Existence check
        2. Expiration check
        3. Stock availability check
        """
        drug = self.check_stock(drug_id)

        # 1. Existence Check
        if not drug:
            print(f"ERROR: Drug ID {drug_id} not found in system.")
            return

        # 2. Expiration Check
        if drug.is_expired():
            print(f"CRITICAL WARNING: Cannot dispense {drug.name}. Expired on {drug.expiry_date}.")
            return

        # 3. Stock Check
        if drug.quantity < quantity_needed:
            print(f"ERROR: Insufficient stock for {drug.name}. Have: {drug.quantity}, Needed: {quantity_needed}")
            return

        # Process Transaction
        drug.quantity -= quantity_needed
        total_cost = drug.price * quantity_needed
        
        transaction_record = {
            "date": datetime.date.today(),
            "drug": drug.name,
            "qty": quantity_needed,
            "total": total_cost
        }
        self.sales_log.append(transaction_record)

        print(f"--- RECEIPT ---")
        print(f"Dispensed: {drug.name} {drug.dosage}")
        print(f"Quantity: {quantity_needed}")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Remaining Stock: {drug.quantity}")
        print(f"---------------")

# ==========================================
# Main Execution
# ==========================================

if __name__ == "__main__":
    system = PharmacySystem()

    # 1. Setup Inventory (Simulating Database)
    # Note: Amoxicillin is set with a future date, Paracetamol with a past date
    med1 = Medicine("RX001", "Amoxicillin", "500mg", 12.50, 100, "2028-12-31")
    med2 = Medicine("RX002", "Paracetamol", "650mg", 5.00, 50, "2022-01-01") 

    system.add_medicine(med1)
    system.add_medicine(med2)

    print("\n--- Test Case 1: Successful Dispense ---")
    system.dispense_medicine("RX001", 10)

    print("\n--- Test Case 2: Expired Medicine Check ---")
    system.dispense_medicine("RX002", 5)

    print("\n--- Test Case 3: Insufficient Stock Check ---")
    system.dispense_medicine("RX001", 200)
