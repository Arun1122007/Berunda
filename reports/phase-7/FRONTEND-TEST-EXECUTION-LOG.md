# Project Berunda — Frontend Test Execution Summary

## Vitest Test Suite Output
```
[1m[7m[36m RUN [39m[27m[22m [36mv2.1.9 [39m[90mD:/Hack2Skill/Berunda/apps/web[39m

 [32mâœ“[39m src/features/evidence/__tests__/EvidenceManager.test.tsx [2m([22m[2m2 tests[22m[2m)[22m[90m 131[2mms[22m[39m
 [32mâœ“[39m src/features/offenders/__tests__/OffendersPage.test.tsx [2m([22m[2m2 tests[22m[2m)[22m[90m 230[2mms[22m[39m
 [32mâœ“[39m src/features/investigation/__tests__/InvestigationNotes.test.tsx [2m([22m[2m4 tests[22m[2m)[22m[90m 135[2mms[22m[39m
 [32mâœ“[39m src/features/cases/__tests__/CaseListPage.test.tsx [2m([22m[2m3 tests[22m[2m)[22m[90m 181[2mms[22m[39m
 [32mâœ“[39m __tests__/App.test.tsx [2m([22m[2m1 test[22m[2m)[22m[90m 55[2mms[22m[39m
 [32mâœ“[39m src/features/search/__tests__/SearchPage.test.tsx [2m([22m[2m3 tests[22m[2m)[22m[90m 146[2mms[22m[39m
 [32mâœ“[39m src/features/related-cases/__tests__/RelatedCasesPanel.test.tsx [2m([22m[2m2 tests[22m[2m)[22m[90m 84[2mms[22m[39m
 [32mâœ“[39m src/features/cases/__tests__/CaseDetailPage.test.tsx [2m([22m[2m4 tests[22m[2m)[22m[90m 272[2mms[22m[39m
 [32mâœ“[39m src/features/cases/__tests__/CreateCasePage.test.tsx [2m([22m[2m4 tests[22m[2m)[22m[33m 346[2mms[22m[39m

[2m Test Files [22m [1m[32m9 passed[39m[22m[90m (9)[39m
[2m      Tests [22m [1m[32m25 passed[39m[22m[90m (25)[39m
[2m   Start at [22m 23:20:26
[2m   Duration [22m 7.26s[2m (transform 3.68s, setup 5.91s, collect 8.80s, tests 1.58s, environment 21.81s, prepare 3.42s)[22m
```

