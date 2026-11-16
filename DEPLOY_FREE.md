# Free public test deployment

This project is prepared for a free demo using Render for the Django site and Supabase for PostgreSQL and property-photo storage.

## Before publishing the code

1. Create a **private** GitHub repository and push this project to it.
2. Keep `.gitignore` in place. It excludes the local database, uploads, and virtual environment.
3. Do not upload real customer records for a public test. The hosted database starts empty; add sample listings and customers after deployment.

If this is a new local Git repository, configure your commit identity first, then run `git add .`, `git commit`, and `git push` from `C:\RealEstateCRM`.

## Create free Supabase resources

1. Create a Supabase project.
2. In Storage, create a bucket named `property-images` and make it public. Public buckets allow anyone with an image URL to view those images, so store only photos intended for public property listings there.
3. Enable the S3 protocol in the Storage settings. Copy the S3 endpoint, region, access key ID, and secret access key.
4. From the project's **Connect** page, copy the **Session pooler** PostgreSQL connection string (port `5432`). Use this for `DATABASE_URL`; the direct database connection may require IPv6, while the shared session pooler supports IPv4.

## Deploy on Render

1. In Render, choose **New → Blueprint**, connect the GitHub repository, and apply its `render.yaml` blueprint.
2. When prompted, provide the Supabase values:
   - `DATABASE_URL`: the Session pooler connection string.
   - `SUPABASE_S3_BUCKET`: `property-images`.
   - `SUPABASE_S3_ACCESS_KEY` and `SUPABASE_S3_SECRET_KEY`: the S3 credentials.
   - `SUPABASE_S3_ENDPOINT_URL`: the copied S3 endpoint, for example `https://PROJECT_REF.storage.supabase.co/storage/v1/s3`.
   - `SUPABASE_S3_REGION`: the region shown in Supabase's S3 settings.
   - `SUPABASE_S3_PUBLIC_DOMAIN`: `PROJECT_REF.supabase.co/storage/v1/object/public/property-images` (without `https://`).
   - `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD`: choose credentials for the first CRM administrator. Keep the password private.
3. Render builds and deploys the app. Open the generated `.onrender.com` address and sign in with the administrator credentials.
4. Test the complete workflow: add a property and photo, view it on the public listing page, search it by its house ID, add a sample customer, and check sales/rentals and reports.

## Deploy on PythonAnywhere

The production settings enable WhiteNoise whenever `DEBUG=false`, so WhiteNoise must be installed in the same Python environment used by the PythonAnywhere web app. This project is configured to use `/home/reach55/.virtualenvs/realestate-env`. From a Bash console, run:

```bash
cd ~/RealEstateCRM
source ~/.virtualenvs/realestate-env/bin/activate
python -m pip install -r requirements.txt
```

If your PythonAnywhere Web tab uses a different virtualenv, replace the activation path with that virtualenv's `bin/activate` path. Then open the Web tab and click **Reload**. The `whitenoise>=6.9,<7` requirement is already included in `requirements.txt`; if the import error remains, confirm the Web tab and Bash console are using the same virtualenv.

## Free-plan limits

This is suitable for a demo, not production use. Render's free web service sleeps after 15 minutes without traffic, so the first visit can take about a minute to wake. Supabase Free currently includes 500 MB of database space and 1 GB of file storage; an inactive project can pause after a week. Check each provider's dashboard for current limits.

## Local development

Without `DATABASE_URL` and the Supabase storage variables, the project continues to use local SQLite and `./media` uploads. Production secrets belong in the hosting provider's environment settings, never in this file or GitHub.
