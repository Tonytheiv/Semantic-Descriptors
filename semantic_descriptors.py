import math as m


def build_semantic_descriptors(sentences):
    res = {}
    for sentence in sentences:
        memory1 = set()
        for word in sentence:
            if word not in memory1:
                if word not in res:
                    res[word] = {}
                memory2 = set()
                memory1.add(word)
                for remaining_word in sentence:
                    if (remaining_word is not word) and (remaining_word not in memory2):
                        if remaining_word in res[word]:
                            res[word][remaining_word] += 1
                        else:
                            res[word][remaining_word] = 1
                        memory2.add(remaining_word)
    return res


def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for name in filenames:
        master = open(name, "r", encoding="latin1").read().lower()
        master = master.replace(",", " ").replace("--", " ").replace("-", " ").replace(":", " ").replace(";", " ")
        master = master.replace("!", ".").replace("? ", ".").split(".")
        for text in master:
            sentences.append(text.split())
    return build_semantic_descriptors(sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    mem_score = 0.0
    mem_word = None
    for words in choices:
        if (word and words) in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[words])
            if similarity > mem_score or similarity == 0.0:
                mem_score = similarity
                mem_word = words
        else:
            mem_score = -1.0
    return mem_word


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    questions = []
    res = []
    num_correct = 0.0
    master = open(filename, "r", encoding="latin1").read().split("\n")
    for question in range(len(master)):
        questions.append(master[question])
        res.append(questions[question].split(" "))
    for words in res:
        if most_similar_word(words[0], words[2:], semantic_descriptors, similarity_fn) == words[1]:
            num_correct += 1
    return num_correct*100/(len(res))


def cosine_similarity(vec1, vec2):
    res, v1abs, v2abs = 0.0, 0.0, 0.0
    for key in vec1:
        if key not in vec2:
            vec2[key] = 0
    for key2 in vec2:
        if key2 not in vec1:
            vec1[key2] = 0
    for keys in vec1:
        res += vec1[keys] * vec2[keys]
        v1abs += vec1[keys] ** 2
        v2abs += vec2[keys] ** 2
    return res/(m.sqrt(v1abs) * m.sqrt(v2abs))
