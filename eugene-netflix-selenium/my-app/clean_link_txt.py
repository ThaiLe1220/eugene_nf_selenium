import re
import os


def clean_netflix_inacessible_links(input_file, output_file, lang_code):
    cleaned_links = []

    with open(input_file, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("https://www.netflix.com/watch/"):
                movie_id = re.split(r"[^0-9]", line.split("/")[-1])[0]
                cleaned_link = f"https://www.netflix.com/watch/{movie_id}"
                cleaned_links.append(cleaned_link)

    unique_sorted_links = sorted(
        set(cleaned_links), key=lambda x: int(x.split("/")[-1])
    )

    directory = f"./markup/en-{lang_code}/"
    markup_files = os.listdir(directory)

    # Check if the movie_id is in the markup file names
    inaccessible_links = [
        link
        for link in unique_sorted_links
        if not any(movie_id in file for file in markup_files)
    ]
    file_count = len(
        [
            name
            for name in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, name))
        ]
    )
    print(f"There are {file_count} files in {directory}")

    # Write the accessible links to the output file
    with open(output_file, "w") as file:
        for link in inaccessible_links:
            file.write(link + "\n")


# clean_netflix_links("./source/movies_links.txt", "./source/movies_links_cleaned.txt")
clean_netflix_inacessible_links(
    "./source/movies_links_inaccessed.txt",
    "./source/movies_links_inaccessed_cleaned.txt",
    "vi",
)
