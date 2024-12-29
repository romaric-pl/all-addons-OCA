from openupgradelib import openupgrade, openupgrade_merge_records

_xml_ids_renames = [
    # account_tax_templates
    ("account_tax_template_s_igic0b", "account_tax_template_igic_r_0"),
    ("account_tax_template_s_igic3b", "account_tax_template_igic_r_3"),
    ("account_tax_template_s_igic7b", "account_tax_template_igic_r_7"),
    ("account_tax_template_s_igic95b", "account_tax_template_igic_r_9_5"),
    ("account_tax_template_s_igic15b", "account_tax_template_igic_r_15"),
    ("account_tax_template_s_igic20b", "account_tax_template_igic_r_20"),
    ("account_tax_template_s_igic_ISP0b", "account_tax_template_igic_s_ISP0"),
    ("account_tax_template_s_igic_ex0b", "account_tax_template_igic_ex_0"),
    ("account_tax_template_s_igic_ex_b", "account_tax_template_igic_re_ex"),
    ("account_tax_template_s_igic_cmino_b", "account_tax_template_igic_cmino"),
    ("account_tax_template_p_igic0_bc", "account_tax_template_igic_sop_0"),
    ("account_tax_template_p_igic3_bc", "account_tax_template_igic_sop_3"),
    ("account_tax_template_p_igic7_bc", "account_tax_template_igic_sop_7"),
    ("account_tax_template_p_igic95_bc", "account_tax_template_igic_sop_9_5"),
    ("account_tax_template_p_igic15_bc", "account_tax_template_igic_sop_15"),
    ("account_tax_template_p_igic20_bc", "account_tax_template_igic_sop_20"),
    ("account_tax_template_p_igic_ISP0bc", "account_tax_template_igic_ISP0"),
    ("account_tax_template_p_igic_ISP3bc", "account_tax_template_igic_ISP3"),
    ("account_tax_template_p_igic_ISP7bc", "account_tax_template_igic_ISP7"),
    ("account_tax_template_p_igic_ISP95bc", "account_tax_template_igic_ISP95"),
    ("account_tax_template_p_igic_ISP15bc", "account_tax_template_igic_ISP15"),
    ("account_tax_template_p_igic_ISP20bc", "account_tax_template_igic_ISP20"),
    ("account_tax_template_p_igic_ex_bc", "account_tax_template_igic_p_ex"),
    ("account_tax_template_p_igic_cmino_bc", "account_tax_template_igic_sop_cmino"),
    ("account_tax_template_p_igic3_cmino_bc", "account_tax_template_igic_sop_3_cmino"),
    ("account_tax_template_p_igic7_cmino_bc", "account_tax_template_igic_sop_7_cmino"),
    (
        "account_tax_template_p_igic95_cmino_bc",
        "account_tax_template_igic_sop_9_5_cmino",
    ),
    (
        "account_tax_template_p_igic15_cmino_bc",
        "account_tax_template_igic_sop_15_cmino",
    ),
    (
        "account_tax_template_p_igic20_cmino_bc",
        "account_tax_template_igic_sop_20_cmino",
    ),
    ("account_tax_template_p_igic0_inv_bc", "account_tax_template_igic_sop_0_inv"),
    ("account_tax_template_p_igic3_inv_bc", "account_tax_template_igic_sop_3_inv"),
    ("account_tax_template_p_igic7_inv_bc", "account_tax_template_igic_sop_7_inv"),
    ("account_tax_template_p_igic95_inv_bc", "account_tax_template_igic_sop_9_5_inv"),
    ("account_tax_template_p_igic15_inv_bc", "account_tax_template_igic_sop_15_inv"),
    ("account_tax_template_p_igic20_inv_bc", "account_tax_template_igic_sop_20_inv"),
    ("account_tax_template_p_igic0_imp_bc", "account_tax_template_igic_sop_i_0"),
    ("account_tax_template_p_igic3_imp_bc", "account_tax_template_igic_sop_i_3"),
    ("account_tax_template_p_igic7_imp_bc", "account_tax_template_igic_sop_i_7"),
    ("account_tax_template_p_igic95_imp_bc", "account_tax_template_igic_sop_i_9_5"),
    ("account_tax_template_p_igic15_imp_bc", "account_tax_template_igic_sop_i_15"),
    ("account_tax_template_p_igic20_imp_bc", "account_tax_template_igic_sop_i_20"),
    (
        "account_tax_template_p_igic0_imp_inv_bc",
        "account_tax_template_igic_sop_i_0_inv",
    ),
    (
        "account_tax_template_p_igic3_imp_inv_bc",
        "account_tax_template_igic_sop_i_3_inv",
    ),
    (
        "account_tax_template_p_igic7_imp_inv_bc",
        "account_tax_template_igic_sop_i_7_inv",
    ),
    (
        "account_tax_template_p_igic95_imp_inv_bc",
        "account_tax_template_igic_sop_i_9_5_inv",
    ),
    (
        "account_tax_template_p_igic15_imp_inv_bc",
        "account_tax_template_igic_sop_i_15_inv",
    ),
    (
        "account_tax_template_p_igic20_imp_inv_bc",
        "account_tax_template_igic_sop_i_20_inv",
    ),
    ("account_tax_template_p_igic0_re_bc", "account_tax_template_igic_p_re0"),
    ("account_tax_template_p_igic03_re_bc", "account_tax_template_igic_p_re03"),
    ("account_tax_template_p_igic07_re_bc", "account_tax_template_igic_p_re07"),
    ("account_tax_template_p_igic095_re_bc", "account_tax_template_igic_p_re095"),
    ("account_tax_template_p_igic15_re_bc", "account_tax_template_igic_p_re15"),
    ("account_tax_template_p_igic20_re_bc", "account_tax_template_igic_p_re20"),
    # account_assoc -> account_assoc_canary
    ("account_assoc_100", "account_assoc_canary_100"),
    ("account_assoc_1030", "account_assoc_canary_1030"),
    ("account_assoc_1034", "account_assoc_canary_1034"),
    ("account_assoc_1040", "account_assoc_canary_1040"),
    ("account_assoc_1044", "account_assoc_canary_1044"),
    ("account_assoc_120", "account_assoc_canary_120"),
    ("account_assoc_121", "account_assoc_canary_121"),
    ("account_assoc_129", "account_assoc_canary_129"),
    ("account_assoc_1300", "account_assoc_canary_1300"),
    ("account_assoc_1301", "account_assoc_canary_1301"),
    ("account_assoc_1320", "account_assoc_canary_1320"),
    ("account_assoc_1321", "account_assoc_canary_1321"),
    ("account_assoc_207", "account_assoc_canary_207"),
    ("account_assoc_2400", "account_assoc_canary_2400"),
    ("account_assoc_canary_240", "account_assoc_canary_2400"),
    ("account_assoc_2401", "account_assoc_canary_2401"),
    ("account_assoc_2402", "account_assoc_canary_2402"),
    ("account_assoc_2403", "account_assoc_canary_2403"),
    ("account_assoc_2404", "account_assoc_canary_2404"),
    ("account_assoc_2490", "account_assoc_canary_2490"),
    ("account_assoc_2491", "account_assoc_canary_2491"),
    ("account_assoc_2492", "account_assoc_canary_2492"),
    ("account_assoc_2493", "account_assoc_canary_2493"),
    ("account_assoc_2494", "account_assoc_canary_2494"),
    ("account_assoc_2807", "account_assoc_canary_2807"),
    ("account_assoc_2830", "account_assoc_canary_2830"),
    ("account_assoc_2831", "account_assoc_canary_2831"),
    ("account_assoc_2907", "account_assoc_canary_2907"),
    ("account_assoc_2935", "account_assoc_canary_2935"),
    ("account_assoc_296", "account_assoc_canary_296"),
    ("account_assoc_2990", "account_assoc_canary_2990"),
    ("account_assoc_canary_299", "account_assoc_canary_2990"),
    ("account_assoc_2991", "account_assoc_canary_2991"),
    ("account_assoc_2992", "account_assoc_canary_2992"),
    ("account_assoc_2993", "account_assoc_canary_2993"),
    ("account_assoc_2994", "account_assoc_canary_2994"),
    ("account_assoc_412", "account_assoc_canary_412"),
    ("account_assoc_447", "account_assoc_canary_447"),
    ("account_assoc_4480", "account_assoc_canary_4480"),
    ("account_assoc_canary_448", "account_assoc_canary_4480"),
    ("account_assoc_4482", "account_assoc_canary_4482"),
    ("account_assoc_4489", "account_assoc_canary_4489"),
    ("account_assoc_464", "account_assoc_canary_464"),
    ("account_assoc_4707", "account_assoc_canary_4707"),
    ("account_assoc_4757", "account_assoc_canary_4757"),
    ("account_assoc_490", "account_assoc_canary_490"),
    ("account_assoc_551", "account_assoc_canary_551"),
    ("account_assoc_5935", "account_assoc_canary_5935"),
    ("account_assoc_596", "account_assoc_canary_596"),
    ("account_assoc_canary_6343", "account_common_canary_6343"),
    ("account_assoc_canary_6344", "account_common_canary_6344"),
    ("account_assoc_canary_6393", "account_common_canary_6393"),
    ("account_assoc_canary_6394", "account_common_canary_6394"),
    ("account_assoc_6501", "account_assoc_canary_6501"),
    ("account_assoc_6502", "account_assoc_canary_6502"),
    ("account_assoc_6503", "account_assoc_canary_6503"),
    ("account_assoc_6504", "account_assoc_canary_6504"),
    ("account_assoc_6510", "account_assoc_canary_6510"),
    ("account_assoc_6511", "account_assoc_canary_6511"),
    ("account_assoc_6512", "account_assoc_canary_6512"),
    ("account_assoc_6513", "account_assoc_canary_6513"),
    ("account_assoc_6514", "account_assoc_canary_6514"),
    ("account_assoc_653", "account_assoc_canary_653"),
    ("account_assoc_654", "account_assoc_canary_654"),
    ("account_assoc_655", "account_assoc_canary_655"),
    ("account_assoc_6560", "account_assoc_canary_6560"),
    ("account_assoc_canary_656", "account_assoc_canary_6560"),
    ("account_assoc_6561", "account_assoc_canary_6561"),
    ("account_assoc_658", "account_assoc_canary_658"),
    ("account_assoc_663", "account_assoc_canary_663"),
    ("account_assoc_6710", "account_assoc_canary_6710"),
    ("account_assoc_canary_671", "account_assoc_canary_6710"),
    ("account_assoc_6711", "account_assoc_canary_6711"),
    ("account_assoc_6910", "account_assoc_canary_6910"),
    ("account_assoc_canary_691", "account_assoc_canary_6910"),
    ("account_assoc_6911", "account_assoc_canary_6911"),
    ("account_assoc_694", "account_assoc_canary_694"),
    ("account_assoc_720", "account_assoc_canary_720"),
    ("account_assoc_721", "account_assoc_canary_721"),
    ("account_assoc_722", "account_assoc_canary_722"),
    ("account_assoc_7230", "account_assoc_canary_7230"),
    ("account_assoc_canary_723", "account_assoc_canary_7230"),
    ("account_assoc_7231", "account_assoc_canary_7231"),
    ("account_assoc_7233", "account_assoc_canary_7233"),
    ("account_assoc_728", "account_assoc_canary_728"),
    ("account_assoc_763", "account_assoc_canary_763"),
    ("account_assoc_791", "account_assoc_canary_791"),
    ("account_assoc_794", "account_assoc_canary_794"),
    ("account_assoc_7962", "account_assoc_canary_7962"),
    ("account_assoc_7963", "account_assoc_canary_7963"),
    # account_full
    ("account_full_canary_134", "account_full_canary_1340"),
    ("account_full_canary_255", "account_full_canary_2550"),
    ("account_full_canary_47071", "account_common_canary_47071"),
    ("account_full_canary_47072", "account_common_canary_47072"),
    ("account_full_canary_553", "account_full_canary_5530"),
    ("account_full_canary_599", "account_full_canary_5990"),
    ("account_full_canary_6343", "account_common_canary_6343"),
    ("account_full_canary_6344", "account_common_canary_6344"),
    ("account_full_canary_6393", "account_common_canary_6393"),
    ("account_full_canary_6394", "account_common_canary_6394"),
    ("account_full_canary_644", "account_full_canary_6440"),
    ("account_full_canary_645", "account_full_canary_6450"),
    ("account_full_canary_651", "account_full_canary_6510"),
    ("account_full_canary_663", "account_full_canary_6630"),
    ("account_full_canary_763", "account_full_canary_7630"),
    ("account_full_canary_795", "account_full_canary_7950"),
    ("account_full_canary_830", "account_full_canary_8300"),
    # account_pymes
    ("account_pymes_canary_47071", "account_common_canary_47071"),
    ("account_pymes_canary_47072", "account_common_canary_47072"),
    ("account_pymes_canary_6343", "account_common_canary_6343"),
    ("account_pymes_canary_6344", "account_common_canary_6344"),
    ("account_pymes_canary_6393", "account_common_canary_6393"),
    ("account_pymes_canary_6394", "account_common_canary_6394"),
]

