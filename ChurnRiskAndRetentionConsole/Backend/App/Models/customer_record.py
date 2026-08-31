from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Optional, Mapping

from .gender import Gender
from .multiple_lines_option import MultipleLinesOption
from .internet_service_option import InternetServiceOption
from .feature_option import FeatureOption
from .contract_type import ContractType
from .payment_method_type import PaymentMethodType
from .outreach import Outreach
from ..Services.risk_score_service import CalculateRiskScore

@dataclass
class CustomerRecord:
    customer_id: str
    gender: Gender
    senior_citizen: bool
    partner: bool
    dependents: bool
    tenure: int
    phone_service: bool
    multiple_lines: MultipleLinesOption
    internet_service: InternetServiceOption
    online_security: FeatureOption
    online_backup: FeatureOption
    device_protection: FeatureOption
    tech_support: FeatureOption
    streaming_tv: FeatureOption
    streaming_movies: FeatureOption
    contract: ContractType
    paperless_billing: bool
    payment_method: PaymentMethodType
    monthly_charges: Decimal
    total_charges: Optional[Decimal]
    churn: bool
    outreach: str
    risk_score: Optional[Decimal] = None
    list_of_risks: Optional[list] = None


    @staticmethod
    def _parse_bool_yes_no(value: str) -> bool:
        return str(value).strip().lower() == "yes"

    @staticmethod
    def _parse_bool_numeric(value: str) -> bool:
        v = str(value).strip()
        return v == "1" or v.lower() == "true" or v.lower() == "yes"

    @staticmethod
    def _parse_decimal(value: str) -> Optional[Decimal]:
        s = str(value).strip()
        if s == "" or s.lower() in {"nan", "none"}:
            return None
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError):
            return None

    @staticmethod
    def _calculate_risk_score(customer_data: dict) -> tuple:
        risk_score, list_of_risks = CalculateRiskScore(customer_data)
        return Decimal(str(risk_score)), list_of_risks

    @classmethod
    def from_csv_row(cls, row: Mapping[str, str]) -> "CustomerRecord":
        get = lambda k: str(row.get(k, "")).strip()

        def parse_enum(enum_cls, val, fallback=None):
            for member in enum_cls:
                if str(member.value).lower() == val.lower():
                    return member
            return fallback or list(enum_cls)[0]

        monthly = cls._parse_decimal(get("MonthlyCharges")) or Decimal("0")
        total = cls._parse_decimal(get("TotalCharges"))
        (riskScore, risks) = cls._calculate_risk_score({
            "churn": cls._parse_bool_yes_no(get("Churn")),
            "tenure": int(get("tenure") or 0),
            # Add other customer data fields as needed
        })
        return cls(
            customer_id=get("customerID"),
            gender=parse_enum(Gender, get("gender"), Gender.UNKNOWN),
            senior_citizen=cls._parse_bool_numeric(get("SeniorCitizen")),
            partner=cls._parse_bool_yes_no(get("Partner")),
            dependents=cls._parse_bool_yes_no(get("Dependents")),
            tenure=int(get("tenure") or 0),
            phone_service=cls._parse_bool_yes_no(get("PhoneService")),
            multiple_lines=parse_enum(MultipleLinesOption, get("MultipleLines"), MultipleLinesOption.NO),
            internet_service=parse_enum(InternetServiceOption, get("InternetService"), InternetServiceOption.NONE),
            online_security=parse_enum(FeatureOption, get("OnlineSecurity"), FeatureOption.NO),
            online_backup=parse_enum(FeatureOption, get("OnlineBackup"), FeatureOption.NO),
            device_protection=parse_enum(FeatureOption, get("DeviceProtection"), FeatureOption.NO),
            tech_support=parse_enum(FeatureOption, get("TechSupport"), FeatureOption.NO),
            streaming_tv=parse_enum(FeatureOption, get("StreamingTV"), FeatureOption.NO),
            streaming_movies=parse_enum(FeatureOption, get("StreamingMovies"), FeatureOption.NO),
            contract=parse_enum(ContractType, get("Contract"), ContractType.MONTH_TO_MONTH),
            paperless_billing=cls._parse_bool_yes_no(get("PaperlessBilling")),
            payment_method=parse_enum(PaymentMethodType, get("PaymentMethod"), PaymentMethodType.OTHER),
            monthly_charges=monthly,
            total_charges=total,
            churn=cls._parse_bool_yes_no(get("Churn")),
            outreach=Outreach.NOT_CONTACTED,
            risk_score=riskScore,
            list_of_risks=risks,
        )
