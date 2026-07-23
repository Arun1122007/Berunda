const catalyst = require("zcatalyst-sdk-node");

function soundex(name) {
  const map = { b: "1", f: "1", p: "1", v: "1", c: "2", g: "2", j: "2", k: "2", q: "2", s: "2", x: "2", z: "2", d: "3", t: "3", l: "4", m: "5", n: "5", r: "6" };
  const s = name.toUpperCase();
  let code = s[0];
  for (let i = 1; i < s.length && code.length < 4; i++) {
    if (map[s[i]] && map[s[i]] !== code[code.length - 1]) code += map[s[i]];
  }
  return code.padEnd(4, "0");
}

function levenshtein(a, b) {
  const m = [], i = a.length, j = b.length;
  for (let k = 0; k <= i; k++) m[k] = [k];
  for (let k = 0; k <= j; k++) m[0][k] = k;
  for (let k = 1; k <= i; k++)
    for (let l = 1; l <= j; l++)
      m[k][l] = Math.min(m[k - 1][l] + 1, m[k][l - 1] + 1, m[k - 1][l - 1] + (a[k - 1] !== b[l - 1] ? 1 : 0));
  return 1 - m[i][j] / Math.max(i, j);
}

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { name, age, districtId } = event?.data || {};

  if (!name) return context.closeWithSuccess({ candidates: [] });

  const table = ctx.datastore().table("int_PersonEntity");
  const allRows = await table.getAllRows();

  const candidates = allRows
    .filter((r) => {
      const ageDiff = Math.abs((r.DOB ? new Date().getFullYear() - new Date(r.DOB).getFullYear() : 0) - (age || 0));
      return r.PrimaryDistrictID === districtId && ageDiff <= 5;
    })
    .map((r) => ({
      entityId: r.PersonEntityID,
      name: r.CanonicalName,
      soundexScore: soundex(name) === soundex(r.CanonicalName) ? 0.4 : 0,
      levenshteinScore: levenshtein(name.toLowerCase(), r.CanonicalName.toLowerCase()) * 0.3,
      totalScore: 0,
    }));

  candidates.forEach((c) => {
    c.totalScore = c.soundexScore + c.levenshteinScore + 0.1;
    c.totalScore = Math.round(c.totalScore * 10000) / 10000;
  });

  candidates.sort((a, b) => b.totalScore - a.totalScore);
  context.closeWithSuccess({ candidates: candidates.slice(0, 10) });
};