_xml_ids_renames_es_full_canary = [
    ("account_common_canary_4707", "account_full_canary_4707"),
    ("account_common_canary_4757", "account_full_canary_4757"),
]

_xml_ids_renames_es_pymes_canary = [
    ("account_common_canary_4707", "account_pymes_canary_4707"),
    ("account_common_canary_4757", "account_pymes_canary_4757"),
]

_taxes_to_merge = [
    (
        (
            "account_tax_template_s_igic_ISP3b",
            "account_tax_template_s_igic_ISP7b",
            "account_tax_template_s_igic_ISP95b",
            "account_tax_template_s_igic_ISP15b",
            "account_tax_template_s_igic_ISP20b",
        ),
        "account_tax_template_p_igic_ISP0bc",
    ),
    (
        (
            "account_tax_template_s_igic3_cmino_b",
            "account_tax_template_s_igic7_cmino_b"
            "account_tax_template_s_igic95_cmino_b",
            "account_tax_template_s_igic15_cmino_b",
            "account_tax_template_s_igic20_cmino_b",
        ),
        "account_tax_template_s_igic_cmino_b",
    ),
    (["account_tax_template_s_igic0s"], "account_tax_template_s_igic0b"),
    (["account_tax_template_s_igic3s"], "account_tax_template_s_igic3b"),
    (["account_tax_template_s_igic7s"], "account_tax_template_s_igic7b"),
    (["account_tax_template_s_igic95s"], "account_tax_template_s_igic95b"),
    (["account_tax_template_s_igic15s"], "account_tax_template_s_igic15b"),
    (["account_tax_template_s_igic20s"], "account_tax_template_s_igic20b"),
    (["account_tax_template_p_igic0_sc"], "account_tax_template_p_igic0_bc"),
    (["account_tax_template_p_igic3_sc"], "account_tax_template_p_igic3_bc"),
    (["account_tax_template_p_igic7_sc"], "account_tax_template_p_igic7_bc"),
    (["account_tax_template_p_igic95_sc"], "account_tax_template_p_igic95_bc"),
    (["account_tax_template_p_igic15_sc"], "account_tax_template_p_igic15_bc"),
    (["account_tax_template_p_igic20_sc"], "account_tax_template_p_igic20_bc"),
]

