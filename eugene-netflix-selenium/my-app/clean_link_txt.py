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

    # Sort the links in descending order based on the numeric part of the ID
    sorted_links = sorted(cleaned_links, key=lambda x: int(x.split("/")[-1]))
    unique_sorted_links = sorted(set(link.strip() for link in sorted_links))

    # Writing the sorted and cleaned links to the output file
    with open(output_file, "w") as file:
        for link in unique_sorted_links:
            file.write(link + "\n")


# Replace './source/movies_links.txt' and './source/movies_links_cleaned.txt'
# with the paths to your input and output files, respectively
# clean_netflix_links("./source/movies_links.txt", "./source/movies_links_cleaned.txt")
clean_netflix_links(
    "./source/movies_links_inaccessed.txt",
    "./source/movies_links_inaccessed_cleaned.txt",
)
