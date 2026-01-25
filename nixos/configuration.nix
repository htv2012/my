# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running ‘nixos-help’).

{ config, pkgs, ... }:
{

  imports = [
    ./hardware-configuration.nix
    <home-manager/nixos>
    ./home.nix
  ];

  nix.settings.experimental-features = [
    "nix-command"
    "flakes"
  ];

  home-manager.users.haiv =
    { pkgs, ... }:
    {
      home.stateVersion = "25.05";
    };

  # Bootloader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  hardware.system76.enableAll = true;
  networking.hostName = "lemur"; # Define your hostname.
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Enable networking
  networking.networkmanager.enable = true;

  # Set your time zone.
  time.timeZone = "America/Los_Angeles";

  # Select internationalisation properties.
  i18n.defaultLocale = "en_US.UTF-8";

  i18n.extraLocaleSettings = {
    LC_ADDRESS = "en_US.UTF-8";
    LC_IDENTIFICATION = "en_US.UTF-8";
    LC_MEASUREMENT = "en_US.UTF-8";
    LC_MONETARY = "en_US.UTF-8";
    LC_NAME = "en_US.UTF-8";
    LC_NUMERIC = "en_US.UTF-8";
    LC_PAPER = "en_US.UTF-8";
    LC_TELEPHONE = "en_US.UTF-8";
    LC_TIME = "en_US.UTF-8";
  };

  # Enable the X11 windowing system.
  services.xserver.enable = true;

  # Enable the GNOME Desktop Environment.
  services.displayManager.gdm.enable = true;
  services.desktopManager.gnome.enable = true;

  # Configure keymap in X11
  services.xserver.xkb = {
    layout = "us";
    variant = "";
  };

  # Enable CUPS to print documents.
  services.printing.enable = true;

  # Enable System76 power management
  services.power-profiles-daemon.enable = false;
  hardware.system76.power-daemon.enable = true;

  # Enable sound with pipewire.
  services.pulseaudio.enable = false;
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
    # If you want to use JACK applications, uncomment this
    #jack.enable = true;

    # use the example session manager (no others are packaged yet so this is enabled by default,
    # no need to redefine it in your config for now)
    #media-session.enable = true;
  };

  # Enable touchpad support (enabled default in most desktopManager).
  # services.xserver.libinput.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.haiv = {
    isNormalUser = true;
    description = "Hai Vu";
    extraGroups = [
      "adm"
      "networkmanager"
      "video"
      "wheel"
    ];
    packages = with pkgs; [
      #  thunderbird
    ];
    shell = pkgs.zsh;
  };

  # Install firefox.
  programs.firefox.enable = true;

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  # List packages installed in system profile. To search, run:
  # $ nix search wget
  environment.systemPackages = with pkgs; [
    pkgs._1password-cli
    pkgs._1password-gui
    pkgs.alacritty
    pkgs.bat
    pkgs.brightnessctl
    pkgs.bruno
    pkgs.bruno-cli
    pkgs.curl
    pkgs.eza
    pkgs.foot
    pkgs.fzf
    pkgs.gawk
    pkgs.ghostty
    pkgs.git
    pkgs.gnumake
    pkgs.gnused
    pkgs.google-chrome
    pkgs.joplin
    pkgs.joplin-desktop
    pkgs.jq
    pkgs.kitty
    pkgs.nerd-fonts.inconsolata
    pkgs.nixfmt
    pkgs.python3
    pkgs.ripgrep
    pkgs.tree
    pkgs.uv
    pkgs.vim
    pkgs.vscode
    pkgs.vscode
    pkgs.wezterm
    pkgs.wget
    pkgs.xsel
    pkgs.zed-editor
    pkgs.zsh
  ];

  # zsh
  programs.zsh = {
    enable = true;
    promptInit = ''
                  # Load version control information
                  autoload -Uz vcs_info
                  precmd() { vcs_info }

                  # Format the git information
                  # %b: branch name
                  # %u: unstaged changes (dirty flag)
                  zstyle ':vcs_info:git:*' formats '%F{cyan}%b%u%f'
                  zstyle ':vcs_info:git:*' actionformats '%F{cyan}%b%f|%F{red}%a%u%f'
                  zstyle ':vcs_info:git:*' check-for-changes true
                  zstyle ':vcs_info:git:*' unstagedstr '%F{cyan}*%f'

                  # Build the prompt
                  # %(?..%F{yellow}%?%f ): Show exit code in yellow if non-zero
                  # %F{green}%~%f: Green directory (relative to home)
                  # ''${vcs_info_msg_0_}: Git info
                  # $'\n': New line
                  # %F{green}$%f : Green dollar sign and space
      	    PROMPT="%{%F{226}%}%n%{%F{220}%}@%{%F{214}%}%m %{%F{33}%}%1~ %{%f%}
      $ "
    '';
  };

  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };

  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  # services.openssh.enable = true;

  # Open ports in the firewall.
  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  # Or disable the firewall altogether.
  # networking.firewall.enable = false;

  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It‘s perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  # Before changing this value read the documentation for this option
  # (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
  system.stateVersion = "25.11"; # Did you read the comment?

}
