import pandas as pd


def load_data(source):
    if isinstance(source, pd.DataFrame):
        return source
    elif isinstance(source, str):
        if source.endswith('.csv'):
            return pd.read_csv(source)
        elif source.endswith('.txt'):
            return pd.read_csv(source, delimiter='\t')
        elif source.endswith('.xlsx'):
            return pd.read_excel(source)
        else:
            raise ValueError("Unsupported file type provided.")
    else:
        raise TypeError("Input source must be a pandas DataFrame or a filepath as a string.")


def create_codebook(dataframe):

    required_columns = ['question_concept_id', 'question']
    response_columns = ['answer_concept_id', 'answer', 'answer_text', 'answer_numeric']

    response_columns = [col for col in response_columns if col in dataframe.columns]

    if not all(col in dataframe.columns for col in required_columns):
        raise ValueError("Dataframe must contain the necessary columns: 'question_concept_id' and 'question'.")

    dataframe['question_concept_id'] = dataframe['question_concept_id'].astype(str)

    grouped = dataframe.groupby(required_columns).apply(
        lambda x: x[response_columns].drop_duplicates().reset_index(drop=True)
    )

    codebook_df = grouped.reset_index(drop=False)

    codebook_df = codebook_df[required_columns + response_columns].drop_duplicates()

    return codebook_df


def generate_codebook(source):

    try:

        data = load_data(source)

        codebook_df = create_codebook(data)

        return codebook_df
    except ImportError:
        print("Required module not installed.")
    except Exception as e:
        print(f"Error: {e}")


def print_codebook(source):

    try:

        data = load_data(source)

        codebook_df = create_codebook(data)

        from tabulate import tabulate
        print(tabulate(codebook_df, headers='keys', tablefmt='psql', showindex=False))
    except ImportError:
        print("Tabulate module not installed, using default print.")
        print(codebook_df)
    except Exception as e:
        print(f"Error: {e}")


def create_formatted_codebook(dataframe):

    dataframe['question'] = dataframe['question'].str.strip().str.lower()
    dataframe['answer'] = dataframe['answer'].str.strip().str.lower()

    dataframe = dataframe.drop_duplicates(subset=['question_concept_id', 'question', 'answer_concept_id'])

    grouped = dataframe.groupby(['question_concept_id', 'question'], sort=False)

    formatted_data = []

    for (question_concept_id, question), group in grouped:
        is_first = True

        for idx, row in group.iterrows():
            if is_first:
                formatted_data.append({
                    'question_concept_id': question_concept_id,
                    'question': question,
                    'answer_concept_id': row['answer_concept_id'],
                    'answer_concept_id recoded as answer_numeric': row['answer_numeric'],
                    'answer': row['answer'],
                    'answer recoded as answer_text': row['answer_text']
                })
                is_first = False
            else:
                formatted_data.append({
                    'question_concept_id': '',
                    'question': '',
                    'answer_concept_id': row['answer_concept_id'],
                    'answer_concept_id recoded as answer_numeric': row['answer_numeric'],
                    'answer': row['answer'],
                    'answer recoded as answer_text': row['answer_text']
                })

    formatted_codebook_df = pd.DataFrame(formatted_data)

    return formatted_codebook_df.to_html(index=False, escape=False)