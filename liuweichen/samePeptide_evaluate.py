import os
import sys
import joblib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import scipy.sparse as ss
import seaborn as sns

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialize logging.
from gleams import logger as glogger
glogger.init()
from gleams import rndm
rndm.set_seeds()


import logging
logger = logging.getLogger('gleams')
logger.setLevel(logging.DEBUG)

# Plot styling.
plt.style.use(['seaborn-white', 'seaborn-paper'])
plt.rc('font', family='serif')
sns.set_palette(['#9e0059', '#6da7de', '#ee266d', '#dee000', '#eb861e'])
sns.set_context('paper', font_scale=1.3)    # Single-column figure.

metadata = pd.read_parquet(os.path.join('/nvme/liuweichen/data_test',
                                        'cluster','embed_GLEAMS.parquet'))[['dataset', 'filename', 'scan','sequence','charge']].dropna(subset=['sequence'])
metadata['sequence'] = metadata['sequence'].str.replace('I','L')

num_samples = min(10_000_000, len(metadata))
idx_sample = np.random.choice(metadata.index, num_samples, False) # 从metadata的序列号中抽出num_samples个数，且抽出后不放回
metadata = metadata.loc[idx_sample]

pairwise_distances = ss.load_npz(os.path.join('/nvme/liuweichen/data_test', 'cluster','dist_GLEAMS.npz'))
pairwise_distances = pairwise_distances[metadata.index][:, metadata.index]
logger.info('Using %d non-zero pairwise distances between %d randomly '
            'selected embeddings', pairwise_distances.count_nonzero(),len(metadata))

logger.info('Verify whether neighbors have the same peptide label')
rows, columns, dist = ss.find(pairwise_distances)
sequences = ((metadata['sequence'] + '/' + metadata['charge'].astype(str))
             .reset_index(drop=True))
same_label = (sequences.loc[rows].reset_index(drop=True) ==
              sequences.loc[columns].reset_index(drop=True))
order = np.argsort(dist)  # 元素从小到大排列，提取其在排列前对应的index(索引)输出
dist = np.asarray(dist)[order]
same_label = np.asarray(same_label)[order]
prop_same_label = np.cumsum(same_label) / np.arange(1, len(same_label) + 1)

joblib.dump([dist, prop_same_label], 'nn_dist.joblib')

width = 7
height = width / 1.618    # golden ratio
fig, ax = plt.subplots(figsize=(width, height))
max_dist = 0.5
mask = dist < max_dist
ax.plot(dist[mask], prop_same_label[mask], label='Original')
ax.set_xlim(0, max_dist)
ax.set_ylim(0.95, 1)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.legend(loc='lower left')
ax.set_xlabel('Embedded distance')
ax.set_ylabel('Proportion same peptide')
sns.despine()
plt.savefig('nn_dist.png', dpi=300, bbox_inches='tight')
logging.shutdown()


