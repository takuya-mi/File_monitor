# File_monitor

指定したディレクトリをサブプロセスで監視し、一定時間ごとにファイル数を取得する。監視中、ファイル数が複数回に渡って変化しなかった場合、実行中のプロセスが正常終了したか、または何らかのエラーで停止したと判断する。  
この際、指定された宛先にメールを送信する。メールの宛先は `config.yaml`をディレクトリに追加して指定する。 

---

**<config.ymal>**   

      server_info:  
        SMTP_HOST: '*'  
        SMTP_PORT: *  
        FROM_ADDRESS: '*'  
        USER_NAME: '*'  
        PASSWORD: '*'  
      
      receiver_info:  
        TO_ADDRESS: '*'  
        CC_ADDRESS: ''  
        BCC_ADDRESS: ''  
  
---

また、FileObserverを直接呼び出せば、GUIを使用せずに監視が可能である。メインプロセスとは完全に独立して実行されるので、呼び出し元が停止しても動作する。  


## 使い方

1. **`gui.py` を実行する**  
   プログラムのユーザーインターフェースを起動する。

**<２から６は繰り返し利用可>**

2. **インターバルを分単位で指定する**  
   ディレクトリ内のファイル数を取得する間隔を分単位で設定する。（小数可）

3. **カウント回数を整数で指定する**  
   ファイル数が変化しない回数の閾値を指定する。

4. **対象の機器を指定する**  
   機器の名前を入力する。（例：`XAFS`）

5. **スクリーンショットを撮影するか否かを指定する**  
   どちらかのラジオボタンを選択する。

6. **監視を開始する**  
   startボタンを押して、監視プロセスを実行する。(メール送信後、監視プロセスは自動的に停止する)

7. **監視を停止する**  
   途中で監視をやめたい場合、stopボタンを押して、監視プロセスを停止する。



   

---
