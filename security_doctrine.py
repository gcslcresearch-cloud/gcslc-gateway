"""
Global Security Doctrine – 8R Stealth Paradigm (D1–D8)

Applies the 8R sequence to:
- Border Security
- Intelligence Refinement

© GCSLC. Proprietary.
"""

from dataclasses import dataclass
from typing import List


DETERMINANTS_D1_D8 = [
    "D1 Refine",
    "D2 Reset",
    "D3 Research",
    "D4 Restructure",
    "D5 Resuscitate",
    "D6 Revitalize",
    "D7 Re-engineer",
    "D8 Retain",
]


@dataclass
class DoctrineStep:
    determinant: str
    description: str


def border_security_doctrine() -> List[DoctrineStep]:
    """Military-grade 8R logic for paramilitary Border Security."""
    return [
        DoctrineStep("D1 Refine", "Refine rules of engagement, patrol patterns, and data capture."),
        DoctrineStep("D2 Reset", "Reset legacy protocols that leak intelligence or enable porous borders."),
        DoctrineStep("D3 Research", "Research cross-border threat vectors and smuggling routes (NW/NE corridors)."),
        DoctrineStep("D4 Restructure", "Restructure command, logistics, and surveillance architecture."),
        DoctrineStep("D5 Resuscitate", "Resuscitate degraded outposts with 8R-ready infrastructure and comms."),
        DoctrineStep("D6 Revitalize", "Revitalize rapid-response units and inter-agency coordination."),
        DoctrineStep("D7 Re-engineer", "Re-engineer border security with AI-assisted monitoring and nodal alerts."),
        DoctrineStep("D8 Retain", "Retain strategic advantage; lock in sovereign control over border flows."),
    ]


def intelligence_refinement_doctrine() -> List[DoctrineStep]:
    """Military-grade 8R logic for Intelligence Refinement."""
    return [
        DoctrineStep("D1 Refine", "Refine collection priorities; remove noise from intelligence feeds."),
        DoctrineStep("D2 Reset", "Reset analyst workflows and briefing formats for clarity."),
        DoctrineStep("D3 Research", "Research adversary patterns, digital signatures, and nodal behaviors."),
        DoctrineStep("D4 Restructure", "Restructure data pipelines and analytic cells for convergence."),
        DoctrineStep("D5 Resuscitate", "Resuscitate dormant sources and high-value human/technical assets."),
        DoctrineStep("D6 Revitalize", "Revitalize fusion centers and cross-agency sharing protocols."),
        DoctrineStep("D7 Re-engineer", "Re-engineer analytic models with AI/ML tuned to 8R determinants."),
        DoctrineStep("D8 Retain", "Retain critical knowledge; secure institutional memory and sovereign IP."),
    ]

