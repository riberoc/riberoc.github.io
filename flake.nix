{
  description = "Quartz digital garden development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSystem = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forEachSystem (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            # Provide Node.js (which includes npm/npx) and git (required by Quartz)
            packages = with pkgs; [
              nodejs_22
              git
            ];

            shellHook = ''
              echo "🪴 Quartz dev environment loaded!"
              echo "Node version: $(node --version)"
              echo "npm version:  $(npm --version)"

              # Automatically install node_modules if they don't exist yet
              if [ ! -d "node_modules" ]; then
                echo "📦 Installing npm dependencies for Quartz..."
                npm install
              fi
            '';
          };
        });
    };
}
