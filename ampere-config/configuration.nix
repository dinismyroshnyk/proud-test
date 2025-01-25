{ modulesPath, lib, pkgs, config, ... }:
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
        user = "nginx";
        group = "nginx";
        virtualHosts."130.61.74.203" = {
            addSSL = true;
            enableACME = false;
            sslCertificate = "/etc/ssl/certs/nginx-selfsigned.crt";
            sslCertificateKey = "/etc/ssl/private/nginx-selfsigned.key";
            locations."/" = {
                proxyPass = "http://127.0.0.1:8000";
            };
            locations."/dashboard/" = {
                proxyPass = "http://127.0.0.1:19999/";
                proxyWebsockets = true;
                extraConfig = ''
                    auth_basic "Netdata Dashboard";
                    auth_basic_user_file /var/lib/netdata/htpasswd;

                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;

                    rewrite ^/dashboard/?(.*)$ /$1 break;
                    sub_filter_once off;
                    sub_filter 'href="/' 'href="/dashboard/';
                    sub_filter 'src="/' 'src="/dashboard/';
                    sub_filter 'action="/' 'action="/dashboard/';
                '';
            };
        };
    };

    # Create Nginx user and group.
    users = {
        users.nginx = {
            isSystemUser = true;
            group = "nginx";
        };
        groups.nginx = {};
    };

    # Generate SSL certificates.
    systemd.services.generate-ssl-certs = {
        wantedBy = [ "nginx.service" ];
        before = [ "nginx.service" ];
        serviceConfig = {
            Type = "oneshot";
            User = "root";
            Group = "root";
        };
        script = ''
            # Create directories with proper permissions
            mkdir -p /etc/ssl/certs /etc/ssl/private
            chmod 755 /etc/ssl/certs
            chmod 710 /etc/ssl/private
            chown root:nginx /etc/ssl/private

            # Generate certificates
            ${pkgs.openssl}/bin/openssl req -x509 -nodes -days 365 \
                -newkey rsa:2048 \
                -keyout /etc/ssl/private/nginx-selfsigned.key \
                -out /etc/ssl/certs/nginx-selfsigned.crt \
                -subj "/CN=130.61.74.203" \
                -addext "subjectAltName = IP:130.61.74.203"

            # Set proper permissions for Nginx
            chmod 640 /etc/ssl/private/nginx-selfsigned.key
            chown root:nginx /etc/ssl/private/nginx-selfsigned.key
        '';
    };

    # Add systemd service for Django.
    systemd.services.django-app = {
        enable = true;
        description = "Django Application Service";
        after = [ "network.target" "postgresql.service" "nginx.service" ];
        wants = [ "postgresql.service" "nginx.service" ];

        serviceConfig = {
            Type = "simple";
            User = "root";
            WorkingDirectory = "/testing/app";
            ExecStartPre = "${pkgs.bash}/bin/bash -c 'source projectenv/bin/activate && python manage.py makemigrations --noinput && python manage.py migrate --noinput'";
            ExecStart = "${pkgs.bash}/bin/bash -c 'source projectenv/bin/activate && python manage.py runserver'";
            Restart = "always";
            RestartSec = "30s";
            EnvironmentFile = "/etc/django-environment";
        };

        environment = {
            PYTHONPATH = "/testing/app";
            DJANGO_SETTINGS_MODULE = "app.settings";
        };
    };

    # Create environment file for secrets
    environment.etc."django-environment" = {
        text = ''
            DB_NAME=proud_db
            DB_USER=root
            DB_HOST=localhost
            DB_PORT=5432
        '';
        mode = "0600";
    };

    # System packages.
    environment.systemPackages = with pkgs; [
        apacheHttpd
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

    # Root user keys.
    users.users = {
        root.openssh.authorizedKeys.keys = [
            "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEBuRiGrNd5DLnjN3EbqV2wRvlnOh9iMmIOTsLfMvQRE dinis@omen-15"
            "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMdCQ8vgC3QBlUu3rI65VzTiomxsprsIv5hHU7oiLoeKBFtG4IlgkgIYyV2mayMbIjQ7bx/t1MfHHx+8+y+WrYI= dinis myroshnyk@WIN-7TB4RCE36HU"
            "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEnG5aUk9bdYx51nnDCy4JE9HQ5doRIHLAXJZKXD2oKB dinismyroshnyk2@protonmail.com"
            "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNRWrtr+9OZyz1yt8sRDWyXW949CPhk5ejkqYofnGcJWApPEFkTJY2NK7YvG7nVMJhcK63OUNKGolajl9zyPcM4= mariana@LAPTOP-HS584L9C"
        ];
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
            # TYPE  DATABASE   USER     ADDRESS       METHOD
            local   all        all                    trust
            host    all        all      127.0.0.1/32  trust
            host    all        all      ::1/128       trust
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