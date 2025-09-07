{
  pkgs,
  lib,
  config,
  ...
}:
{
  env = {
    DATABASE_URL = "dev.db";
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
