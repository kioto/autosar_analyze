# autosar_analyze
Analyzing AUTOSAR specification

shとpython3で書いてます。

## AUTOSARのPDFファイルをダウンロード

get_autosar_pdf.sh

AUTOSAR 4.2.2のPDFをダウンロードする。

## SRS解析（５章のみ）

* Acrobat Readerでテキスト化＋UTF-8変換済みテキストファイルが前提
（PythonでPDF->Text変換を色々やってみたけど、できたテキストはあんまり扱いやすくなかった）
* AUTOSAR_SRS_*.txtを食わせると、５章の表の情報を取り出してCSV形式で表示
* 表の中の表のデータ取得は期待しないで
