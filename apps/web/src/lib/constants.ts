export const DISTRICTS: Record<number, string> = {
  1: "Bengaluru Urban",
  2: "Bengaluru Rural",
  3: "Belagavi",
  4: "Mysuru",
  5: "Hubballi-Dharwad",
  6: "Kalaburagi",
  7: "Mangaluru",
  8: "Shivamogga",
  9: "Tumakuru",
  10: "Ballari",
};

export const CASE_STATUS: Record<string, string> = {
  filed: "Filed",
  under_investigation: "Under Investigation",
  charge_sheet_filed: "Charge Sheet Filed",
  trial: "Trial",
  convicted: "Convicted",
  acquitted: "Acquitted",
  closed: "Closed",
};

export const CASE_STATUS_COLOR: Record<string, "info" | "warning" | "success" | "danger"> = {
  filed: "info",
  under_investigation: "warning",
  charge_sheet_filed: "info",
  trial: "warning",
  convicted: "success",
  acquitted: "info",
  closed: "info",
};

export const SEVERITY_LABEL: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
  critical: "Critical",
};

export const SEVERITY_COLOR: Record<string, "info" | "warning" | "danger"> = {
  low: "info",
  medium: "warning",
  high: "danger",
  critical: "danger",
};
