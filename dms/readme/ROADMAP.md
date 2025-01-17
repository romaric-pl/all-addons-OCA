- Files preview in portal
- Allow to download folder in portal and create zip file with all
  content
- Save in cache own_root directories and update in every
  create/write/unlink function
- Add a migration procedure for converting an storage to attachment one
  for populating existing records with attachments as folders
- Add a link from attachment view in chatter to linked documents
- If Inherit permissions from related record (the
  inherit_access_from_parent_record field from storage) is changed when
  directories already exist, inconsistencies may occur because groups
  defined in the directories and subdirectories will still exist, all
  groups in these directories should be removed before changing.
- Since portal users can read `dms.storage` records, if your module
  extends this model to another storage backend that needs using
  secrets, remember to forbid access to the secrets fields by other
  means. It would be nice to be able to remove that rule at some point.
- Searchpanel in files: Highlight items (shading) without records when
  filtering something (by name for example).
- Accessing the clipboard (for example copy share link of file/directory)
  is limited to secure connections. It also happens in any part of Odoo.