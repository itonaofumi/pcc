# midi_senderアプリのビルドについて
node.jsとelectronが必要。

node.jsをインストールし、pccディレクトリで以下のコマンドを実行。
```
npm i -D electron
npm i -D electron-packager
```

テスト実行
```
npx electron midi_sender
```

バージョン確認
```
npx electron -v
```

パッケージ作成
```
npx electron-packager midi_sender MidiSenderApp --platform=win32 --arch=x64 --electron-version=1.8.4 --overwrite
```
