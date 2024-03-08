from bitcoinlib.wallets import Wallet
import concurrent.futures
import time
import random
import string

class NoBalanceWalletFound(Exception):
    pass

def generate_wallet_with_balance():
    i = 0
    while i < 10000000:
        # Generate a unique wallet name with a timestamp and random string
        unique_name = f'my_wallet_{int(time.time())}_{"".join(
            random.choices(string.ascii_letters, k=4))}'

        # Create a new wallet with the unique name
        wallet = Wallet.create(unique_name)

        # Check the balance of the wallet
        balance = wallet.balance()

        # Print the count of the number of wallets created only in one line 
        print(f"Wallet created. Balance: {balance} BTC, Number of wallets created: {i}", end="\r")

        # Check if the balance is greater than zero
        if balance > 0.000000000000000:
            print("Wallet has balance. Exiting the loop.")
            print(f"Wallet Name: {unique_name}")
            print(f"Address: {wallet.get_key().address}")
            print(f"Private Key: {wallet.get_key().wif}")  # Note: Removed the '()' here
            print(f"Balance: {balance} BTC")
            return wallet
        i += 1

    raise NoBalanceWalletFound("No wallet with a non-zero balance found within the specified attempts.")

def process_wallet():
    try:
        my_wallet = generate_wallet_with_balance()
        return my_wallet
    except NoBalanceWalletFound as e:
        return str(e)

if __name__ == "__main__":
    # Number of processes for parallel execution
    num_processes = 25

    # Create a thread pool executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_processes) as executor:
        # Submit the process_wallet function to the executor
        future = executor.submit(process_wallet)

        # Print the result of the process_wallet function
        print(future.result())

    # if error occurs, it will be printed here
    print(future.exception())
