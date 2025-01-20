{ pkgs ? import <nixpkgs> {} }:

let
    pythonEnv = pkgs.python3.withPackages (ps: with ps; [ pip ]);
    projectRoot = builtins.toString ./.;
in
pkgs.mkShell {
    buildInputs = with pkgs; [
        pythonEnv
        tree
        postgresql
        firefox
        nodePackages.npm
    ];

    shellHook = ''
        export PYTHONPATH=$PYTHONPATH:$(pwd)

        python3 -m venv app/projectenv
        source app/projectenv/bin/activate

        pip install -r app/requirements.txt

        if [ ! -d app/static/proud/node_modules ]; then
            (
                cd app/static/proud &&
                echo "Installing dependencies:" &&
                npm install @types/node &&
                npm install @rollup/plugin-alias &&
                npm install @sveltejs/vite-plugin-svelte &&
                npm install @tsconfig/svelte &&
                npm install svelte &&
                npm install svelte-check &&
                npm install tslib &&
                npm install typescript &&
                npm install vite
            )
        fi

        alias cls='clear'
        alias srun-open="(cd ${projectRoot}/app && python manage.py makemigrations && python manage.py migrate && python manage.py runserver > /dev/null 2>&1 &) && firefox 127.0.0.1:8000"
        alias srun="(cd ${projectRoot}/app && python manage.py makemigrations && python manage.py migrate && python manage.py runserver)"
        alias close='pkill -f "python manage.py runserver"'
        alias drun='(cd ${projectRoot}/app/static/proud && npm run dev)'

        echo "Shell is ready!"
    '';
}