from bitcoinlib.wallets import Wallet
import concurrent.futures
import time
import random
import string

class NoBalanceWalletFound(Exception):
    pass

def generate_wallet_with_balance(attempts=10):
    for _ in range(attempts):
        # Generate a unique wallet name with a timestamp and random string
        unique_name = f'my_wallet_{int(time.time())}_{"".join(random.choices(string.ascii_letters, k=4))}'

        # Create a new wallet with the unique name
        wallet = Wallet.create(unique_name)

        # Check the balance of the wallet
        balance = wallet.balance()

        # Print the wallet details and balance
        print(f"Wallet Name: {unique_name}")
        print(f"Address: {wallet.get_key().address}")
        print(f"Private Key: {wallet.get_key().wif}")  # Note: Removed the '()' here
        print(f"Balance: {balance} BTC")

        # Check if the balance is greater than zero
        if balance > 0.000000000000000:
            print("Wallet has balance. Exiting the loop.")
            return wallet

    raise NoBalanceWalletFound("No wallet with a non-zero balance found within the specified attempts.")

def process_wallet():
    try:
        my_wallet = generate_wallet_with_balance(100000)
        return my_wallet
    except NoBalanceWalletFound as e:
        return str(e)

if __name__ == "__main__":
    # Number of processes for parallel execution
    num_processes = 25

    # Use ProcessPoolExecutor for parallel execution
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Create a list of futures for the processes
        future_results = [executor.submit(process_wallet) for _ in range(num_processes)]

        # Iterate over completed futures in the order they were completed
        for future in concurrent.futures.as_completed(future_results):
            try:
                result = future.result()
                if isinstance(result, Wallet):
                    print(f"Completed Process - Wallet Name: {result.name}")
                else:
                    print(f"Error: {result}")
            except Exception as e:
                print(f"An error occurred: {e}")
