# FY2024 All-Authority Format Census — Population Freeze

Status: **population freeze. No acquisition, no visual inspection, no format classification performed in this document.**

Date: 2026-09-27 (Asia/Tokyo)

Branch: `research/fy2024-all-authority-format-census`, from `main@fc7c0ea`.

## 1. Source of the population

`[FACT]` MOF's official FY2024 cross-authority link table: `https://www.mof.go.jp/policy/budget/budger_workflow/budget/fy2024/2024yokyuippan_link.html`, fetched 2026-09-27. This page is treated as the canonical population starting point per the originating task's own §3.

## 2. Frozen population (33 authorities, in the page's own listed order)

`[FACT]` Each row below reproduces the authority name and its 歳出 (expenditure) column link exactly as listed on the MOF page. No PDF has been acquired yet; no landing page has been visited yet; these are the MOF-page-stated links only, not yet verified as leading to an actual PDF.

| # | authorityId (provisional) | authorityName | mofIndexUrl (歳出 link as listed) |
|---|---|---|---|
| 1 | kunaicho | 皇室費 | https://www.kunaicho.go.jp/kunaicho/kunaicho/gaisanyokyu.html |
| 2 | shugiin | 衆議院 | https://www.shugiin.go.jp/internet/itdb_annai.nsf/html/statics/osirase/kaikei-gaisan.html |
| 3 | sangiin | 参議院 | https://www.sangiin.go.jp/japanese/annai/oshirase/yosan-gaisan.html |
| 4 | ndl | 国立国会図書館 | https://www.ndl.go.jp/jp/aboutus/outline/finances.html |
| 5 | sotsui | 裁判官訴追委員会 | https://www.sotsui.go.jp/budget/index.html |
| 6 | dangai | 裁判官弾劾裁判所 | https://www.dangai.go.jp/info/report.html |
| 7 | courts | 裁判所 | https://www.courts.go.jp/about/yosan_kessan/vcmsFolder_1269/vcms_1269.html |
| 8 | jbaudit | 会計検査院 | https://www.jbaudit.go.jp/jbaudit/bud_clo/bud/06.html |
| 9 | cabinet | 内閣 | https://www.cas.go.jp/jp/yosan/index.html |
| 10 | cas | 内閣官房 | https://www.cas.go.jp/jp/yosan/index.html |
| 11 | clb | 内閣法制局 | https://www.clb.go.jp/policy/budget/ |
| 12 | jinji | 人事院 | https://www.jinji.go.jp/yosan/6yosantop.html |
| 13 | cao | 内閣本府 | https://www.cao.go.jp/yosan/yosan.html |
| 14 | kunaicho-agency | 宮内庁 | https://www.kunaicho.go.jp/kunaicho/kunaicho/gaisanyokyu.html |
| 15 | jftc | 公正取引委員会 | https://www.jftc.go.jp/soshiki/kyotsukoukai/yosan/yosankessan/r6.html |
| 16 | npa | 警察庁 | https://www.npa.go.jp/policies/budget/r6/gaisanyokyu/index.html |
| 17 | ppc | 個人情報保護委員会 | https://www.ppc.go.jp/aboutus/budget/budget_R6/ |
| 18 | jcrc | カジノ管理委員会 | https://www.jcrc.go.jp/about/budget.html |
| 19 | fsa | 金融庁 | https://www.fsa.go.jp/common/budget/yosan/6youkyuu-2.html |
| 20 | caa | 消費者庁 | https://www.caa.go.jp/policies/budget/ |
| 21 | cfa | こども家庭庁 | https://www.cfa.go.jp/policies/budget/ |
| 22 | digital | デジタル庁 | https://www.digital.go.jp/budget/r6request |
| 23 | soumu | 総務省 | https://www.soumu.go.jp/menu_yosan/yosan_R06.html |
| 24 | moj | 法務省 | https://www.moj.go.jp/kaikei/bunsho/kaikei02_00121.html |
| 25 | mofa | 外務省 | https://www.mofa.go.jp/mofaj/annai/yosan_kessan/mofa_yosan_kessan/index.html |
| 26 | mof | 財務省 | https://www.mof.go.jp/about_mof/mof_budget/budget/fy2024/2024ippan_2.pdf |
| 27 | mext | 文部科学省 | https://www.mext.go.jp/a_menu/yosan/r01/1420672_00009.htm |
| 28 | mhlw | 厚生労働省 | https://www.mhlw.go.jp/wp/yosan/yosan/24syokan/05.html |
| 29 | maff | 農林水産省 | https://www.maff.go.jp/j/budget/230901.html |
| 30 | meti | 経済産業省 | https://www.meti.go.jp/main/yosangaisan/fy2024/index.html |
| 31 | mlit | 国土交通省 | https://www.mlit.go.jp/page/kanbo05_hy_003158.html |
| 32 | env | 環境省 | https://www.env.go.jp/guide/budget/r06/page_00887.html |
| 33 | mod | 防衛省 | https://www.mod.go.jp/j/budget/gaisan/index.html |

## 3. Cross-reference to existing case-001–005

`[FACT]` Of the 33 frozen population entries, 5 already have detailed source-survey-through-benchmark research: `digital` (case-001), `meti` (case-002), `soumu` (case-003), `mext` (case-004), `mlit` (case-005). These will be integrated into the census from already-committed source-safe evidence, not re-surveyed from scratch, per the originating task's own §5/§12.

## 4. Notes on this freeze

`[OBSERVATION]` MOF's page lists 内閣 and 内閣官房 as two separate rows sharing the identical link (`cas.go.jp/jp/yosan/index.html`) — not yet resolved whether these produce distinct PDFs or the same package; deferred to acquisition/landing-page inspection.

`[OBSERVATION]` 皇室費 and 宮内庁 share the identical link (`kunaicho.go.jp`) — same open question, deferred.

`[FACT]` No acquisition, landing-page visit, PDF download, or visual inspection has been performed for any of the 33 entries as of this freeze. This document records only the MOF-page-stated links.

`[INTERPRETATION]` This is a provisional authorityId scheme (romanized, informal) for internal tracking within this census only — not a claim about any external identifier standard.

## 5. Batching (execution convenience only, per the originating task's §15)

- **Batch A** (major ministries/agencies): mof, mhlw, maff, env, mod, mofa, moj, cfa, fsa, npa
- **Batch B** (Cabinet/commissions): cas, cao, clb, jinji, jftc, ppc, jcrc, caa, +remaining MOF-listed
- **Batch C** (Legislative/Judicial/independent): shugiin, sangiin, ndl, sotsui, dangai, courts, jbaudit, kunaicho
- **Already surveyed** (case-001–005): digital, meti, soumu, mext, mlit

This batching is execution-internal only; the final census integrates all batches into one population table, per the originating task's own instruction not to let batching fragment the final report.

---

**This document freezes the population only. No acquisition, PDF download, visual inspection, or format classification has been performed.**
