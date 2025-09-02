{
  pkgs,
  lib,
  config,
  ...
}:
{
  # https://devenv.sh/languages/
  languages = {
    python = {
      enable = true;
      uv.enable = true;
    };
  };

  packages = with pkgs; [
    just
  ];

  # See full reference at https://devenv.sh/reference/options/
}
