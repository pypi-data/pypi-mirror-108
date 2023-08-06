import pandas as pd
import numpy as np

def spearman_cor(embed):
    # Load simlex words
    df = pd.read_excel('data/SimLex-999.xlsx')
    word1 = list(df['word1'])
    word2 = list(df['word2'])
    simlex_words = set(word1 + word2)

    # Load trained embedding
    embed_words = list(embed.keys())
    embed_words = set(embed_words)

    # common words
    common_words = embed_words.intersection(simlex_words)

    # Compress simplex to only common words
    df1 = df.loc[(df['word1'].isin(common_words)) & (df['word2'].isin(common_words))]
    word1 = list(df1['word1'])
    word2 = list(df1['word2'])
    sim_index = list(df1['SimLex999'])

    # Calculate Cosine Simalirity
    cos_sim = []
    for a, b in zip(word1, word2):
        cos_sim.append(np.dot(embed[a], embed[b]) / (np.linalg.norm(embed[a]) * np.linalg.norm(embed[b])))

    # Calculate difference in ranks
    sim_index = -1 * np.array(sim_index)
    cos_sim = -1 * np.array(cos_sim)
    emb_rank = np.argsort(cos_sim)
    sim_rank = np.argsort(sim_index)
    distance = abs(emb_rank - sim_rank)

    # Calculate spearman correlation
    n = len(distance)
    rho = 1 - 6 * np.sum(np.square(distance)) / (n * (n ** 2 - 1))
    return rho
