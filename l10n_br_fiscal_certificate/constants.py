# Copyright (C) 2021  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

CERTIFICATE_TYPE_NFE = "nf-e"
CERTIFICATE_TYPE_ECPF = "e-cpf"
CERTIFICATE_TYPE_ECNPJ = "e-cnpj"

CERTIFICATE_TYPE = [
    (CERTIFICATE_TYPE_ECPF, "E-CPF"),
    (CERTIFICATE_TYPE_ECNPJ, "E-CNPJ"),
    (CERTIFICATE_TYPE_NFE, "NF-e"),
]

CERTIFICATE_TYPE_DEFAULT = CERTIFICATE_TYPE_NFE

CERTIFICATE_SUBTYPE = [("a1", "A1"), ("a3", "A3")]
CERTIFICATE_SUBTYPE_DEFAULT = "a1"
