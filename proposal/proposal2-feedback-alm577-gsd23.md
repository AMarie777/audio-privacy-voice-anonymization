# CS 1657 P2 Proposal Feedback

__Group:__ Gabexa-Proj2

__Names:__ Diaz, Gabriela; Mckee, Alexa

__Users:__ gsd23; alm577

## Comments

### Technical depth

I like that you gave yourself enough flexibility to expand the technical depth
if needed. There could be a lot of different audio transformations to try,
including combinations of them. Your comparison metric, cosine similarity, can
also be expanded or supplemented. I think it would be worth trying some other
measures as well. For instance, can you download a model that you can train to
classify your voice, and then see if it still classifies you correctly after
changes to the audio? Can you record a clip of yourselves saying “Hey Google” or
“Hey Siri,” and then see which transformations prevent it from being recognized
while still sounding understandable?

To measure whether an audio transformation preserves privacy while still being
comprehensible, perhaps you’re looking for something like: Speaker recognition
has low accuracy, but machine transcription still has high accuracy.

### Topic relevance

Very relevant to privacy and the prompt.

### Support of goals

Well-justified support of goals.

## Overall

Really interesting idea! I’ve wondered at times about the “anonymous voice” and
whether it really provides any anonymity, since it seems like it primarily
relies on shifting the tone downward… isn’t that easily reversible by shifting
back up? It might be interesting in your work to consider which transformations
are and aren’t easily reversible, in addition to gauging which prevent
identification.

Here is a survey paper (a paper which summarizes prior research) of different
models for speaker recognition:
https://ieeexplore.ieee.org/abstract/document/9074184

