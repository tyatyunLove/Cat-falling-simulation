# 猫ひねりシミュレーション（Cat Righting Reflex Simulation）

これは、猫が自由落下中に体をひねって着地姿勢を整える「猫ひねり現象（cat righting reflex）」を、物理モデルに基づいてシミュレーションするPythonプログラムです。

## プロジェクト概要

- 角運動量保存則に基づき、猫の体を2つの剛体に分けて回転運動を解析
- VPythonによる可視化で3ステップのひねり動作をアニメーション表示

## 使用技術

- Python 3.x
- NumPy
- SciPy
- Matplotlib
- VPython（3D可視化）

## ファイル構成
- README.md
- catfallingsimulation.py(体重と慎重を入力するとそのねこのひねりを可視化する)
- findingalphabeta.py(前屈と後屈の関係のグラフ)
- turningratio.py(曲げ角度と猫ひねり率の関係のグラフ)

  
