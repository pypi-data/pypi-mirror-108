import os.path
import shutil
from io import StringIO

import numpy as np
import pandas as pd

from ludwig.experiment import full_experiment
from ludwig.predict import full_predict


# function to generate sequence data like this
#         in_seq            out_seq
#          a b c              b c d
#        e a b d            a b c e
#      b b e e a          c c a a b
def generate_tagger_sequence(min_seq_size=5, max_seq_size=5, num_records=100):
    in_vocab = list("abcde")
    mapping_dict = {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e', 'e': 'a'}

    def generate_output(x):
        letter = x[0]
        repeat = int(x[1])
        return ' '.join(repeat * letter)

    input_list = []
    output_list = []
    for _ in range(num_records):
        n = np.random.randint(min_seq_size, max_seq_size + 1, 1)
        input_seq = np.random.choice(in_vocab, n, replace=True)
        output_seq = [mapping_dict[x] for x in input_seq]
        input_list.append(' '.join(input_seq))
        output_list.append(' '.join(output_seq))

    train = {
        'in_seq': input_list,
        'out_seq': output_list
    }

    return pd.DataFrame(train)


def dump_key(parms, keys):
    return [key + ": " + str(parms[key]) for key in keys]


shutil.rmtree('./data_to_pred', ignore_errors=True)
os.mkdir('./data_to_pred')
shutil.rmtree('./results', ignore_errors=True)
shutil.rmtree('./results_0', ignore_errors=True)
shutil.rmtree('./results_1', ignore_errors=True)

# From TF1 unit test_experiment.py::test_experiment.py::test_experiment_attention
input_features = [
    {'name': 'in_seq', 'type': 'sequence', 'encoder': 'rnn',
     'cell_type': 'rnn',
     'reduce_output': None}
]
output_features = [
    {'name': 'out_seq', 'type': 'sequence',
     'decoder': 'tagger',
     'reduce_input': None
     }
]

config = {
    'input_features': input_features,
    'output_features': output_features,
    'combiner': {
        'type': 'concat',  # 'concat'
        'fc_size': 14
    },
    'training': {'epochs': 15, 'early_stop': 5}
}

args = {
    'config': config,
    'skip_save_processed_input': True,
    'skip_save_progress': True,
    'skip_save_unprocessed_output': True,
    'skip_save_model': False,
    'skip_save_log': False,
    'debug': False
}

np.random.seed(31)  # 13
data_df = generate_tagger_sequence(3, 10, 2000)
test_df = generate_tagger_sequence(3, 10, 1000)

exp_dir_name = full_experiment(data_df=data_df, **args)

data_df.to_csv('./data_to_pred/train.csv', index=False)

full_predict(
    './results/experiment_run/model',
    data_csv='./data_to_pred/train.csv',
    evaluate_performance=True)

# separate test data set
print(test_df.head(20))
test_df.to_csv('./data_to_pred/my_data.csv', index=False)
full_predict(
    './results/experiment_run/model',
    data_csv='./data_to_pred/my_data.csv',
    evaluate_performance=False)

# check for spurious 0s
# read in predictions
# df = pd.read_csv('./results_1/out_seq_predictions.csv', header=None)
with open('./results_1/out_seq_predictions.csv', 'r') as f:
    buffer = f.read()
buffer = buffer.replace(',', ' ').replace('<PAD>', '-')
df2 = pd.read_csv(StringIO(buffer), header=None)
df2.columns = ['predicted_sequence']

number_predictions = df2['predicted_sequence'].shape[0]
ind_without_end_pad = df2['predicted_sequence'].apply(
    lambda x: False if x[-1] == '-' else True)
number_missing_end_pad = np.sum(ind_without_end_pad)
number_tokens = df2['predicted_sequence'].str.replace(' ', '').str.len()
number_pads = df2['predicted_sequence'].str.count('-')
ind_multiple_pads = number_pads > 1
number_multiple_pads = np.sum(ind_multiple_pads)

try:
    assert not np.any(ind_multiple_pads) and not np.any(ind_without_end_pad)
    print("No spurious 0s or missing 0s")
except AssertionError:
    print("ISSUES FOUND!!!!!!")
    print("number of rows with issues:\n",
          "\tmissing end pads:", number_missing_end_pad, "out of",
          number_predictions, "\n",
          "\tmultiple pads:", number_multiple_pads, "out of",
          number_predictions, "\n"
          )

df2_last = pd.read_csv('./results_1/out_seq_last_predictions.csv', header=None)
df2_last.columns = ['predicted_last']
df3 = pd.concat([test_df, df2, df2_last], axis=1)
pd.options.display.width = None
pd.options.display.max_colwidth = None

print('config:')
print("input features:", dump_key(input_features[0], ['encoder', 'cell_type']))
print("output features", dump_key(output_features[0], ['decoder']))
print('training:',
      dump_key(config['training'], ['epochs', 'early_stop']))
print("\nRandom sample of predicted sequences:")
print(df3.sample(n=15, random_state=33))

if number_missing_end_pad > 0:
    print("\n\nsample without end pads:")
    print(df3.loc[ind_without_end_pad].head(10))

if number_multiple_pads > 0:
    print("\n\nsample multiple pads:")
    print(df3.loc[ind_multiple_pads].head(10))
