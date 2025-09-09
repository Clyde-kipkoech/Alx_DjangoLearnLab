Permissions & Groups Setup:
- Book model has 4 custom permissions: can_view, can_create, can_edit, can_delete.
- Groups:
  - Viewers → can_view
  - Editors → can_view, can_create, can_edit
  - Admins → can_view, can_create, can_edit, can_delete
- Views are protected with @permission_required decorators.
- Assign users to groups via the Django admin site.
