{ modulesPath, pkgs, ... }:
{
    imports = [
        (modulesPath + "/profiles/qemu-guest.nix")
        (modulesPath + "/installer/scan/not-detected.nix")
        ../disk-config.nix
    ];

    boot.loader.grub = {
        efiSupport = true;
        efiInstallAsRemovable = true;
    };

    services.openssh.enable = true;

    environment.systemPackages = with pkgs; [
        git
    ];

    users.users.root.openssh.authorizedKeys.keys = [
        "YOUR PUBLIC SSH KEY"
    ];

    nix.settings.experimental-features = [ "flakes" "nix-command" ];

    system.stateVersion = "24.11";
}