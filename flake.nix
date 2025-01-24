{
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
        disko = {
            url = "github:nix-community/disko";
            inputs.nixpkgs.follows = "nixpkgs";
        };
        sops-nix.url = "github:Mic92/sops-nix";
    };

    outputs = { self, nixpkgs, disko, sops-nix, ...}: {
        nixosConfigurations = {
            ampere-install = nixpkgs.lib.nixosSystem {
                system = "aarch64-linux";
                modules = [
                    disko.nixosModules.disko
                    ./ampere-install/configuration.nix
                    ./ampere-install/hardware-configuration.nix
                ];
            };
            ampere-config = nixpkgs.lib.nixosSystem {
                system = "aarch64-linux";
                modules = [
                    disko.nixosModules.disko
                    sops-nix.nixosModules.sops
                    ./ampere-config/configuration.nix
                    ./ampere-config/hardware-configuration.nix
                ];
            };
        };
        ampere-config = self.nixosConfigurations.ampere-config.config.system.build.toplevel;
    };
}