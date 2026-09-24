# 概算要求 ingestion PoC

## 目的

MOF/RSのような統一CSVを前提にできない概算要求資料を、いきなりV2へ直結せず、

```text
source document
  -> adapter-specific extraction
  -> staging (rawに近い中間表現)
  -> canonical request records
  -> validation
  -> 将来 V2 Budget Item / System Entity へlink
```

という段階に分けて処理できるかを確認するPoC。

最初のgolden caseとして、令和6年度デジタル庁の

- 歳出概算要求書
- 「重要政策推進枠」要望一覧

を対象にしている。

## このPoCで確認したこと

1. 「係」を府省庁と決め打ちしない。
   - `厚生労働第1係` の下に `総務省システム` が存在するケースを正しく `総務省` と判定する。
2. 同じ金額をヘッダ・通常分・費目で重複SUMしない。
   - 金額のauthorityを `system_header -> component_sum -> expense_sum` の優先順位で決める。
3. 通常概算要求と重要政策推進枠を別record typeとして保持する。
4. page / source line / raw textをstagingに保持し、後から解釈ロジックを変更できるようにする。
5. 曖昧な行を無理に推定しない前提を置く。
6. 既知の総額をgolden validationとして使えることを確認する。

## 実行

依存パッケージなし。Node.jsのみ。

```bash
npm run poc
```

生成物:

```text
out/
  staging.jsonl
  request-normalized.jsonl
  systems.csv
  request-scopes.csv
  validation.json
  run-manifest.json
```

## PoC結果

現在のfixtureでは:

```text
staging records   25
normalized records 8
system records      5
scope records       3
validation          PASS
```

Golden:

```text
通常分                          448,267,326 千円
重要政策推進枠（システム関連） 118,772,628 千円
------------------------------------------------
実質概算要求                    567,039,954 千円
```

### 代表的な構造検証

`財務省システム` はシステムヘッダの要求額 102,935,743千円と、fixture内の通常分/特殊要因分の費目合計が一致する。

また、`厚生労働第1係` 配下の `総務省システム` は、周囲の係名ではなくシステム名から `総務省` と判定する。

これは今回の調査で判明した「係名 = 実際の府省庁とは限らない」をparserの回帰条件にしたもの。

## staging と normalized を分ける理由

### staging

できるだけsourceに忠実。

例:

```json
{
  "sourceDocumentId": "digital-r6-request-table-01",
  "sourcePage": 24,
  "sourceLine": 960,
  "recordKind": "expense",
  "rawText": "...",
  "groupLabel": "厚生労働第1係",
  "systemLabel": "総務省システム",
  "rawAmountsThousandYen": {
    "requestThousandYen": 200112
  }
}
```

sourceの読み方を後から修正しても、stagingを再利用できる。

### canonical / normalized

V2へつなぐための意味付きrecord。

```json
{
  "recordType": "request_system",
  "requestYear": 2023,
  "fiscalYear": 2024,
  "requestType": "normal",
  "budgetItem": "情報通信技術調達等適正・効率化推進費",
  "groupLabel": "厚生労働第1係",
  "systemLabel": "総務省システム",
  "ministryHint": "総務省",
  "requestYen": 200112000,
  "amountResolution": "expense_sum",
  "confidence": "high"
}
```

## 現時点では意図的にやっていないこと

- PDFそのもののdownload/extract
- 全32ページの完全parse
- 省庁ごとに異なるPDF/Excel形式への対応
- OCR
- system nameのfuzzy matching
- System Entityへの恒久ID付与
- V2 MOF Budget Itemへのproduction link

このPoCは「抽出された文字列をどう安全に中間ファイル化するか」を先に検証している。

## 次に進めるなら

### Phase 1: source acquisition

```text
source-manifest
  url
  fetchedAt
  sha256
  mimeType
  adapterId
```

を固定し、PDF/Excel原本をrawとして保存する。

### Phase 2: adapter interface

省庁・年度・資料形式ごとに小さなadapterを置く。

```ts
interface RequestDocumentAdapter {
  supports(meta: SourceDocumentMeta): boolean;
  extract(raw: Buffer): Promise<StagingRecord[]>;
  normalize(rows: StagingRecord[]): RequestRecord[];
  validate(rows: RequestRecord[]): ValidationFinding[];
}
```

「全省庁共通parser」を先に作らず、adapterを追加していく。

### Phase 3: golden corpus

まずデジタル庁R6をfull-document goldenにする。

- 項020総額
- 通常分
- 重要政策推進枠
- 府省システム名
- 合計金額
- 係と府省が一致しないknown case

を固定する。

### Phase 4: V2接続

最終的には、概算要求を次の上流に置く。

```text
Request / Concept
  -> Budget Item
  -> Budget Events
  -> Transfer
  -> Settlement
  -> RS Review Project
  -> System Entity
  -> Payment / Contract
```

ここで `request record -> MOF budget item` のlinkも、V2既存方針と同様に `link_method / confidence / source_ref` を保持する。

## 判断

PoCとしては、中間ファイル方式は十分成立しそう。

特に重要なのは、PDF解析の精度を最初から100%にすることではなく、

- raw/stagingを残す
- confidentなものだけnormalizedへ上げる
- 未解決を未解決のまま保持する
- goldenで金額と構造を検証する

というV2と同じ思想を、概算要求の上流にも適用すること。
