// ROLE-BASED ACCESS CONTROL (RBAC) PERMISSION MATRIX

export const ROLES = {
  ADMIN: "ADMIN",
  OFFICER: "OFFICER",
  REVIEWER: "REVIEWER",
  AUDITOR: "AUDITOR",
  CITIZEN: "CITIZEN"
};

export const PERMISSIONS = {
  // Navigation & Page access
  ACCESS_ADMIN_DASHBOARD: ["ADMIN"],
  ACCESS_OFFICER_DASHBOARD: ["ADMIN", "OFFICER"],
  ACCESS_REVIEWER_DASHBOARD: ["ADMIN", "REVIEWER"],
  ACCESS_AUDITOR_DASHBOARD: ["ADMIN", "AUDITOR"],
  ACCESS_CITIZEN_DASHBOARD: ["ADMIN", "OFFICER", "REVIEWER", "AUDITOR", "CITIZEN"],

  // Feature operations
  UPLOAD_BATCH: ["ADMIN", "OFFICER"],
  HUMAN_REVIEW_EDIT: ["ADMIN", "REVIEWER"],
  APPROVE_RECORD: ["ADMIN", "REVIEWER"],
  REJECT_RECORD: ["ADMIN", "REVIEWER"],
  MANAGE_USERS: ["ADMIN"],
  MANAGE_SETTINGS: ["ADMIN"],
  VIEW_AUDIT_TRAIL: ["ADMIN", "AUDITOR", "REVIEWER"],
  SEARCH_PUBLIC_RECORDS: ["ADMIN", "OFFICER", "REVIEWER", "AUDITOR", "CITIZEN"],
  SUBMIT_GRIEVANCE: ["CITIZEN"]
};

export function hasPermission(userRole, permissionKey) {
  if (!userRole) return false;
  const allowedRoles = PERMISSIONS[permissionKey];
  if (!allowedRoles) return false;
  return allowedRoles.includes(userRole);
}

export function getDefaultDashboardForRole(role) {
  switch (role) {
    case ROLES.ADMIN:
      return "/a/dashboard";
    case ROLES.OFFICER:
      return "/o/dashboard";
    case ROLES.REVIEWER:
      return "/r/dashboard";
    case ROLES.AUDITOR:
      return "/au/dashboard";
    case ROLES.CITIZEN:
      return "/u/dashboard";
    default:
      return "/login";
  }
}

export function getLandRecordsForUser(records = [], user) {
  if (!user) return [];
  if (user.role === ROLES.CITIZEN) {
    const targetCitizenId = user.citizenId || user.id;
    return records.filter(record => record.citizenId === targetCitizenId);
  }
  return records;
}

export function canUserAccessRecord(record, user) {
  if (!user || !record) return false;
  if (user.role === ROLES.CITIZEN) {
    const targetCitizenId = user.citizenId || user.id;
    return record.citizenId === targetCitizenId;
  }
  return true;
}

