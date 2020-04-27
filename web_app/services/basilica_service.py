import basilica
import os 

# Grab pertinent environment variable data
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY")

# Create a connection object
connection = basilica.Connection(BASILICA_API_KEY)

if __name__ == "__main__":
    embedding = connection.embed_sentence("This is my tweet", model="twitter")

    tweets = ["Hello World!", "BTC to the moon!"]
    for embed in embeddings:
        print("----")
        print(len(embed))
