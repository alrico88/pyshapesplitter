from InquirerPy import inquirer
import geopandas as gpd
from pathlib import Path
from yaspin import yaspin


def ask_for_property_generic(message: str, choices: list) -> str:
    return inquirer.select(message=message, choices=choices).execute()


def ask_for_filter_type() -> str:
    choices = ("By text", "From a list")

    return inquirer.select(
        message="Which way would you like to filter?", choices=choices
    ).execute()


def ask_for_output_dir() -> str:
    home = str(Path.home())

    default_output_dir = Path(f"{home}/Shapefiles").resolve()

    output_dir = inquirer.text(
        message="Enter an output folder", default=str(default_output_dir)
    ).execute()

    return output_dir.rstrip("/")


def write_geojson(output_dir: str, filename: str, geojson: str):
    f = open(
        Path(f"{output_dir}/{filename}.geojson").resolve(),
        "w",
    )
    f.write(geojson)
    f.close()


def main():
    filepath = inquirer.text(message="Path to shapefile to split").execute()

    reading_spinner = yaspin(text="Reading shapefile")
    reading_spinner.start()
    df = gpd.read_file(filename=Path(filepath.strip()).resolve())
    reading_spinner.text = f"Successfully read file. Found {df.shape[0]} features"
    reading_spinner.ok()

    columns = list(filter(lambda x: x != "geometry", list(df.columns)))
    column_to_split_by = ask_for_property_generic(
        message="Choose a column to split by", choices=columns
    )

    wants_filter = inquirer.confirm(
        message="Do you want to filter the items to split?", default=False
    ).execute()

    filter_fn = lambda x: True

    if wants_filter:
        column_to_filter_by = ask_for_property_generic(
            message="Select a property to filter by", choices=columns
        )

        filter_type = ask_for_filter_type()

        if filter_type == "From a list":
            distinct_filter_values = sorted(df[column_to_filter_by].unique())

            items_to_filter = inquirer.select(
                message="Choose values to keep",
                choices=distinct_filter_values,
                multiselect=True,
            ).execute()

            filter_fn = lambda row: row[column_to_filter_by] in items_to_filter
        else:
            search_str = inquirer.text(message="Enter a string to search for").execute()

            filter_fn = lambda row: search_str in row[column_to_filter_by]

    filter_result = df.apply(filter_fn, axis=1)
    df = df[filter_result]
    files_to_create = df[column_to_split_by].unique()
    files_amount = len(files_to_create)

    output_dir = ask_for_output_dir()

    writing_spinner = yaspin(text=f"Writing {files_amount} files")
    writing_spinner.start()

    for index, item in enumerate(files_to_create):
        writing_spinner.text = f"Writing file {index + 1} of {files_amount}: {item}"
        filtered_df = df[df[column_to_split_by] == item]
        write_geojson(
            output_dir=output_dir, filename=item, geojson=filtered_df.to_json()
        )

    writing_spinner.text = f"Written {files_amount} files to {output_dir}"
    writing_spinner.ok()


if __name__ == "__main__":
    main()
