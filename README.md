The **'omopsurvey'** Python package offers a comprehensive solution for transforming standardized response codes from the Observational Medical Outcomes Partnership (OMOP) Common Data Model (CDM) survey variables into numeric values, streamlining the data preparation process. By automating the mapping and conversion of response codes, as well as the handling of missing data, it makes data analysis more accessible and reliable. The package provides a range of functions designed to help researchers and data analysts efficiently work through OMOP CDM survey data, ensuring accurate mappings of responses and effective management of data discrepancies. This package is a helpful tool for those working with OMOP CDM survey data, offering a path to more profound and accurate analyses by dramatically lowering the burden of data preprocessing.

## response_set.py

>
>**map_items(input_data)**: Maps survey responses to corresponding numeric and text labels based on predefined special cases and mappings defined in a loaded survey key. This function also handles survey responses that fall outside the predefined cases by attempting to fetch mappings from the loaded survey data.
> Parameters: <input_data>: DataFrame containing survey responses with columns question_concept_id and answer_concept_id. 
> 
> Returns: The modified DataFrame with added columns answer_numeric and answer_text containing the mapped values.
>
>**create_dummies(input_data)**: create_dummies(user_data)
Transforms survey data to include dummy variables for questions that allow multiple answers. Each response is converted into a separate row with a unique identifier, allowing for easier analysis in statistical software. 
> 
> Parameters: <user_data>: DataFrame containing survey responses with columns question_concept_id and answer_concept_id. 
> 
> Returns: A new DataFrame with additional rows for select-all-that-apply questions, properly formatted for further analysis.
> 
>**scale(data, variables, scale_name)**: Transforms responses from "select all that apply" questions in a survey dataset into individual rows for each selected answer. This function utilizes a preloaded question_key integrated within the package, which includes a select_all flag to identify questions that allow multiple answers. 
> 
> Upon execution, the function identifies all "select all that apply" questions based on the select_all flag from the question_key. For each response to these questions in the user_data DataFrame, it creates a new row, modifying the question_concept_id to append the answer_concept_id. This adjustment effectively treats each answer as a unique sub-question, allowing for detailed data analysis of multi-select responses.
> 
> The function then removes the original rows corresponding to "select all" questions to prevent data redundancy. 
> 
## pivot_data.py

>
>**pivot(filename)**: Pivots a dataset to structure numeric survey responses in a wide format. The function checks if the specified file exists; if not, it prints an error message and returns. It reads the data from the file into a DataFrame, then pivots this DataFrame so that each row represents a respondent and each column represents a question, with cells containing the numeric answers. 
>
>The column names are prefixed with 'q' to denote question IDs. The pivoted DataFrame is then saved to a new CSV file with a filename prefixed by 'pivot_n_'. The function concludes by printing the name of the newly saved file.
>
>**pivot_text(filename)**: Similar to pivot_data_numeric, but pivots text responses instead. It processes and pivots the dataset to structure text survey responses in a wide format, follows the same file existence check, reading, and pivoting process, but focuses on answer_text values. The output file is named with a 'pivot_t_' prefix, and the function notifies the user of the successfully saved file.
>

## recode_missing.py
>
>**recode(input_data)**: Recodes missing values in a dataset with NaN (Not a Number). This function supports both CSV and Excel files. It identifies missing values based on a predefined list ([-999,..., -980]) and uses pandas to read the file, recoding occurrences of these values with NaN. The function raises a ValueError if the input file is not in one of the supported formats.
>

## codebooks.py
>
>**codebook(df)**: Generates a codebook from a DataFrame containing survey data. The function selects relevant columns (question_concept_id, question, answer_concept_id, answer_numeric, answer_text), removes duplicates, and sorts the entries by question_concept_id to create the codebook DataFrame. This DataFrame is returned for further use or inspection.
>
>**print_codebook(codebook_df)**: Prints the provided codebook DataFrame in a readable format. It attempts to use the tabulate library to print the DataFrame with headers, formatted as an SQL-style table. If tabulate is not installed, it falls back to pandas' built-in printing options, adjusting the display settings to ensure that all data is visible without truncation. This function is useful for displaying the codebook in a terminal or other environments where a visual representation of the DataFrame is beneficial.