"""CloudInstruction Pydantic schema with security validators."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CloudInstruction(BaseModel):
    """Structured instruction for cloud-based security analysis agents.

    Includes validators to prevent secret leakage and prompt injection.
    """

    model_config = ConfigDict(extra="forbid")

    task_id: str
    action: Literal["analyze_smali", "web_recon", "validate_cve", "complete_audit"]
    target: str = Field(..., description="Sanitized target, no secrets")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str

    @field_validator("target", "reasoning")
    @classmethod
    def validate_no_secrets_or_injection(cls, value: str, info) -> str:
        """Validate that fields don't contain secrets or prompt injection.

        Args:
            value: The field value to validate
            info: Validation context

        Returns:
            The validated value

        Raises:
            ValueError: If AWS keys, JWT tokens, or prompt injection detected
        """
        field_name = info.field_name

        # Check for AWS access keys
        if re.search(r"AKIA[0-9A-Z]{16}", value):
            raise ValueError(
                f"AWS access key detected in {field_name}. "
                "Remove secrets before creating instruction."
            )

        # Check for JWT tokens
        if re.search(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+", value):
            raise ValueError(
                f"JWT token detected in {field_name}. Remove secrets before creating instruction."
            )

        # Check for prompt injection attempts
        injection_patterns = [
            "ignore previous",
            "system:",
            "bypass",
        ]

        value_lower = value.lower()
        for pattern in injection_patterns:
            if pattern in value_lower:
                raise ValueError(
                    f"Prompt injection detected in {field_name}: '{pattern}'. "
                    "Instruction rejected for security."
                )

        return value
