import pandas as pd
import os


def pivot_data_numeric(data):

    pivot_df = data.pivot_table(index='respondent_id',
                                columns='question_concept_id',
                                values='answer_numeric',
                                aggfunc='first')

    pivot_df.columns = ['q' + str(col) for col in pivot_df.columns]
    dir_name = os.path.dirname(data)
    new_filename = 'pivot_n_' + os.path.basename(data)
    new_filepath = os.path.join(dir_name, new_filename)
    pivot_df.to_csv(new_filepath)

    print(f"Pivoted dataset with numeric values saved as: {new_filepath}")


def pivot_data_text(data):

    pivot_df = data.pivot_table(index='respondent_id',
                                columns='question_concept_id',
                                values='answer_text',
                                aggfunc='first')

    pivot_df.columns = ['q' + str(col) for col in pivot_df.columns]
    dir_name = os.path.dirname(data)
    new_filename = 'pivot_t_' + os.path.basename(data)
    new_filepath = os.path.join(dir_name, new_filename)
    pivot_df.to_csv(new_filepath)

    print(f"Pivoted dataset with text values saved as: {new_filename}")

