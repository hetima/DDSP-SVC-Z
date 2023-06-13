# DDSP-SVC-Z

[DDSP-SVC](https://github.com/yxlllc/DDSP-SVC)を使いやすくするスクリプトです。

InquirerPyが必要です。

```
pip install inquirerpy
```

## z_main_diff.py
main_diff.pyを簡略化したコマンドです。DDSP-SVCのフォルダ内に配置してください（カレントディレクトリがDDSP-SVCであれば他の場所に置いても動きます）。引数なしで実行します。

```
python z_main_diff.py
```

モデルを一覧から選んでwavファイルを指定（ドラッグ＆ドロップ）するだけで推論を開始します。結果は入力したwavファイルと同じ場所に「モデル名-元ファイル名(-連番).wav」という名前で生成されます。

モデルは `exp/モデル名` というフォルダ構成で、その中に `combsub` と `diff` というフォルダ名で学習されたものが対象です。最大数値のptファイルが使われます。

```
exp
 ├model1
 └model2
   ├combsub
   │ ├config.yaml
   │ ├...
   │ └model_xxxx.pt
   └diff
      ├config.yaml
      ├...
      └model_xxxx.pt
```

