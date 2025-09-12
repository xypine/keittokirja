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
