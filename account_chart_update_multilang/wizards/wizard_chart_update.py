# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models
from odoo.tools import ormcache


class WizardUpdateChartsAccount(models.TransientModel):
    _inherit = "wizard.update.charts.accounts"

    lang = fields.Selection(default="en_US")

    @ormcache("self.lang")
    def _other_langs(self):
        return self.env["res.lang"].search([("code", "!=", self.lang)]).mapped("code")

    def _get_lang_selection_options(self):
        """Only can translate in base language by default."""
        en = self.env.ref("base.lang_en")
        return [(en.code, en.name)]

    def _update_other_langs(self, templates):
        for tpl_xmlid in templates.get_external_id().values():
            template = self.env.ref(tpl_xmlid)
            module, xmlid = tpl_xmlid.split(".", 1)
            rec_xmlid = f"{module}.{self.company_id.id}_{xmlid}"
            rec = self.env.ref(rec_xmlid, False)
            if not rec:
                continue
            translations = {}
            for key in self._diff_translate_fields(template, rec):
                for lang in self._other_langs():
                    field = rec._fields[key]
                    old_value = field._get_stored_translations(rec).get(
                        rec.env.lang, "en_US"
                    )
                    if old_value.startswith("<p>") and old_value.endswith("</p>"):
                        old_value = old_value[3:-4]
                    is_callable = callable(field.translate)
                    translated = template.with_context(lang=lang)[key]
                    translations[lang] = (
                        {old_value: translated} if is_callable else translated
                    )
                rec.update_field_translations(key, translations)

    def _diff_translate_fields(self, template, real):
        """Find differences by comparing the translations of the fields."""
        res = {}
        to_include = self.fields_to_include(template._name)
        for key in to_include:
            if not (template._fields.get(key) and template._fields[key].translate):
                continue
            for lang in self._other_langs():
                template_trans = template.with_context(lang=lang)[key]
                real_trans = real.with_context(lang=lang)[key]
                if template_trans != real_trans:
                    res[key] = template[key]
        return res

    def diff_fields(self, template, real):
        """Compare template and real translations too."""
        res = super().diff_fields(template, real)
        res.update(self._diff_translate_fields(template, real))
        return res

    def _update_taxes(self):
        """Update the taxes with their template translations."""
        res = super()._update_taxes()
        self._update_other_langs(self.tax_ids.tax_id)
        return res

    def _update_fiscal_positions(self):
        """Update the fiscal positions with their template translations."""
        res = super()._update_fiscal_positions()
        self._update_other_langs(self.fiscal_position_ids.fiscal_position_id)
        return res
