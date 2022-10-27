# %%
from email.policy import default
import re
import time
import streamlit as st
from collections import Counter
from pprint import pprint

# %%


def words(text): return re.findall(r'\w+', text.lower())


word_count = Counter(words(open('big.txt', encoding="utf-8").read()))
N = sum(word_count.values())
def P(word): return word_count[word] / N  # float


letters = 'abcdefghijklmnopqrstuvwxyz'

# %%


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def correction(word):
    return max(candidates(word), key=P)


def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words):
    return set(w for w in words if w in word_count)


def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in word_count)


# %%
# optionss = []
# optionss.append(None)
# for i in word_count.keys():
#     optionss.append(i)    
st.title("Spellchecker")
the_word = st.selectbox("Choose a word:", word_count.keys())

st.write("or")
the_word = st.text_input("Type your own:", value=the_word)
with st.sidebar:
    show = st.checkbox("show original word")
if show:
    st.write("original word:", the_word)
w = correction(the_word)
if the_word == w:
    st.success(the_word + " is the correct spelling")
else:
    st.error("Correction: " + w)
