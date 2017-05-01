# pcc - Physical Controller Connector for Maya

## 推奨ハードウェア
KORG [nanoKONTROL2](http://www.korg.com/jp/products/computergear/nanokontrol2/)
ですが、いわゆるMIDIフェーダーであれば何でも使えるはずです。

## インストール
1. [node.js](https://nodejs.org/)をインストール。
2. pccリポジトリをクローンするか、zipでダウンロード。
3. pccディレクトリに移動し、`npm install`を実行。
4. PhysicalControllerConnector.pyを、Mayaのpythonパスの通った場所にコピー。
5. Mayaを起動し、pcc_launch.pyをシェルフに登録。

## KORG nanoKONTROL2のセットアップ
1. KORG nanoKONTROL2用の[ドライバーとエディター](http://www.korg.com/jp/support/download/product/0/159/#software)をインストールします。
2. pccディレクトリの中にある、nanoKONTROL2.nktrl2_dataを転送します。

## 使い方
1. Mayaを起動し、シェルフに登録したpcc_launch.pyをクリックします。
2. コマンドプロンプトでpccディレクトリに移動し、`node sender.js`と打ち込んで実行します。

## Recommendation hardware
[KORG nanoKONTROL2](http://www.korg.com/jp/products/computergear/nanokontrol2/) or any MIDI faders.

## Installation
1. Install [node.js](https://nodejs.org/)
2. Clone or download this repository.
3. Go to pcc directory then `npm install`
4. Copy PhysicalControllerConnector.py to your Maya python script directory.
5. Launch Maya and add pcc_launch.py to shelf.

## Setup for KORG nanoKontrol2
1. Install the [driver and editor](http://www.korg.com/jp/support/download/product/0/159/#software) for the nanoKONTROL2.
2. Transfer the nanoKONTROL2.nktrl2_data in pcc directory.

## How to use
1. Launch Maya then click pcc_launch.py in the shelf.
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
