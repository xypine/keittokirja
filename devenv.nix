{
  pkgs,
  lib,
  config,
  ...
}:
{
  env = {
    DATABASE_URL = "dev.db";
    SECRET_KEY = "DEVDEVDEV";
    VERIFY_CONTACT = "joe@example.com";
  };

  # https://devenv.sh/languages/
  languages = {
    python = {
      enable = true;
      uv.enable = true;
    };
  };

  packages = with pkgs; [
    sqlite
    just
  ];

  # See full reference at https://devenv.sh/reference/options/
}
