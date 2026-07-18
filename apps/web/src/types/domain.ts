export interface CaseMaster {
  caseId: string;
  firNumber: string;
  districtId: string;
  policeStationId: string;
  crimeTypeId: string;
  dateFiled: string;
  dateRegistered: string;
  status: CaseStatus;
  narrative: string;
  sections: string[];
  createdAt: string;
  updatedAt: string;
}

export type CaseStatus =
  | "filed"
  | "under-investigation"
  | "charge-sheet-filed"
  | "trial"
  | "convicted"
  | "acquitted"
  | "closed";

export interface PersonEntity {
  personId: string;
  masterCaseId: string;
  name: string;
  role: PersonRole;
  age?: number;
  gender?: string;
  address?: string;
  phone?: string;
  idMark?: string;
  firMention: string;
  confidence: number;
  resolvedToEntityId?: string;
  createdAt: string;
}

export type PersonRole =
  | "accused"
  | "victim"
  | "witness"
  | "complainant"
  | "informant";

export interface LocationEntity {
  locationId: string;
  masterCaseId: string;
  name: string;
  latitude: number;
  longitude: number;
  type: LocationType;
  district: string;
  policeStation: string;
  description?: string;
  confidence: number;
  createdAt: string;
}

export type LocationType =
  | "crime-scene"
  | "residence"
  | "business"
  | "transit"
  | "other";

export interface VehicleEntity {
  vehicleId: string;
  masterCaseId: string;
  registrationNumber: string;
  type: VehicleType;
  make?: string;
  model?: string;
  color?: string;
  ownerName?: string;
  confidence: number;
  createdAt: string;
}

export type VehicleType =
  | "two-wheeler"
  | "three-wheeler"
  | "four-wheeler"
  | "heavy-vehicle"
  | "other";

export interface CrimeType {
  crimeTypeId: string;
  name: string;
  category: string;
  description?: string;
  bnsSections: string[];
}

export interface District {
  districtId: string;
  name: string;
  state: string;
  population?: number;
  area?: number;
  policeStations: PoliceStation[];
}

export interface PoliceStation {
  policeStationId: string;
  districtId: string;
  name: string;
  latitude: number;
  longitude: number;
  jurisdictionArea?: string;
  contactNumber?: string;
}
