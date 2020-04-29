import basilica
import os 

# Grab pertinent environment variable data
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY")

# Create a connection object
connection = basilica.Connection(BASILICA_API_KEY)

if __name__ == "__main__":
    embedding = connection.embed_sentence("This is my tweet", model="twitter")

    tweets = ["Hello World!", "BTC to the moon!"]
    print(f"INFO: Running a test embedding Basilica call")
    ctr = 0
    for embed in embedding:
        print(f"TEST: Embed #{ctr}: ", embed)
        ctr = ctr + 1
        if ctr > 3:
            print(f"TEST: ...")
            break


    
