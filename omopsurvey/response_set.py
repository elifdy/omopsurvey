import pandas as pd
import os


def load_survey_data(filename='survey_key.csv'):
    current_dir = os.path.dirname(os.path.realpath(__file__))

    file_path = os.path.join(current_dir, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path {file_path} does not exist.")
    return pd.read_csv(file_path)


def map_responses(input_data):
    special_cases = {
        903087: (-999, "Don't Know"),
        903096: (-998, "Skip"),
        903072: (-997, "Does Not Apply To Me"),
        903079: (-996, "Prefer Not To Answer"),
        903070: (-995, "Other"),
        903092: (-994, "Not Sure"),
        903095: (-993, "None"),
        903103: (-992, "Unanswered"),
        40192432: (-991, "I am not religious"),
        40192487: (-990, "I do not believe in God (or a higher power)"),
        40192520: (-989, "Does not apply to my neighborhood"),
        903081: (-988, "Free Text"),
        596889: (998, "Text"),
        596883: (-994, "Not Sure"),
        1332844: (-994, "Not Sure"),
        903598: (-996, "Prefer Not To Answer"),
        903596: (-996, "Prefer Not To Answer"),
        903601: (-996, "Prefer Not To Answer"),
        903607: (-996, "Prefer Not To Answer"),
        903610: (-996, "Prefer Not To Answer"),
        903604: (-996, "Prefer Not To Answer"),
        43529089: (-997, "No Blood Related Daughters"),
        43529086: (-997, "No Blood Related Siblings"),
        43529092: (-997, "No Blood Related Sons"),
        43529090: (-997, "No Daughters Related")
    }
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
        if answer_id in special_cases:
            input_data.at[idx, 'answer_numeric'], input_data.at[idx, 'answer_text'] = special_cases[answer_id]
        else:
            input_data.at[idx, 'answer_numeric'] = mapping_numeric.get(question_id, {}).get(answer_id, None)
            input_data.at[idx, 'answer_text'] = mapping_text.get(question_id, {}).get(answer_id, None)

        if pd.isna(answer_id) and pd.notna(row['answer']) and str(row['answer']).isdigit():
            input_data.at[idx, 'answer_numeric'] = int(row['answer'])
            input_data.at[idx, 'answer_text'] = str(row['answer'])

        if isinstance(input_data.at[idx, 'answer_text'], (int, float)):
            input_data.at[idx, 'answer_text'] = str(input_data.at[idx, 'answer_text'])

        # if isinstance(input_data.at[idx, 'answer_text'], (int, float)):
        #     input_data.at[idx, 'answer_text'] = str(input_data.at[idx, 'answer_text'])
        # elif isinstance(input_data.at[idx, 'answer_text'], str) and input_data.at[idx, 'answer_text'].isdigit():
        #     pass

    return input_data


def create_dummies(user_data):
    question_key = load_survey_data()

    data = user_data.merge(question_key[['question_concept_id', 'select_all']], on='question_concept_id', how='left')

    select_all_questions = question_key[question_key['select_all'] == 1]['question_concept_id'].unique()

    select_all_data = data[data['question_concept_id'].isin(select_all_questions)]

    for question_id in select_all_questions:
        current_question_data = select_all_data[select_all_data['question_concept_id'] == question_id]
        dummies = pd.get_dummies(current_question_data['answer_text']).add_prefix(f'{question_id}_')
        data = data.join(dummies, how='left', rsuffix='_dummy')
    data.drop(select_all_data.index, inplace=True)
    data.drop(columns=['select_all'], inplace=True)

    return data
