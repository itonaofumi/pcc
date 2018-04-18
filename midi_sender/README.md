# How to build midi_sender app
Need node.js and Electron.
node.jsとElectronが必要です。

Install node.js, electron and electron-packager.
node.jsをインストールし、pccディレクトリで以下のコマンドを実行。
```
npm i -D electron
npm i -D electron-packager
```

test
テスト実行
```
npx electron midi_sender
```

check electron version
エレクトロンのバージョン確認
```
npx electron -v
```

make package
パッケージ作成
```
npx electron-packager midi_sender MidiSenderApp --platform=win32 --arch=x64 --electron-version=1.8.4 --overwrite
```
