# pcc - Physical Controller Connector for Maya
![cubeTrans](http://itonaofumi.github.io/pcc/cubeTrans.gif)
![cubeRot](http://itonaofumi.github.io/pcc/cubeRot.gif)
![cubeScale](http://itonaofumi.github.io/pcc/cubeScale.gif)
![hand1](http://itonaofumi.github.io/pcc/hand1.gif)
![hand2](http://itonaofumi.github.io/pcc/hand2.gif)
![face](http://itonaofumi.github.io/pcc/face.gif)

## Recommendation hardware
[KORG nanoKONTROL2](http://www.korg.com/jp/products/computergear/nanokontrol2/) or any MIDI fader should be usable.

## Installation
1. Install [node.js](https://nodejs.org/)
2. Clone or [download](https://github.com/itonaofumi/pcc/archive/master.zip) this repository.
3. Go to pcc directory then `npm install`
4. Copy PhysicalControllerConnector.py to your Maya python script directory.
5. Launch Maya and add pcc_launch.py to shelf.

## Setup for KORG nanoKontrol2
1. Install the [driver and editor](http://www.korg.com/jp/support/download/product/0/159/#software) for the nanoKONTROL2.
2. Transfer the nanoKONTROL2.nktrl2_data in pcc directory.

## How to use
1. Launch Maya then click pcc_launcher.py in the shelf.
2. Go to pcc directory then `node sender.js`


## Parameter specification
|Track|CC|Connect|Scale|Offset(0.0 - 1.0)|Attr Initial|Attribute|
|-----|--|-------|-----|------|------------|---------|
|1 - 4|see below|0=off, 1=on|Scale for fader value|Zero position of fader|Attr Initial Value|Attribute name|

![pcc_table](http://itonaofumi.github.io/pcc/pcc_table.png)
![cc](http://itonaofumi.github.io/pcc/nanoKONTROL2CC.png)
![cc_spec](http://itonaofumi.github.io/pcc/nanoKONTROL2CC_specE.png)

## 推奨ハードウェア
KORG [nanoKONTROL2](http://www.korg.com/jp/products/computergear/nanokontrol2/)
ですが、いわゆるMIDIフェーダーであれば何でも使えるはずです。

## インストール
1. [node.js](https://nodejs.org/)をインストール。
2. pccリポジトリをクローンするか、zipで[ダウンロード](https://github.com/itonaofumi/pcc/archive/master.zip)。
3. pccディレクトリに移動し、`npm install`を実行。
4. PhysicalControllerConnector.pyを、Mayaのpythonパスの通った場所にコピー。
5. Mayaを起動し、pcc_launch.pyをシェルフに登録。

## KORG nanoKONTROL2のセットアップ
1. KORG nanoKONTROL2用の[ドライバーとエディター](http://www.korg.com/jp/support/download/product/0/159/#software)をインストールします。
2. pccディレクトリの中にある、nanoKONTROL2.nktrl2_dataを転送します。

## 使い方
1. Mayaを起動し、シェルフに登録したpcc_launcher.pyを実行。
2. コマンドプロンプトでpccディレクトリに移動し、`node sender.js`と打ち込んで実行。

## パラメーターについて
|Track|CC|Connect|Scale|Offset(0.0 - 1.0)|Attr Initial|Attribute|
|-----|--|-------|-----|------|------------|---------|
|1 - 4|下図参照|0=オフ, 1=オン|フェーダーの値をスケールします|フェーダーのどの位置を０とするか|アトリビュートの初期値|接続するアトリビュート|

![pcc_table](http://itonaofumi.github.io/pcc/pcc_table.png)
![cc](http://itonaofumi.github.io/pcc/nanoKONTROL2CC.png)
![cc_spec](http://itonaofumi.github.io/pcc/nanoKONTROL2CC_specJ.png)

## License
Copyright (c) 2017 Naofumi Ito

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