TAX_MERGE_OPS = {
    "amount": "target",
    "repartition_line_ids": "target",
    "name": "target",
    "description": "target",
    "invoice_label": "target",
}

TAX_REPARTITION_LINE_MERGE_OPS = {
    "tag_ids": "target",
    "factor": "target",
    "factor_percent": "target",
    "invoice_label": "target",
}


def rename_taxes_xmlids(env, company):
    _xml_ids_renames_company = [
        (
            f"account.{company.id}_{xml_ids[0]}",
            f"account.{company.id}_{xml_ids[1]}",
        )
        for xml_ids in _xml_ids_renames
    ]
    if company.chart_template == "es_full_canary":
        _xml_ids_renames_company.extend(
            [
                (
                    f"account.{company.id}_{xml_ids[0]}",
                    f"account.{company.id}_{xml_ids[1]}",
                )
                for xml_ids in _xml_ids_renames_es_full_canary
            ]
        )
    elif company.chart_template == "es_pymes_canary":
        _xml_ids_renames_company.extend(
            [
                (
                    f"account.{company.id}_{xml_ids[0]}",
                    f"account.{company.id}_{xml_ids[1]}",
                )
                for xml_ids in _xml_ids_renames_es_pymes_canary
            ]
        )

    openupgrade.rename_xmlids(env.cr, _xml_ids_renames_company)


