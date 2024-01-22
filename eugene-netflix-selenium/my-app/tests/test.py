import re

# Initialize an empty list to store the Netflix links and movie IDs
netflix_links = []
movies_ids = []

# Read the links from the movies_links.txt file and add them to the list
with open("movies_links.txt", "r") as file:
    for line in file:
        line = line.strip()  # Remove any leading/trailing spaces or newline characters
        if line.startswith("https://www.netflix.com/watch/"):
            netflix_links.append(line)
            # Extract the movie ID by splitting the URL at '/' and taking the last part
            movie_id = line.split("/")[-1]
            movie_id = re.split(r"[^0-9]", movie_id)[0]

            movies_ids.append(movie_id)

# Print the extracted Netflix links and movie IDs
for link in netflix_links:
    print(link)

for movie_id in movies_ids:
    print(movie_id)
