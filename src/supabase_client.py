import os

from supabase import create_client, Client

# The persistence layer.

SUPABASE_URL = os.environ.get(
    "SUPABASE_URL"
)

SUPABASE_SERVICE_ROLE_KEY = os.environ.get(
    "SUPABASE_SERVICE_ROLE_KEY"
)

BUCKET_NAME = "documents"


if not SUPABASE_URL:

    raise RuntimeError(
        "SUPABASE_URL environment variable "
        "is not set."
    )


if not SUPABASE_SERVICE_ROLE_KEY:

    raise RuntimeError(
        "SUPABASE_SERVICE_ROLE_KEY environment variable "
        "is not set."
    )


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)
