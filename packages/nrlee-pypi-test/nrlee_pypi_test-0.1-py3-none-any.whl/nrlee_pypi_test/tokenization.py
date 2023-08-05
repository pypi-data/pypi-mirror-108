from pynori.korean_analyzer import KoreanAnalyzer

def tokenization_with_pynori():
  nori = KoreanAnalyzer(decompound_mode='DISCARD',
                        infl_decompound_mode='DISCARD',
                        discard_punctuation=True,
                        output_unknown_unigrams=False,
                        pos_filter=False, stop_tags=['JKS', 'JKB', 'VV', 'EF'],
                        synonym_filter=False, mode_synonym='NORM')
  print(nori.do_analysis("화이트라운드반팔티셔츠"))
