# pcc - Physical Controller Connector for Maya

## 推奨ハードウェア
KORG [nanoKONTROL2](http://www.korg.com/jp/products/computergear/nanokontrol2/)
ですが、いわゆるMIDIフェーダーであれば何でも使えるはずです。

## Recommendation hardware
[KORG nanoKONTROL2](http://www.korg.com/jp/products/computergear/nanokontrol2/)

## インストール
1. [node.js](https://nodejs.org/)をインストール。
2. pccリポジトリをクローンするか、zipでダウンロード。
3. pccディレクトリに移動し、`npm install`を実行。
4. PhysicalControllerConnector.pyを、Mayaのpythonパスの通った場所にコピー。
5. Mayaを起動し、pcc_launch.pyをシェルフに登録。

## Installation
1. Install [node.js](https://nodejs.org/)
2. Clone or download this repository.
3. Go to pcc directory then `npm install`
4. Copy PhysicalControllerConnector.py to your Maya python script directory.
5. Launch Maya and add pcc_launch.py to shelf.

## Setup for KORG nanoKontrol2
1. Install the driver and editor.
2. Transfer the nanoKONTROL2.nktrl2_data in pcc directory.

## How to use
1. Click pcc_launch.py
2. Go to pcc directory then `node sender.js`


## Parameter specification
|Track|CC|Connect|Scale|Offset|Attr Initial|Attribute|
|-----|--|-------|-----|------|------------|---------|
|1 - 4|see below|0: off / 1:on|Scale for slider value|Offset slider 'zero' point|Attr Initial Value|Attribute name|
|1    |1 |1      |1    |0.5   |0           |pCube1.tx|
|1    |2 |1      |1    |0.5   |0           |pCube1.tx|
|1    |3 |1      |1    |0.5   |0           |pCube1.tx|
|1    |4 |1      |360  |0.5   |0           |pCube1.rx|
|1    |5 |1      |360  |0.5   |0           |pCube1.rx|
|1    |6 |1      |360  |0.5   |0           |pCube1.rx|
|2    |1 |1      |10   |0.5   |1           |pCube1.rx|
|2    |2 |1      |10   |0.5   |1           |pCube1.rx|
|2    |3 |1      |10   |0.5   |1           |pCube1.rx|
