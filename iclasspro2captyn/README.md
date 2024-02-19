# iClassPro to Captyn Data Conversion

This tool converts account information from iClassPro to a CSV format that can be imported into Captyn.

# Usage Notes

    1. Export all columns from iClassPro to a CSV file.
    2. Edit the exported CSV and append numbers to the following column names to make them unique:
        Secondary Guardian Name -> 1,2,3,4
        Secondary Phone Number -> 1,2,3
        Secondary Email -> 1,2

    3. Ensure the iclass_event_to_captyn_offering table correctly reflects the mapping for your use.
    4. Add any custom columns to captyn_accounts_and_participants_cols
    5. Update any column mappings in iclass_to_captyn_account and iclass_to_captyn_participant
    6. in the main() function, edit the filename to match your iClassPro CSV export
    7. Run and enjoy.