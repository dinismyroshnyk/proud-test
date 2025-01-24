{ modulesPath, lib, pkgs, ... }:
let
    pythonEnv = pkgs.python3.withPackages (ps: with ps; [ pip ]);
in
{
    imports = [
        (modulesPath + "/profiles/qemu-guest.nix")
        ../disk-config.nix
    ];

    # Allow unfree packages.
    nixpkgs.config.allowUnfreePredicate = pkg: builtins.elem (lib.getName pkg) [
        "netdata"
        "postman"
    ];

    # Bootloader.
    boot.loader.grub = {
        efiSupport = true;
        efiInstallAsRemovable = true;
    };

    # OpenSSH.
    services.openssh = {
        enable = true;
        settings = {
            PasswordAuthentication = false;
            PermitRootLogin = "prohibit-password";
        };
    };

    # Netdata.
    services.netdata = {
        enable = true;
        package = pkgs.netdata.override {
            withCloudUi = true;
        };
        config = {
            web = {
                mode = "static-threaded";
                bind_to = "127.0.0.1";
            };
        };
    };

    # Nginx.
    services.nginx = {
        enable = true;
        virtualHosts."130.61.74.203" = {
            addSSL = true;
            enableACME = false;
            sslCertificate = "/etc/ssl/certs/nginx-selfsigned.crt";
            sslCertificateKey = "/etc/ssl/private/nginx-selfsigned.key";
            locations."/" = {
                proxyPass = "http://127.0.0.1:8000";
            };
            locations."/dashboard/" = {
                proxyPass = "http://127.0.0.1:19999";
            };
        };
    };

    # Generate SSL certificates.
    systemd.services.generate-ssl-certs = {
        wantedBy = [ "nginx.service" ];
        before = [ "nginx.service" ];
        serviceConfig.Type = "oneshot";
        script = ''
            mkdir -p /etc/ssl/{certs,private}
            ${pkgs.openssl}/bin/openssl req -x509 -nodes -days 365 \
                -newkey rsa:2048 \
                -keyout /etc/ssl/private/nginx-selfsigned.key \
                -out /etc/ssl/certs/nginx-selfsigned.crt \
                -subj "/CN=130.61.74.203"
        '';
    };

    # System packages.
    environment.systemPackages = with pkgs; [
        screen
        nodePackages.npm
        pythonEnv
    ];

    # Enabled programs.
    programs = {
        git.enable = true;
        neovim = {
            enable = true;
            vimAlias = true;
            viAlias = true;
        };
    };

    # Firewall settings.
    networking.firewall.allowedTCPPorts = [ 80 443 ];

    # Remove sudo password requirement for specified users. Currently not working.
    security.sudo.extraRules = [{
        users = [ "dinis" "ricol" "mariana" ];
        commands =  [ { command = "/home/root/secret.sh"; options = [ "SETENV" "NOPASSWD" ]; } ];
    }];

    # Users.
    users.users = {
        root.openssh.authorizedKeys.keys = [ # Remove later.
            "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEBuRiGrNd5DLnjN3EbqV2wRvlnOh9iMmIOTsLfMvQRE dinis@omen-15"
            "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEnG5aUk9bdYx51nnDCy4JE9HQ5doRIHLAXJZKXD2oKB dinismyroshnyk2@protonmail.com"
        ];
        dinis = {
            isNormalUser = true;
            extraGroups = [ "wheel" ];
            openssh.authorizedKeys.keys = [
                "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEBuRiGrNd5DLnjN3EbqV2wRvlnOh9iMmIOTsLfMvQRE dinis@omen-15"
                "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMdCQ8vgC3QBlUu3rI65VzTiomxsprsIv5hHU7oiLoeKBFtG4IlgkgIYyV2mayMbIjQ7bx/t1MfHHx+8+y+WrYI= dinis myroshnyk@WIN-7TB4RCE36HU"
            ];
        };
        ricol = {
            isNormalUser = true;
            extraGroups = [ "wheel" ];
            openssh.authorizedKeys.keys = [];
        };
        mariana = {
            isNormalUser = true;
            extraGroups = [ "wheel" ];
            openssh.authorizedKeys.keys = [
                "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNRWrtr+9OZyz1yt8sRDWyXW949CPhk5ejkqYofnGcJWApPEFkTJY2NK7YvG7nVMJhcK63OUNKGolajl9zyPcM4= mariana@LAPTOP-HS584L9C"
            ];
        };
    };

    # Enable PostgreSQL.
    services.postgresql = {
        enable = true;
        settings.port = 5432;
        ensureUsers = [
            {
                name = "root";
                ensureClauses = {
                    superuser = true;
                    createrole = true;
                    createdb = true;
                };
            }
        ];
        ensureDatabases = [ "proud_db" ];
        authentication = pkgs.lib.mkOverride 10 ''
            #type  database   DBuser  auth-method
            local  all        all     trust
            host   all        all     127.0.0.1/32   trust
        '';
    };

    # Environment aliases.
    environment.shellAliases = {
        cls="clear";
    };

    # Enable flake support.
    nix.settings.experimental-features = [ "flakes" "nix-command" ];

    # System state version.
    system.stateVersion = "24.11";
}