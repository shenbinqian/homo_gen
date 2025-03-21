# Automatic Generation of Chinese Homophone Words

This repository contains the code and data to generate Chinese homophone words to probe machine translation evaluation systems for our paper [Automatically Generating Chinese Homophone Words to Probe Machine Translation Estimation Systems](https://arxiv.org/abs/2503.16158) accepted by the 10th Workshop on Noisy and User-generated Text (W-NUT) at NAACL 2025. Our method using self-information achieves much higher correlation with human preferences than an existing method proposed by Hiruncharoenvate et al. (2015). These generated homophone words can be used for censorship avoidance or as what we show, creating data perturbations to probe the robustness of MT or MT evaluation systems.


## Installation

Please clone our repository and install the following dependencies. 

```
pip install jieba pandas pypinyin numpy torch transformers
```

Pytorch and transormers are used to run language models to get self-information scores, which is the method (the last step) we propose to filter all possible homophone candidates. If you are restricted with GPUs or you just want to generate all homophones without filtering, this step is not necessary.

## Optional Step 0 to Prepare Weibo Corpus

This step is to prepare the Weibo corpus $D$ to get a frequency list as both our method and the baseline are based on frequency. Since $D$ is provided in the [weibo_char_freq.json](https://github.com/surrey-nlp/homo_gen/blob/main/weibo_char_freq.json) file, this step is optional for replicating our results. However, you can run the following command on your own databases.

```
python preprocessing.py
```

## Step 1 Homophone Generation

Once the corpus is prepared, run the following code to generate all possible homophones and the top-k homophones filtered using the baseline method proposed by Hiruncharoenvate et al. (2015). The generator uses the file [extracted_keywords.xlsx](https://github.com/surrey-nlp/homo_gen/blob/main/extracted_keywords.xlsx) which contains translation error words discovered by [Qian et al. (2023)](https://aclanthology.org/2023.eamt-1.13/). You can replace this file with your own words that need homophone substitution.

```
python generator.py
```

## Step 2 Pick Frequent Translation Error Words and Frequent Homophones

Pick most errorneous words in translation, and optionally filter homophone candidates based on frequency for getting self-information scores. To create your own data, you can run the following code. To replicate our results, you can skip this step and use the data in *freq_candidates* folder to get self-information scores in the next step.

```
python prepare4self_info.py
```

## Step 3 Get Self-information Scores

Check for which word you want to get self-information scores and run the following code.

```
python self_info.py
```

## Reference(s)

Chaya Hiruncharoenvate, Zhiyuan Lin, and Eric Gilbert. 2015. Algorithmically Bypassing Censorship on Sina Weibo with Nondeterministic Homophone Substitutions. In *Proceedings of the International AAAI Conference on Web and Social Media*, 9(1):150–158.

Shenbin Qian, Constantin Orasan, Felix Do Carmo, Qiuliang Li, and Diptesh Kanojia. 2023. Evaluation of Chinese-English Machine Translation of Emotion-Loaded Microblog Texts: A Human Annotated Dataset for the Quality Assessment of Emotion Translation. In *Proceedings of the 24th Annual Conference of the European Association for Machine Translation*, pages 125–135, Tampere, Finland. European Association for Machine Translation.