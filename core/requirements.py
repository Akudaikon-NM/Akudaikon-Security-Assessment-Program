"""
Requirements backbone for GLBA + §748.0 + §748.1
"""

GLBA_REQUIREMENTS = {
    "Section 501(b)": "Implement administrative, technical, and physical safeguards to protect customer information security and confidentiality, against anticipated threats, and against unauthorized access causing substantial harm."
}

SECTION_748_0_REQUIREMENTS = {
    "12 CFR § 748.0(a)": "Each federally insured credit union must develop and maintain a security program to ensure the security and confidentiality of member records and information.",
    "12 CFR § 748.0(b)(1)": "Protect against anticipated threats or hazards to the security or integrity of member records and information.",
    "12 CFR § 748.0(b)(2)": "Protect against unauthorized access to or use of member records or information that could result in substantial harm or inconvenience to a member.",
    "12 CFR § 748.0(b)(3)": "Protect credit union offices from physical crimes, including robberies, burglaries, larcenies, and embezzlement.",
    "12 CFR § 748.0(b)(4)": "Respond to incidents of unauthorized access to sensitive member information.",
    "12 CFR § 748.0(b)(5)": "Prevent the destruction of vital records, as defined in 12 CFR Part 749.",
    "12 CFR § 748.0(c)": "Ensure proper disposal of consumer information.",
    "12 CFR § 748.0(d)": "Adjust the security program in light of changing threats, vulnerabilities, and similar factors.",
    "12 CFR § 748.0(e)": "Designate an employee or committee to coordinate and be responsible for the security program.",
    "12 CFR § 748.0(f)": "Provide for regular testing and monitoring of the security program.",
    "12 CFR § 748.0(g)": "Adjust the security program based on testing and monitoring results."
}

SECTION_748_1_REQUIREMENTS = {
    "12 CFR § 748.1(a)": "Annual certification of compliance through the Credit Union Profile.",
    "12 CFR § 748.1(b)": "Catastrophic act reporting.",
    "12 CFR § 748.1(c)": "Cyber incident reporting within 72 hours.",
    "12 CFR § 748.1(d)": "Suspicious Activity Report (SAR) coordination, where applicable."
}

ALL_REQUIREMENTS = {**GLBA_REQUIREMENTS, **SECTION_748_0_REQUIREMENTS, **SECTION_748_1_REQUIREMENTS}