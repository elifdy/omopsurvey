import pandas as pd
import os


def load_survey_data(filename='survey_healthcare.csv'):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(current_dir, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    return pd.read_csv(file_path)


def map_responses(input_data):
    survey_data = load_survey_data()

    mapping_numeric = survey_data.groupby('question_concept_id').apply(
        lambda x: dict(zip(x['answer_concept_id'], x['answer_numeric']))).to_dict()

    mapping_text = survey_data.groupby('question_concept_id').apply(
        lambda x: dict(zip(x['answer_concept_id'], x['answer_text'].str.strip()))).to_dict()

    input_data['answer_numeric'] = None
    input_data['answer_text'] = None

    for idx, row in input_data.iterrows():
        question_id = row['question_concept_id']
        answer_id = row['answer_concept_id']

        input_data.at[idx, 'answer_numeric'] = mapping_numeric.get(question_id, {}).get(answer_id, None)
        input_data.at[idx, 'answer_text'] = mapping_text.get(question_id, {}).get(answer_id, None)

        if isinstance(input_data.at[idx, 'answer_text'], (int, float)):
            input_data.at[idx, 'answer_text'] = str(input_data.at[idx, 'answer_text'])
        elif isinstance(input_data.at[idx, 'answer_text'], str) and input_data.at[idx, 'answer_text'].isdigit():
            pass

    return input_data
