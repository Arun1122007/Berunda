const catalyst = require("zcatalyst-sdk-node");

module.exports = async (event, context) => {
  const ctx = catalyst.initialize(context);
  const { briefFacts } = event?.data || {};

  const entities = {
    persons: [],
    vehicles: [],
    locations: [],
    sections: [],
  };

  if (!briefFacts) {
    return context.closeWithSuccess({ entities });
  }

  const namePattern = /[A-Z][a-z]+(?:\s[A-Z][a-z]+)+/g;
  const names = briefFacts.match(namePattern) || [];
  entities.persons = [...new Set(names)].map((n) => ({ name: n }));

  const vehiclePattern = /[A-Z]{2}-\d{2}-[A-Z]{2}-\d{4}/g;
  const vehicles = briefFacts.match(vehiclePattern) || [];
  entities.vehicles = [...new Set(vehicles)].map((v) => ({ number: v }));

  const sectionPattern = /(\d+)\s*IPC/g;
  const sections = [...briefFacts.matchAll(sectionPattern)].map((m) => m[1]);
  entities.sections = [...new Set(sections)].map((s) => ({ section: s }));

  context.closeWithSuccess({ entities });
};