## Vite Production Build Output
```
> @berunda/web@0.1.0 build
> vite build

[36mvite v5.4.21 [32mbuilding for production...[36m[39m
transforming...
[32mâœ“[39m 2418 modules transformed.
rendering chunks...
computing gzip size...
[2mdist/[22m[32mindex.html                             [39m[1m[2m  1.08 kB[22m[1m[22m[2m â”‚ gzip:   0.53 kB[22m
[2mdist/[22m[35massets/index-BO2M9H9l.css              [39m[1m[2m 43.96 kB[22m[1m[22m[2m â”‚ gzip:   7.98 kB[22m
[2mdist/[22m[35massets/HotspotMapPage-CuCRB34y.css     [39m[1m[2m 65.48 kB[22m[1m[22m[2m â”‚ gzip:   9.22 kB[22m
[2mdist/[22m[36massets/formatters-BSmOHwVo.js          [39m[1m[2m  0.60 kB[22m[1m[22m[2m â”‚ gzip:   0.36 kB[22m
[2mdist/[22m[36massets/useApi-uTumPe5V.js              [39m[1m[2m  1.00 kB[22m[1m[22m[2m â”‚ gzip:   0.51 kB[22m
[2mdist/[22m[36massets/NotFoundPage-COOHtEPp.js        [39m[1m[2m  1.26 kB[22m[1m[22m[2m â”‚ gzip:   0.63 kB[22m
[2mdist/[22m[36massets/Card-Bx9D5iFd.js                [39m[1m[2m  1.38 kB[22m[1m[22m[2m â”‚ gzip:   0.55 kB[22m
[2mdist/[22m[36massets/HotspotMapPage-0W8ZS6k9.js      [39m[1m[2m  1.45 kB[22m[1m[22m[2m â”‚ gzip:   0.81 kB[22m
[2mdist/[22m[36massets/LinkGraphPage-C4t4gvFz.js       [39m[1m[2m  1.60 kB[22m[1m[22m[2m â”‚ gzip:   0.86 kB[22m
[2mdist/[22m[36massets/LoginPage-DxRm1haC.js           [39m[1m[2m  1.79 kB[22m[1m[22m[2m â”‚ gzip:   0.87 kB[22m
[2mdist/[22m[36massets/AnalyticsPage-CL8ckFVF.js       [39m[1m[2m  1.89 kB[22m[1m[22m[2m â”‚ gzip:   0.93 kB[22m
[2mdist/[22m[36massets/AskBerundaPage-Ck46nRTn.js      [39m[1m[2m  2.86 kB[22m[1m[22m[2m â”‚ gzip:   1.17 kB[22m
[2mdist/[22m[36massets/FirAiReviewPage-BzY5SOlk.js     [39m[1m[2m  4.12 kB[22m[1m[22m[2m â”‚ gzip:   1.55 kB[22m
[2mdist/[22m[36massets/EntityPage-C3d1P6H8.js          [39m[1m[2m  4.49 kB[22m[1m[22m[2m â”‚ gzip:   1.46 kB[22m
[2mdist/[22m[36massets/CaseListPage-BEcMJ0eH.js        [39m[1m[2m  5.22 kB[22m[1m[22m[2m â”‚ gzip:   1.63 kB[22m
[2mdist/[22m[36massets/AuditLogPage-DW2K28mk.js        [39m[1m[2m  5.30 kB[22m[1m[22m[2m â”‚ gzip:   1.75 kB[22m
[2mdist/[22m[36massets/EditCasePage-CZsWqyyM.js        [39m[1m[2m  7.34 kB[22m[1m[22m[2m â”‚ gzip:   2.26 kB[22m
[2mdist/[22m[36massets/OffendersPage-DJpzZqFP.js       [39m[1m[2m  7.36 kB[22m[1m[22m[2m â”‚ gzip:   2.51 kB[22m
[2mdist/[22m[36massets/AnomaliesPage-CbWd-afv.js       [39m[1m[2m  7.65 kB[22m[1m[22m[2m â”‚ gzip:   2.60 kB[22m
[2mdist/[22m[36massets/RiskPage-Dn9rIIIf.js            [39m[1m[2m  7.65 kB[22m[1m[22m[2m â”‚ gzip:   2.48 kB[22m
[2mdist/[22m[36massets/DashboardPage-DFf8P0Jj.js       [39m[1m[2m  7.94 kB[22m[1m[22m[2m â”‚ gzip:   2.44 kB[22m
[2mdist/[22m[36massets/ImportPage-TXAg9tGE.js          [39m[1m[2m  8.42 kB[22m[1m[22m[2m â”‚ gzip:   3.08 kB[22m
[2mdist/[22m[36massets/SocioeconomicPage-WtCf6ZER.js   [39m[1m[2m  8.48 kB[22m[1m[22m[2m â”‚ gzip:   2.41 kB[22m
[2mdist/[22m[36massets/AdminPage-ByG3bXw1.js           [39m[1m[2m  8.48 kB[22m[1m[22m[2m â”‚ gzip:   2.33 kB[22m
[2mdist/[22m[36massets/CreateCasePage-DqDtpGVj.js      [39m[1m[2m  8.92 kB[22m[1m[22m[2m â”‚ gzip:   2.60 kB[22m
[2mdist/[22m[36massets/OffenderDetailPage-n3_iRppu.js  [39m[1m[2m  9.62 kB[22m[1m[22m[2m â”‚ gzip:   2.92 kB[22m
[2mdist/[22m[36massets/ReportsPage-CGp0lcpW.js         [39m[1m[2m  9.70 kB[22m[1m[22m[2m â”‚ gzip:   3.12 kB[22m
[2mdist/[22m[36massets/SearchPage-D8S_6Zc9.js          [39m[1m[2m 11.06 kB[22m[1m[22m[2m â”‚ gzip:   3.27 kB[22m
[2mdist/[22m[36massets/index-CMc5Ygj6.js               [39m[1m[2m 19.87 kB[22m[1m[22m[2m â”‚ gzip:   7.02 kB[22m
[2mdist/[22m[36massets/CaseDetailPage-CpERWeys.js      [39m[1m[2m 21.53 kB[22m[1m[22m[2m â”‚ gzip:   5.50 kB[22m
[2mdist/[22m[36massets/icons-BjAmbC4z.js               [39m[1m[2m 26.72 kB[22m[1m[22m[2m â”‚ gzip:   5.17 kB[22m
[2mdist/[22m[36massets/vendor-CUw78Rje.js              [39m[1m[2m164.19 kB[22m[1m[22m[2m â”‚ gzip:  53.58 kB[22m
[2mdist/[22m[36massets/recharts-DqCax-At.js            [39m[1m[2m423.40 kB[22m[1m[22m[2m â”‚ gzip: 113.03 kB[22m
[2mdist/[22m[36massets/cytoscape-CUqq0XTU.js           [39m[1m[2m443.69 kB[22m[1m[22m[2m â”‚ gzip: 142.35 kB[22m
[2mdist/[22m[36massets/maplibre-CPZg0KlB.js            [39m[1m[2m801.64 kB[22m[1m[22m[2m â”‚ gzip: 217.60 kB[22m
[32mâœ“ built in 16.10s[39m
```
