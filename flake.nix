{
  description = "Node.js development environment with npm and npx";

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
            packages = with pkgs; [
              nodejs
            ];

            shellHook = ''
              echo "🚀 Node.js dev shell loaded!"
              echo "Node version: $(node --version)"
              echo "npm version:  $(npm --version)"
              echo "npx version:  $(npx --version)"
            '';
          };
        });
    };
}
