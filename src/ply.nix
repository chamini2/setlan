let
   pkgs = import <nixpkgs> {};
 in
 { stdenv ? pkgs.stdenv, python ? pkgs.python, ply ? pkgs.python27Packages.ply }:

 stdenv.mkDerivation {
   name = "python-nix";
   version = "0.1.0.0";
   src = ./.;
   buildInputs = [ python ply ];
}

