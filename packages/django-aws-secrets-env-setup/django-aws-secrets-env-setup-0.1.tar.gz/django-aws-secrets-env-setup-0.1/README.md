# django-aws-secrets-env-setup
This is a helper function to set up environment variables from AWS secrets manager.
The main function to use is `set_env_variables(secret_name, default_region_name)`.
`secret_name` is the name of the secret to get from the manager.
`default_region_name` is the region that should be used if `os.environ["SECRETS_REGION_NAME"]` is not set.
