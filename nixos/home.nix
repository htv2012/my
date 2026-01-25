# home.nix
{ config, pkgs, ... }:
{
  home-manager.backupFileExtension = "bak";
  home-manager.users.haiv = {

    # Enable dconf settings
    dconf.settings = {
      "org/gnome/desktop/interface" = {
        color-scheme = "prefer-dark";
      };
    };

    # Set GTK theme for older apps
    gtk = {
      enable = true;
      theme = {
        name = "Adwaita-dark";
        package = pkgs.gnome-themes-extra;
      };
    };

    home.sessionPath = [
      "$HOME/.local/bin"
      "$HOME/my/bin"
    ];

    home.sessionVariables = {
      EDITOR = "vim";
      VISUAL = "vim";
    };

    # Sync Qt apps with the GTK theme
    qt = {
      enable = true;
      platformTheme.name = "adwaita";
      style.name = "adwaita-dark";
    };

    # ==================================================================
    # programs
    # ==================================================================

    programs.alacritty = {
      enable = true;
      settings = {
        font = {
          size = 16.0;
          normal = {
            family = "Inconsolata Nerd Font";
            style = "Regular";
          };
        };
      };
    };

    programs.bat = {
      enable = true;
      config = {
        style = "plain";
        theme = "Coldark-Dark";
        map-syntax = "*.exp:Tcl";
      };
    };

    programs.firefox = {
      enable = true;
      profiles.default = {
        search = {
          force = true;
          # Change the default engine here
          default = "ddg";

          engines = {
            "Python Library" = {
              urls = [
                {
                  template = "https://docs.python.org/3/library/{searchTerms}.html";
                }
              ];
              icon = "https://www.python.org/static/favicon.ico";
              definedAliases = [ "py" ];
            };

            # If you want to ensure DuckDuckGo is explicitly configured
            # or use a specific region/theme via URL:
            "ddg" = {
              metaData.alias = "@ddg";
            };
          };
        };
      };
    };

    programs.fzf = {
      enable = true;
      enableBashIntegration = true;
      enableZshIntegration = true;
      enableFishIntegration = true;
    };

    programs.git = {
      enable = true;
      settings = {
        user.name = "Hai Vu";
        user.email = "haivu2004@gmail.com";
        init.defaultBranch = "main";
        pull.rebase = true;
      };
    };

    programs.ssh = {
      enable = true;

      # Disable the legacy default config
      enableDefaultConfig = false;

      matchBlocks = {
        "debian1" = {
          hostname = "134.199.226.49";
          user = "haiv";
          identityFile = "~/.ssh/id_ed25519";
        };
        "github.com" = {
          hostname = "github.com";
          user = "git";
          identityFile = "~/.ssh/id_ed25519";
        };
        "*" = {
          addKeysToAgent = "yes";
        };
      };
    };

    programs.vim = {
      enable = true;
      defaultEditor = true;
      extraConfig = ''
        colorscheme darkblue
        set number
        set autoindent
        syntax on
      '';
    };

    programs.zed-editor = {
      enable = true;

      # Your settings.json translated to Nix
      userSettings = {
        vim_mode = true;
        icon_theme = "Zed (Default)";
        ui_font_size = 16;
        buffer_font_size = 15;

        theme = {
          mode = "dark";
          light = "One Light";
          dark = "One Dark";
        };

        languages = {
          Python = {
            language_servers = [
              "ty"
              "!pyright"
              "!basedpyright"
            ];
          };
        };

        ssh_connections = [
          {
            host = "debian1";
            args = [ ];
            projects = [
              { paths = [ "/home/haiv" ]; }
              { paths = [ "/home/haiv/Projects" ]; }
              { paths = [ "/home/haiv/Projects/pytest-sandbox/./" ]; }
              { paths = [ "/home/haiv/Projects/python-sandbox/./" ]; }
            ];
          }
        ];
      };

      # Optional: List extensions you want to ensure are installed
      extensions = [
        "python"
        "nix"
      ];
    };

    programs.zsh = {
      enable = true;
      enableCompletion = true;

      initContent = ''
        PROMPT=$'\n'"%{$(tput setaf 39)%}%n%{$(tput setaf 45)%}@%{$(tput setaf 51)%}%m %{$(tput setaf 195)%}%~ %{$(tput sgr0)%}"$'\n'"$ "
      '';

      shellAliases = {
        ".." = "cd ..";
        "..." = "cd ../..";
        "...." = "cd ../../..";
        "....." = "cd ../../../..";
        cdd = "cd ~/Downloads";
        cdp = "cd ~/Projects";
        cdm = "cd ~/my";

        zed = "zeditor";

        ls = "eza";
        ll = "ls -l";
        lla = "ll -A";
        lld = "ll -d";

        ga = "git add";
        gc = "git commit";
        gd = "git diff";
        gl = "git pull";
        gp = "git push";
        gs = "git status";

        path = "tr : $'\n' <<< $PATH";
      };
    };
  };
}
