import re


def clean_netflix_links(input_file, output_file):
    cleaned_links = []

    with open(input_file, "r") as file:
        for line in file:
            line = (
                line.strip()
            )  # Remove any leading/trailing spaces or newline characters
            if line.startswith("https://www.netflix.com/watch/"):
                # Extract the movie ID using regular expression
                movie_id = re.split(r"[^0-9]", line.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    # Writing the cleaned links to the output file
    with open(output_file, "w") as file:
        for link in cleaned_links:
            file.write(link + "\n")


# Replace 'movies_links.txt' with the path to your input file and specify the output file name
clean_netflix_links("./source/movies_links.txt", "./source/movies_links_cleaned.txt")
