from enum import Enum
from typing import List
from fastapi import HTTPException, status

class AppRole(str, Enum):
    ADMIN = "ADMIN"
    OFFICER = "OFFICER"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"
    CITIZEN = "CITIZEN"

ROLE_MAPPING = {
    "ADMIN": AppRole.ADMIN,
    "OFFICER": AppRole.OFFICER,
    "REVENUE_OFFICER": AppRole.OFFICER,
    "SURVEY_OFFICER": AppRole.OFFICER,
    "REVIEWER": AppRole.REVIEWER,
    "AUDITOR": AppRole.AUDITOR,
    "CITIZEN": AppRole.CITIZEN,
}

def normalize_role(role_str: str) -> str:
    if not role_str:
        return AppRole.CITIZEN
    upper_role = role_str.upper()
    return ROLE_MAPPING.get(upper_role, upper_role)

def check_role_permission(user_role: str, allowed_roles: List[AppRole]):
    normalized = normalize_role(user_role)
    if normalized not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "FORBIDDEN",
                "message": f"Access denied. Required role(s): {[r.value for r in allowed_roles]}, but user has '{normalized}'."
            }
        )