def merge_tax_repartition_lines(env, tax_to_merge_into, taxes_to_merge):
    for rep_line_to_merge_into in tax_to_merge_into.mapped("repartition_line_ids"):
        rep_lines_to_merge = taxes_to_merge.mapped("repartition_line_ids").filtered(
            lambda rl,
            rep_line_to_merge_into=rep_line_to_merge_into: rl.repartition_type
            == rep_line_to_merge_into.repartition_type
            and rl.document_type == rep_line_to_merge_into.document_type
            and rl.account_id.id == rep_line_to_merge_into.account_id.id
        )
        if not rep_line_to_merge_into or len(rep_lines_to_merge) == 0:
            continue
        openupgrade_merge_records.merge_records(
            env,
            "account.tax.repartition.line",
            rep_lines_to_merge.ids,
            rep_line_to_merge_into.id,
            TAX_REPARTITION_LINE_MERGE_OPS,
            method="sql",
        )


def merge_taxes(env, company):
    for taxes in _taxes_to_merge:
        taxes_to_merge = env["account.tax"]
        for tax in taxes[0]:
            tax_id = env.ref(f"account.{company.id}_{tax}", False)
            if tax_id:
                taxes_to_merge |= tax_id
        tax_to_merge_into = env.ref(f"account.{company.id}_{taxes[1]}", False)
        if len(taxes_to_merge) > 0 and tax_to_merge_into:
            merge_tax_repartition_lines(env, tax_to_merge_into, taxes_to_merge)
            openupgrade_merge_records.merge_records(
                env,
                "account.tax",
                taxes_to_merge.ids,
                tax_to_merge_into.id,
                TAX_MERGE_OPS,
                method="sql",
            )


@openupgrade.migrate()
def migrate(env, version):
    for company in env["res.company"].search([]):
        merge_taxes(env, company)
        rename_taxes_xmlids(env, company)
