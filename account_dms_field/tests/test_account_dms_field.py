from odoo.addons.base.tests.common import BaseCommon


class TestAccountDmsField(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, test_dms_field=True))
        cls.template = cls.env.ref("account_dms_field.field_template_account")
        cls.storage = cls.template.storage_id
        cls.access_group = cls.template.group_ids
        cls.account_model = cls.env["account.move"]
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.test_directory = cls.env["dms.directory"].create(
            {
                "name": "Test Directory",
                "parent_id": cls.template.dms_directory_ids[0].id,
                "storage_id": cls.template.storage_id.id,
            }
        )

    def test_01_account_document_directory(self):
        account_move = self.account_model.create(
            {
                "partner_id": self.partner.id,
            }
        )
        account_move.invalidate_model()
        directory = account_move.dms_directory_ids
        # Assert that only one directory is created for the account move.
        self.assertEqual(len(directory), 1, "Directory length must be 1.")
        # Assert that the storage associated with the directory is the same as the
        # template's storage.
        self.assertEqual(
            directory.storage_id,
            self.storage,
            "Account move directory storage is different from the template storage.",
        )
        # Assert that the custom access group is present in the directory's group
        # list.
        self.assertIn(
            self.access_group,
            directory.group_ids,
            "Account move directory groups are different from the template groups.",
        )
        # Map the names of child directories related to the account move directory.
        child_directory_names = directory.mapped("child_directory_ids.name")
        # Assert that a specific child directory, "Test Directory", exists.
        self.assertIn(
            "Test Directory",
            child_directory_names,
            "Test Directory is not in the child directory of the account move "
            "directory.",
        )
