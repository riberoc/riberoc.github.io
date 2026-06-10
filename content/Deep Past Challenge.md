---
created: 2026-06-05T15:09
updated: 2026-06-06T14:19
tags:
  - publish
  - ai
publish: true
---

One of my most rewarding projects was the Kaggle Competition's Deep Past challenge. Our task was to build a model to translate Old Akkadian text into English. What made it so satisfying was the sheer difficulty and the creativity required at every step.

The main problem was data scarcity. We had very little parallel data, text with both Akkadian and English. This meant that we had to be very surgical with our decisions. We perform a literature review to find out what architectures could work well in this scenario as well as other techniques we could use. At the end, we opted for finetuning two pre-trained models known to perform well in low-resource settings, mBART and T5. Each with different architectures, allowing us the flexibility to compare approaches. 

Apart from the data scarcity, the quality of the data was another issue. The Akkadian text was transliterated from ancient clay tablets, which were not always in the best condition, meaning that some text was unrecoverable. On top of that, the tablets were not always transliterated in the same way, which introduced inconsistencies. It was essential to normalize the text to improve its quality. For example, unrecoverable text must always be labeled in the same way. We ended up building an extensive preprocessing pipeline to normalize these inconsistencies and removed sentences below a certain threshold of quality to avoid adding noise to the model. The language itself also presented unique linguistic challenges, which required us to learn an extra language to make the correct decisions (quite fun).

To compensate for the limited data, we developed augmentation strategies. One approach: swap proper nouns (names of people and places) across sentence pairs. Another: substitute nouns with semantically similar alternatives, for example, replacing "silver" with "gold".

Unfortunately, we didn't win, but reviewing the winning submissions showed that we were on the right track. The main difference was that the winners had a significantly stronger synthetic data pipeline that we didn't think of.

In this challenge we implemented many other features, but these were not mentioned to avoid making it too long. It was one of the most intellectually engaging challenges I have worked on. It required understanding the language, and every improvement felt earned. It was really fun.