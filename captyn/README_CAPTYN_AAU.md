# Captyn AAU
Captyn Membership synchronization for AAU Swimming. Use Captyn as the source of truth for your AAU Swimming registrations and periodically import them from Captyn to AAU Swimming.

# Setup
AAU Swimming charges $22/year for the extended coverage option and renews every September 1st.

Create a Membership in Captyn for AAU Swimming. Configure it to renew on September 1st and to have separate price points in multiples of $22 for 1, 2, 3, 4, etc swimmers.

## captynprofile2membership
Generates a CSV file that can be manually given to Captyn to add all Captyn Profiles as members to a Captyn Membership.

To bulk add all swimmers from Captyn into the new Captyn AAU Membership, you need to provide a CSV to your Captyn support contact. This tool generates that CSV.

## captyngroup2membership
Generates a CSV file that can be manually given to Captyn to add all Captyn Group offering members to a Captyn Membership.

To bulk add swimmers from a specific Captyn Program Offering into the new Captyn AAU Membership, you need to provide a CSV to your Captyn support contact. This tool generates that CSV.

## captyn2aau
Generates a CSV file that can be loaded into AAU from a Captyn Membership CSV export.

This tool takes the CSV export from a Captyn Membership and formats it to be imported into AAU Swiming for registration.

### Creating AAU Memberships From Captyn Data
This is used to register all swimmers for AAU Swimming that have the Captyn AAU Membership 

1. Export the Membership list for the AAU Swimming membership that was created in Captyn
2. Export the latest Profiles list from Captyn
3. Edit `captyn2aau.py` to refer to the two downloaded files.
4. Run `captyn2aau.py`
2. Go to the AAU [Import Memberships Screen](https://play.aausports.org/joinaau/importathletememberships.aspx).
3. Enter your AAU Club Code (Oaklantis is W3D794)
4. Provide the CSV file generated from `captyn2aau.py`
5. Review the summary from the import. If swimmers already exist, that's ok. Sometimes AAU doesn't perfectly match existing swimmers from the Captyn export, so make sure you don't have duplicates.

Note: Gender is optional in Captyn, but required for AAU. Swimmers in Captyn with no specified gender are exported as "O" for "other". When importing to AAU, this will generate an error. You must manually correct this in the exported CSV to be "M" or "F", or record the gender in Captyn and then re-export.
