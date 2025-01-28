import hashlib
import time

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.generate_hash()

    def generate_hash(self, nonce=None):
        if nonce is None:
            nonce = self.nonce
        block_data = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{nonce}"
        return hashlib.sha256(block_data.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2  # You can adjust this difficulty for testing

    def create_genesis_block(self):
        return Block(0, time.time(), ["Genesis Block"], "0")

    def add_new_block(self, transactions):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), transactions, last_block.hash)
        self.apply_proof_of_work(new_block)
        self.chain.append(new_block)

    def apply_proof_of_work(self, block):
        while not block.hash.startswith('0' * self.difficulty):
            block.nonce += 1
            block.timestamp = time.time()
            block.hash = block.generate_hash(block.nonce)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            # Validate hash
            if current_block.hash != current_block.generate_hash(current_block.nonce):
                return False
            # Validate chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def display_chain(self):
        for block in self.chain:
            print(f"Block {block.index} - Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Nonce: {block.nonce}\n")

if __name__ == "__main__":
    blockchain = Blockchain()

    while True:
        print("\n=== Blockchain Menu ===")
        print("1. Add a new block")
        print("2. Display the blockchain")
        print("3. Check blockchain integrity")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Enter transactions (type 'done' to finish):")
            transactions = []
            while True:
                transaction = input("> ")
                if transaction.lower() == 'done':
                    break
                transactions.append(transaction)
            blockchain.add_new_block(transactions)
            print("New block added successfully!")

        elif choice == "2":
            blockchain.display_chain()

        elif choice == "3":
            print("Blockchain integrity is valid:", blockchain.is_chain_valid())

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
